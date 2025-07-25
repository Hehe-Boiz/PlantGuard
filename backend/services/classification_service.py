# <<< THAY THẾ TOÀN BỘ FILE NÀY BẰNG PHIÊN BẢN CUỐI CÙNG >>>

import cv2
import numpy as np
import onnxruntime as ort
from typing import List, Tuple, Optional

def softmax(x):
    """Tính softmax để chuyển đổi scores thành xác suất."""
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)

class YoloClassifier:
    def __init__(self, model_path: str, input_size: int, conf_thres: float):
        """
        Khởi tạo Classifier.
        """
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_size = input_size
        self.conf_thres = conf_thres
        print(f"YOLO Classifier service initialized with model from {model_path}.")

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Tiền xử lý ảnh với letterbox padding."""
        h, w = frame.shape[:2]
        scale = self.input_size / max(h, w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(frame, (nw, nh))
        
        canvas = np.full((self.input_size, self.input_size, 3), 114, dtype=np.uint8)
        pad_top = (self.input_size - nh) // 2
        pad_left = (self.input_size - nw) // 2
        canvas[pad_top:pad_top + nh, pad_left:pad_left + nw] = resized
        
        return cv2.dnn.blobFromImage(canvas, 1/255.0, (self.input_size, self.input_size), swapRB=True, crop=False)

    def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
        """
        Hậu xử lý cho model trả về một mảng scores (shape: 1x10).
        Đây là phiên bản chính xác cuối cùng.
        """
        # `preds` có shape (1, 10), ta lấy mảng 10 scores bên trong.
        scores = preds[0]
        
        # Chuyển đổi scores thành xác suất bằng softmax
        probabilities = softmax(scores)
        
        # Tìm lớp có xác suất cao nhất
        predicted_class_id = np.argmax(probabilities)
        confidence = probabilities[predicted_class_id]
        
        # Áp dụng ngưỡng tin cậy
        if confidence < self.conf_thres:
            return None
        
        return int(predicted_class_id), float(confidence)

    def classify(self, images: List[np.ndarray]) -> List[Optional[Tuple[int, float]]]:
        """
        Khôi phục lại hàm classify chuẩn.
        """
        if not images:
            return []
            
        results = []
        for img in images:
            blob = self._preprocess(img)
            # Đầu ra của session.run là một list, ta lấy phần tử đầu tiên
            preds_list = self.session.run([self.output_name], {self.input_name: blob})
            preds_array = preds_list[0]
            best_result = self._postprocess(preds_array)
            results.append(best_result)
            
        return results