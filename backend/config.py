# backend/app/config.py
MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/data/best.onnx" # Đường dẫn trên server
INPUT_SIZE = 640
CONF_THRES = 0.25
IOU_THRES = 0.45
CLASS_NAMES = ["tomato leaf"]
RECEIVED_IMAGES_DIR = "received_images"
DETECTION_RESULTS_DIR = "detection_results"

# --- CẤU HÌNH CHO MODEL CLASSIFICATION (YOLO-Classify) ---
# THAY ĐỔI CÁC GIÁ TRỊ NÀY CHO PHÙ HỢP VỚI BẠN
# Model này sẽ chạy trên các ảnh đã được cắt ra từ model detection
YOLO_CLASSIFIER_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/data/best_class_YOLO.onnx" # 👈 THAY ĐỔI: Đường dẫn đến file .onnx của YOLO phân loại
YOLO_CLASSIFIER_INPUT_SIZE = 256 # THAY ĐỔI: Kích thước ảnh đầu vào cho YOLO phân loại (ví dụ: 320, 640)
YOLO_CLASSIFIER_CONF_THRES = 0.20 # THAY ĐỔI: Ngưỡng tin cậy cho YOLO phân loại
YOLO_CLASSIFIER_IOU_THRES = 0.45 # THAY ĐỔI: Ngưỡng IOU cho YOLO phân loại
YOLO_CLASSIFIER_CLASS_NAMES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
] # THAY ĐỔI: Danh sách tên các lớp bệnh
