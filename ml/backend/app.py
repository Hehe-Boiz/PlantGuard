import os
from fastapi import FastAPI, WebSocket, Body
from contextlib import asynccontextmanager
from config import MODEL_PATH, INPUT_SIZE, RECEIVED_IMAGES_DIR, DETECTION_RESULTS_DIR
from services.detection_service import DetectionService
from controllers import detection_controller
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncio

# --- Tạo thư mục nếu chưa tồn tại ---
os.makedirs(RECEIVED_IMAGES_DIR, exist_ok=True)
os.makedirs(DETECTION_RESULTS_DIR, exist_ok=True)

# --- Dependency Injection Setup ---
# 1. Khởi tạo service một lần duy nhất
detection_service_instance = DetectionService(MODEL_PATH, INPUT_SIZE)

# 2. Định nghĩa hàm sẽ cung cấp service cho controller
def get_service():
    return detection_service_instance

# --- FastAPI App Setup ---
app = FastAPI(title="Tomato Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Ghi đè (override) dependency trong controller bằng instance đã tạo
app.dependency_overrides[detection_controller.get_detection_service] = get_service

# 4. Bao gồm router từ controller vào app chính
app.include_router(detection_controller.router)

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