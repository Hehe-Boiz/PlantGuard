import cv2
import numpy as np
import time
import os
import json
from typing import List, Dict, Any, Tuple, Optional
import onnxruntime as ort
from datetime import datetime

from config import *
from models.detection import Detection
from utils.image_utils import ImageUtils
from services.classification_service import YoloClassifier, CNNClassifier, TensorFlowH5Classifier

class YoloOnnxDetector:
    def __init__(self, model_path: str, input_size: int, is_unified_model: bool = False):
        """
        Khởi tạo detector.
        - is_unified_model: True nếu model này vừa detect vừa classify.
        """
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_size = input_size
        self.is_unified_model = is_unified_model

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
            if self.is_unified_model:
                class_scores = det[4:]
                class_id = np.argmax(class_scores)
                conf = class_scores[class_id]
            else:
                conf = det[4]
                class_id = 0 

            if conf < CONF_THRES:
                continue

            cx, cy, w, h = det[:4]
            x1, y1 = int((cx - w/2 - pad_left) / scale), int((cy - h/2 - pad_top) / scale)
            x2, y2 = int((cx + w/2 - pad_left) / scale), int((cy + h/2 - pad_top) / scale)
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(ow-1, x2), min(oh-1, y2)
            if x2 <= x1 or y2 <= y1: continue
            
            boxes.append([x1, y1, x2 - x1, y2 - y1])
            scores.append(conf)
            class_ids.append(class_id)

        if not boxes: return []
        
        indices = cv2.dnn.NMSBoxes(boxes, scores, CONF_THRES, IOU_THRES)
        if indices is None or len(indices) == 0: return []

        return [Detection(class_ids[i], scores[i], (boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3])) for i in indices.flatten()]

    def detect(self, frame: np.ndarray) -> List[Detection]:
        blob, scale, pad, orig_shape = self._preprocess(frame)
        preds = self.session.run([self.output_name], {self.input_name: blob})[0]
        return self._postprocess(preds, scale, pad, orig_shape)

class DetectionService_Evaluate:
    """
    Dịch vụ phát hiện + phân loại từ ba bộ phân loại (YOLO, CNN, TF-H5).
    """
    def __init__(self, model_path: str, input_size: int):
        self.detector = YoloOnnxDetector(model_path, input_size, is_unified_model=False)
        print("Evaluation service initialized.")

        self.yolo_classifier = YoloClassifier(
            model_path=YOLO_CLASSIFIER_MODEL_PATH,
            input_size=YOLO_CLASSIFIER_INPUT_SIZE,
            conf_thres=YOLO_CLASSIFIER_CONF_THRES,
        )
        self.cnn_classifier = CNNClassifier(
            model_path=CNN_CLASSIFIER_MODEL_PATH,
            input_size=CNN_CLASSIFIER_INPUT_SIZE,
            conf_thres=CNN_CLASSIFIER_CONF_THRES,
        )
        self.h5_classifier = TensorFlowH5Classifier(
            model_path=H5_CLASSIFIER_MODEL_PATH,
            input_size=H5_CLASSIFIER_INPUT_SIZE,
            conf_thres=H5_CLASSIFIER_CONF_THRES,
        )
        os.makedirs(RECEIVED_IMAGES_DIR, exist_ok=True)
        os.makedirs(DETECTION_RESULTS_DIR, exist_ok=True)
        os.makedirs(JSON_RESULTS_DIR, exist_ok=True)

    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Không thể giải mã ảnh từ bytes.")
        ts = datetime.now().strftime("%d-%m-%Y")
        detections = self.detector.detect(frame)
        timestamp = int(time.time())
        original_filename = f"{ts}_{timestamp}_original.jpg"
        cv2.imwrite(os.path.join(RECEIVED_IMAGES_DIR, original_filename), frame)

        result_data: Dict[str, Any] = {
            "original_image": original_filename, "detections_found": len(detections), "results": []
        }

        if detections:
            cropped_images = ImageUtils.crop_from_detections(frame, detections)
            yolo_results = self.yolo_classifier.classify(cropped_images)
            cnn_results = self.cnn_classifier.classify(cropped_images)
            h5_results = self.h5_classifier.classify(cropped_images)

            for i, det in enumerate(detections):
                cropped_filename = f"{ts}_{timestamp}_detection_{i + 1}.jpg"
                cv2.imwrite(os.path.join(DETECTION_RESULTS_DIR, cropped_filename), cropped_images[i])

                yolo_info = {"label": "Unclassified", "confidence": "0.0000"}
                if yolo_results[i]:
                    yolo_info["label"] = YOLO_CLASSIFIER_CLASS_NAMES[yolo_results[i][0]]
                    yolo_info["confidence"] = f"{yolo_results[i][1]:.4f}"

                cnn_info = {"label": "Unclassified", "confidence": "0.0000"}
                if cnn_results[i]:
                    cnn_info["label"] = CNN_CLASSIFIER_CLASS_NAMES[cnn_results[i][0]]
                    cnn_info["confidence"] = f"{cnn_results[i][1]:.4f}"
                
                h5_info = {"label": "Unclassified", "confidence": "0.0000"}
                if h5_results[i]:
                    h5_info["label"] = H5_CLASSIFIER_CLASS_NAMES[h5_results[i][0]]
                    h5_info["confidence"] = f"{h5_results[i][1]:.4f}"

                result_data["results"].append({
                    "detection_box": det.box,
                    "detection_confidence": f"{det.conf:.4f}",
                    "cropped_image_file": cropped_filename,
                    "yolo_classification": yolo_info,
                    "cnn_classification": cnn_info,
                    "h5_classification": h5_info,
                })

        json_filename = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}_results.json"
        json_filepath = os.path.join(JSON_RESULTS_DIR, json_filename)
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        result_data["json_file"] = json_filename
        return result_data

class DetectionService_Production:
    def __init__(self, model_path: str, input_size: int):
        self.detector = YoloOnnxDetector(model_path, input_size, is_unified_model=True)
        print("Production service initialized.")
        os.makedirs(RECEIVED_IMAGES_DIR, exist_ok=True)
        os.makedirs(DETECTION_RESULTS_DIR, exist_ok=True)
        os.makedirs(JSON_RESULTS_DIR, exist_ok=True)

    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Không thể giải mã ảnh từ bytes.")
            
        ts = datetime.now().strftime("%d-%m-%Y")
        detections = self.detector.detect(frame)
        timestamp = int(time.time())
        original_filename = f"{ts}_{timestamp}_original.jpg"
        cv2.imwrite(os.path.join(RECEIVED_IMAGES_DIR, original_filename), frame)

        result_data = {
            "original_image": original_filename, "detections_found": len(detections), "results": []
        }

        if detections:
            cropped_images = ImageUtils.crop_from_detections(frame, detections)
            for i, det in enumerate(detections):
                cropped_filename = f"{ts}_{timestamp}_detection_{i+1}.jpg"
                cv2.imwrite(os.path.join(DETECTION_RESULTS_DIR, cropped_filename), cropped_images[i])
                result_data["results"].append({
                    "cropped_image_file": cropped_filename,
                    "prediction": {
                        "label": YOLO_CLASSIFIER_CLASS_NAMES[det.cls_id],
                        "confidence": f"{det.conf:.4f}",
                        "detection_box": det.box,
                    }
                })

        json_filename = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}_results.json"
        json_filepath = os.path.join(JSON_RESULTS_DIR, json_filename)
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        result_data["json_file"] = json_filename
        return result_data