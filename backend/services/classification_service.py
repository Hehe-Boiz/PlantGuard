import cv2
import numpy as np
import onnxruntime as ort
from typing import List, Tuple, Optional
import tensorflow as tf

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
        scores = preds[0]
        
        probabilities = softmax(scores)
        
        predicted_class_id = np.argmax(probabilities)
        confidence = probabilities[predicted_class_id]
        
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
            preds_list = self.session.run([self.output_name], {self.input_name: blob})
            preds_array = preds_list[0]
            best_result = self._postprocess(preds_array)
            results.append(best_result)
            
        return results

class CNNClassifier:
    def __init__(self, model_path: str, input_size: int, conf_thres: float):
        """Khởi tạo Classifier cho model CNN."""
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_size = (input_size, input_size) 
        self.conf_thres = conf_thres
        print(f"CNN Classifier service initialized with model from {model_path}.")

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Tiền xử lý ảnh cho model CNN yêu cầu định dạng NCHW.
        - Resize ảnh về kích thước yêu cầu (224x224).
        - Chuẩn hóa giá trị pixel về [0, 1].
        - Chuyển đổi BGR sang RGB.
        - Thay đổi shape từ (H, W, C) sang (1, C, H, W).
        """
        resized_image = cv2.resize(frame, self.input_size)
        
        image_data = resized_image.astype('float32') / 255.0
        image_data = image_data[:, :, ::-1] 
        
        image_data = np.transpose(image_data, (2, 0, 1))
        
        image_data = np.expand_dims(image_data, axis=0)
        
        return image_data

    def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
        """Hậu xử lý cho model CNN."""
        scores = preds[0]
        probabilities = softmax(scores) 
        
        predicted_class_id = np.argmax(probabilities)
        confidence = probabilities[predicted_class_id]
        
        if confidence < self.conf_thres:
            return None
        
        return int(predicted_class_id), float(confidence)

    def classify(self, images: List[np.ndarray]) -> List[Optional[Tuple[int, float]]]:
        """Chạy phân loại trên một danh sách ảnh."""
        if not images:
            return []
            
        results = []
        for img in images:
            blob = self._preprocess(img)
            preds_list = self.session.run([self.output_name], {self.input_name: blob})
            preds_array = preds_list[0]
            best_result = self._postprocess(preds_array)
            results.append(best_result)
            
        return results
class TensorFlowH5Classifier:
    def __init__(self, model_path: str, input_size: int, conf_thres: float):
        """
        Khởi tạo Classifier cho model TensorFlow .h5.
        `input_size` từ config sẽ được bỏ qua và thay bằng kích thước thực tế từ model.
        """
        self.model = tf.keras.models.load_model(model_path)
        self.conf_thres = conf_thres

        try:
            model_input_shape = self.model.input_shape
            self.input_size = (model_input_shape[1], model_input_shape[2])
        except (TypeError, IndexError):
            print("⚠️ Cảnh báo: Không thể tự động xác định input_shape từ model. Sử dụng giá trị từ config.")
            self.input_size = (input_size, input_size)

        print(f"✅ TensorFlow H5 Classifier initialized with model from {model_path}.")
        print(f"   💡 Model expects input size: {self.input_size}")

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Tiền xử lý ảnh cho model .h5."""
        resized_image = cv2.resize(frame, self.input_size)
        image_data = resized_image.astype('float32') / 255.0
        image_data = np.expand_dims(image_data, axis=0)
        return image_data

    def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
        """Hậu xử lý cho model .h5."""
        
        if preds.shape[0] > 1:
            scores = preds[0]
        else:
            scores = preds.flatten() 

        probabilities = softmax(scores)
        predicted_class_id = np.argmax(probabilities)
        confidence = probabilities[predicted_class_id]
        
        if confidence < self.conf_thres:
            return None
            
        return int(predicted_class_id), float(confidence)

    def classify(self, images: List[np.ndarray]) -> List[Optional[Tuple[int, float]]]:
        """Chạy phân loại trên một danh sách ảnh."""
        if not images:
            return []
            
        results = []
        for img in images:
            blob = self._preprocess(img)
            preds = self.model.predict(blob, verbose=0)
            best_result = self._postprocess(preds)
            results.append(best_result)
            
        return results