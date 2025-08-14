import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from fastapi import FastAPI, WebSocket, Body
from config import * 
from services.detection_service import DetectionService_Production, DetectionService_Evaluate
from controllers import detection_controller
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Dependency Injection Setup ---
# 1. Khởi tạo CẢ HAI service một lần duy nhất
production_service_instance = DetectionService_Production(
    model_path=UNIFIED_MODEL_PATH, 
    input_size=UNIFIED_MODEL_INPUT_SIZE 
)
evaluation_service_instance = DetectionService_Evaluate(
    model_path=DETECTION_MODEL_PATH, 
    input_size=DETECTION_MODEL_INPUT_SIZE 
)

# 2. Định nghĩa các hàm sẽ cung cấp service cho controller
def get_production_service():
    return production_service_instance

def get_evaluation_service():
    return evaluation_service_instance

# --- FastAPI App Setup ---
app = FastAPI(title="Tomato Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Ghi đè (override) dependency trong controller bằng các instance đã tạo
app.dependency_overrides[detection_controller.get_prod_service] = get_production_service
app.dependency_overrides[detection_controller.get_eval_service] = get_evaluation_service

# 4. Bao gồm router từ controller vào app chính
app.include_router(detection_controller.router)

# ... (Phần còn lại của file app.py giữ nguyên)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Tomato Detection and Classification API."}

clients: List[WebSocket] = []

index = 0

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.post("/api/data")
async def receive_data(data : SensorData):
    for ws in clients:
        await ws.send_json(data.model_dump())
    return {"status": "sent"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()# giữ kết nối mở
    except:
        clients.remove(websocket)
# @app.post("/upload-image/")
# async def upload_image(jpeg: bytes = Body(..., media_type="image/jpeg")):
#     # Lưu ra file
#     global index
#     index += 1
#     filename = f"./test_image/test{index}.jpg"
#     with open(filename, "wb") as f:
#         f.write(jpeg)
#     return {"status": "ok", "size": len(jpeg)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)