RECEIVED_IMAGES_DIR = "/app/data/image/received_images"
DETECTION_RESULTS_DIR = "/app/data/image/detection_results"
JSON_RESULTS_DIR = "/app/data/image/json_results"

# --- Model chỉ dùng để phát hiện lá (cho /evaluate) ---
DETECTION_MODEL_PATH = "/app/model/best_segment_leaf.onnx"
DETECTION_MODEL_INPUT_SIZE = 640
CONF_THRES = 0.25
IOU_THRES = 0.45
CLASS_NAMES = ["tomato leaf"]

# --- Model hợp nhất (phát hiện + phân loại) cho /image (production) ---
UNIFIED_MODEL_PATH = "/app/model/best-model-segmen-benh-v12.onnx"
UNIFIED_MODEL_INPUT_SIZE = 256

# --- CẤU HÌNH CHO MODEL CLASSIFICATION (YOLO-Classify) ---
YOLO_CLASSIFIER_MODEL_PATH = "/app/model/best_class_YOLO.onnx" 
YOLO_CLASSIFIER_INPUT_SIZE = 256
YOLO_CLASSIFIER_CONF_THRES = 0.20
YOLO_CLASSIFIER_IOU_THRES = 0.45
YOLO_CLASSIFIER_CLASS_NAMES = [
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
] 

CNN_CLASSIFIER_MODEL_PATH = "/app/model/resnet50_finetuned_plant_disease.onnx" 
CNN_CLASSIFIER_INPUT_SIZE = 224
CNN_CLASSIFIER_CONF_THRES = 0.20
CNN_CLASSIFIER_CLASS_NAMES = [
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
] 

H5_CLASSIFIER_MODEL_PATH = "/app/model/cnn_model_classification.h5" 
H5_CLASSIFIER_INPUT_SIZE = 256
H5_CLASSIFIER_CONF_THRES = 0.20
H5_CLASSIFIER_CLASS_NAMES = [
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
]