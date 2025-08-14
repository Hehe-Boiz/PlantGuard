# <<< THAY THẾ TOÀN BỘ FILE NÀY BẰNG PHIÊN BẢN CUỐI CÙNG >>>

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
# class CNNClassifier:
#     def __init__(self, model_path: str, input_size: int, conf_thres: float):
#         """Khởi tạo Classifier cho model CNN."""
#         self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
#         self.input_name = self.session.get_inputs()[0].name
#         self.output_name = self.session.get_outputs()[0].name
#         self.input_size = (input_size, input_size)
#         self.conf_thres = conf_thres
#         print(f"CNN Classifier service initialized with model from {model_path}.")

#     def _preprocess(self, frame: np.ndarray) -> np.ndarray:
#         """
#         Tiền xử lý ảnh cho model CNN.
#         - Resize ảnh về kích thước yêu cầu.
#         - Chuẩn hóa giá trị pixel về [0, 1].
#         - Chuyển đổi BGR sang RGB.
#         - Thay đổi shape từ (H, W, C) sang (1, H, W, C).
#         """
#         resized_image = cv2.resize(frame, self.input_size)
#         image_data = resized_image.astype('float32') / 255.0
#         # Chuyển đổi BGR sang RGB
#         image_data = image_data[:, :, ::-1]
#         # Thêm batch dimension (1, H, W, C)
#         image_data = np.expand_dims(image_data, axis=0)
#         return image_data

#     def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
#         """Hậu xử lý cho model CNN."""
#         scores = preds[0]
#         probabilities = softmax(scores)
        
#         predicted_class_id = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_id]
        
#         if confidence < self.conf_thres:
#             return None
        
#         return int(predicted_class_id), float(confidence)

#     def classify(self, images: List[np.ndarray]) -> List[Optional[Tuple[int, float]]]:
#         """Chạy phân loại trên một danh sách ảnh."""
#         if not images:
#             return []
            
#         results = []
#         for img in images:
#             blob = self._preprocess(img)
#             preds_list = self.session.run([self.output_name], {self.input_name: blob})
#             preds_array = preds_list[0]
#             best_result = self._postprocess(preds_array)
#             results.append(best_result)
            
#         return results

class CNNClassifier:
    def __init__(self, model_path: str, input_size: int, conf_thres: float):
        """Khởi tạo Classifier cho model CNN."""
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_size = (input_size, input_size) # Sẽ là (224, 224) sau khi sửa config
        self.conf_thres = conf_thres
        print(f"CNN Classifier service initialized with model from {model_path}.")

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        --- ĐÃ SỬA LỖI ---
        Tiền xử lý ảnh cho model CNN yêu cầu định dạng NCHW.
        - Resize ảnh về kích thước yêu cầu (224x224).
        - Chuẩn hóa giá trị pixel về [0, 1].
        - Chuyển đổi BGR sang RGB.
        - Thay đổi shape từ (H, W, C) sang (1, C, H, W).
        """
        # Resize ảnh về kích thước model yêu cầu
        resized_image = cv2.resize(frame, self.input_size)
        
        # Chuẩn hóa về [0,1] và đổi BGR to RGB
        image_data = resized_image.astype('float32') / 255.0
        image_data = image_data[:, :, ::-1] # BGR -> RGB
        
        # === PHẦN SỬA LỖI QUAN TRỌNG ===
        # Chuyển từ (H, W, C) sang (C, H, W)
        image_data = np.transpose(image_data, (2, 0, 1))
        
        # Thêm batch dimension để có shape cuối cùng là (1, C, H, W)
        image_data = np.expand_dims(image_data, axis=0)
        
        return image_data

    def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
        """Hậu xử lý cho model CNN."""
        scores = preds[0]
        probabilities = softmax(scores) # Giả định hàm softmax đã được định nghĩa ở đầu file
        
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

        # --- THAY ĐỔI QUAN TRỌNG ---
        # Tự động lấy kích thước input (height, width) từ model đã tải.
        # Ví dụ: model.input_shape có thể là (None, 224, 224, 3)
        # Chúng ta sẽ lấy (224, 224)
        try:
            model_input_shape = self.model.input_shape
            # Lấy chiều cao (vị trí 1) và chiều rộng (vị trí 2)
            self.input_size = (model_input_shape[1], model_input_shape[2])
        except (TypeError, IndexError):
            # Nếu không lấy được, quay lại dùng giá trị từ config
            print("⚠️ Cảnh báo: Không thể tự động xác định input_shape từ model. Sử dụng giá trị từ config.")
            self.input_size = (input_size, input_size)

        print(f"✅ TensorFlow H5 Classifier initialized with model from {model_path}.")
        print(f"   💡 Model expects input size: {self.input_size}") # In ra kích thước thực tế

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Tiền xử lý ảnh cho model .h5."""
        # self.input_size bây giờ là kích thước chính xác (H, W) được lấy từ model
        resized_image = cv2.resize(frame, self.input_size)
        image_data = resized_image.astype('float32') / 255.0
        # Thêm batch dimension để tạo thành tensor (1, H, W, C)
        image_data = np.expand_dims(image_data, axis=0)
        return image_data

    def _postprocess(self, preds: np.ndarray) -> Optional[Tuple[int, float]]:
        """Hậu xử lý cho model .h5."""
        # Kiểm tra nếu preds có nhiều hơn 1 batch (dù predict chỉ chạy 1 ảnh)
        if preds.shape[0] > 1:
            scores = preds[0]
        else:
            scores = preds.flatten() # Làm phẳng mảng (1, num_classes) thành (num_classes,)

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
            # Sử dụng cờ verbose=0 để tắt logging của hàm predict
            preds = self.model.predict(blob, verbose=0)
            best_result = self._postprocess(preds)
            results.append(best_result)
            
        return results