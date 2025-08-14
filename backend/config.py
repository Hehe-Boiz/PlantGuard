RECEIVED_IMAGES_DIR = "../edge/data/image/received_images"
DETECTION_RESULTS_DIR = "../edge/data/image/detection_results"
JSON_RESULTS_DIR = "../edge/data/image/json_results"

# --- Model chỉ dùng để phát hiện lá (cho /evaluate) ---
DETECTION_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/model/best_segment_leaf.onnx"
DETECTION_MODEL_INPUT_SIZE = 640
CONF_THRES = 0.25
IOU_THRES = 0.45
CLASS_NAMES = ["tomato leaf"]

# --- Model hợp nhất (phát hiện + phân loại) cho /image (production) ---
UNIFIED_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/model/best-model-segmen-benh-v12.onnx"
UNIFIED_MODEL_INPUT_SIZE = 256

# --- CẤU HÌNH CHO MODEL CLASSIFICATION (YOLO-Classify) ---
# THAY ĐỔI CÁC GIÁ TRỊ NÀY CHO PHÙ HỢP VỚI BẠN
# Model này sẽ chạy trên các ảnh đã được cắt ra từ model detection
YOLO_CLASSIFIER_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/model/best_class_YOLO.onnx" 
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
] 

CNN_CLASSIFIER_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/model/resnet50_finetuned_plant_disease.onnx" 
CNN_CLASSIFIER_INPUT_SIZE = 224 # THAY ĐỔI: Kích thước ảnh đầu vào cho model CNN
CNN_CLASSIFIER_CONF_THRES = 0.20 # THAY ĐỔI: Ngưỡng tin cậy cho model CNN
CNN_CLASSIFIER_CLASS_NAMES = [
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
] 

H5_CLASSIFIER_MODEL_PATH = "/home/heheboiz/data/PlantGuard/edge/model/cnn_model_classification.h5" # 👈 THAY ĐỔI: Đường dẫn đến file .h5 của bạn
H5_CLASSIFIER_INPUT_SIZE = 256 # THAY ĐỔI: Kích thước ảnh đầu vào cho model .h5
H5_CLASSIFIER_CONF_THRES = 0.20 # THAY ĐỔI: Ngưỡng tin cậy cho model .h5
H5_CLASSIFIER_CLASS_NAMES = [
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
]