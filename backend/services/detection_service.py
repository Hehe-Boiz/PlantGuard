import cv2
import numpy as np
import time
from typing import List, Dict, Any, Tuple
import onnxruntime as ort

from config import *
from models.detection import Detection
from utils.image_utils import ImageUtils
from services.classification_service import YoloClassifier

class YoloOnnxDetector:
    def __init__(self, model_path: str, input_size: int):
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_size = input_size

    def _preprocess(self, frame: np.ndarray) -> Tuple[np.ndarray, float, Tuple[int, int], Tuple[int, int]]:
        h, w = frame.shape[:2]
        scale = self.input_size / max(h, w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(frame, (nw, nh))
        
        canvas = np.full((self.input_size, self.input_size, 3), 114, dtype=np.uint8)
        pad_top = (self.input_size - nh) // 2
        pad_left = (self.input_size - nw) // 2
        canvas[pad_top:pad_top + nh, pad_left:pad_left + nw] = resized
        
        return cv2.dnn.blobFromImage(canvas, 1/255.0, (self.input_size, self.input_size), swapRB=True, crop=False), scale, (pad_left, pad_top), (w, h)

    def _postprocess(self, preds: np.ndarray, scale: float, pad: Tuple[int, int], orig_shape: Tuple[int, int]) -> List[Detection]:
        preds = preds[0].T 
        pad_left, pad_top = pad
        ow, oh = orig_shape
        boxes, scores, class_ids = [], [], []
        
        for det in preds:
            if (conf := det[4]) < CONF_THRES: continue
            
            cx, cy, w, h = det[:4]
            x1, y1 = int((cx - w/2 - pad_left) / scale), int((cy - h/2 - pad_top) / scale)
            x2, y2 = int((cx + w/2 - pad_left) / scale), int((cy + h/2 - pad_top) / scale)
            
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(ow-1, x2), min(oh-1, y2)
            if x2 <= x1 or y2 <= y1: continue
            
            boxes.append([x1, y1, x2 - x1, y2 - y1])
            scores.append(conf)
            class_ids.append(0)

        if not boxes: return []
        indices = cv2.dnn.NMSBoxes(boxes, scores, CONF_THRES, IOU_THRES)
        
        return [Detection(class_ids[i], scores[i], (boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3])) for i in indices.flatten()]

    def detect(self, frame: np.ndarray) -> List[Detection]:
        blob, scale, pad, orig_shape = self._preprocess(frame)
        preds = self.session.run([self.output_name], {self.input_name: blob})[0]
        return self._postprocess(preds, scale, pad, orig_shape)

class DetectionService:
    def __init__(self, model_path: str, input_size: int):
        self.detector = YoloOnnxDetector(model_path, input_size)
        print("✅ Detection service initialized with model.")
        
        self.classifier = YoloClassifier(
            model_path=YOLO_CLASSIFIER_MODEL_PATH,
            input_size=YOLO_CLASSIFIER_INPUT_SIZE,
            conf_thres=YOLO_CLASSIFIER_CONF_THRES
        )


    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Nhận một ảnh dạng bytes, chạy phát hiện, phân loại và trả về kết quả.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        detections = self.detector.detect(frame)
        
        timestamp = int(time.time())
        original_filename = f"{timestamp}_original.jpg"
        cv2.imwrite(f"{RECEIVED_IMAGES_DIR}/{original_filename}", frame)

        result_data = {
            "original_image": original_filename,
            "detections_found": len(detections),
            "results": []
        }

        if detections:
            cropped_images = ImageUtils.crop_from_detections(frame, detections)
            
            # <<< THAY ĐỔI LOGIC PHÂN LOẠI >>>
            classification_results = self.classifier.classify(cropped_images)

            for i, cropped_img in enumerate(cropped_images):
                cropped_filename = f"{timestamp}_detection_{i+1}.jpg"
                cv2.imwrite(f"{DETECTION_RESULTS_DIR}/{cropped_filename}", cropped_img)
                
                # Lấy kết quả phân loại tương ứng và kiểm tra
                class_result = classification_results[i]
                
                if class_result:
                    class_id, class_conf = class_result
                    class_name = YOLO_CLASSIFIER_CLASS_NAMES[class_id]
                    classification_info = {
                        "label": class_name,
                        "confidence": f"{class_conf:.4f}"
                    }
                else:
                    # Trường hợp không phân loại được
                    classification_info = {
                        "label": "Unclassified",
                        "confidence": "0.0000"
                    }

                det_info = {
                    "detection_box": detections[i].box,
                    "detection_confidence": f"{detections[i].conf:.4f}",
                    "cropped_image_file": cropped_filename,
                    "classification_result": classification_info
                }
                result_data["results"].append(det_info)
            
        return result_data
