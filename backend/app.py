import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from fastapi import FastAPI, WebSocket, Body, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from itertools import count
from fastapi.staticfiles import StaticFiles
import traceback
try:
    from config import (
        UNIFIED_MODEL_PATH,
        UNIFIED_MODEL_INPUT_SIZE,
        DETECTION_MODEL_PATH,
        DETECTION_MODEL_INPUT_SIZE,
    )
    from services.detection_service import (
        DetectionService_Production,
        DetectionService_Evaluate,
    )
    from controllers import detection_controller
    HAVE_DETECTION_STACK = True
except Exception:
    print("!!!!!!!!!!!!!!!!! LỖI KHI KHỞI TẠO CÁC MODULE AI !!!!!!!!!!!!!!!!!")
    traceback.print_exc()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    HAVE_DETECTION_STACK = False

app = FastAPI(title="Tomato Detection API")
app.mount("/static", StaticFiles(directory="../app/data/image"), name="static") 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if HAVE_DETECTION_STACK:
    production_service_instance = DetectionService_Production(
        model_path=UNIFIED_MODEL_PATH,
        input_size=UNIFIED_MODEL_INPUT_SIZE,
    )
    evaluation_service_instance = DetectionService_Evaluate(
        model_path=DETECTION_MODEL_PATH,
        input_size=DETECTION_MODEL_INPUT_SIZE,
    )

    def get_production_service():
        return production_service_instance

    def get_evaluation_service():
        return evaluation_service_instance

    app.dependency_overrides[detection_controller.get_prod_service] = (
        get_production_service
    )
    app.dependency_overrides[detection_controller.get_eval_service] = (
        get_evaluation_service
    )

    app.include_router(detection_controller.router)



@app.get("/")
def read_root():
    return {"message": "Welcome to the Tomato Detection and Classification API."}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_json(self, data):
        to_drop = []
        for ws in self.active_connections:
            try:
                await ws.send_json(data)
            except Exception:
                to_drop.append(ws)
        for ws in to_drop:
            self.disconnect(ws)


manager = ConnectionManager()


class SensorData(BaseModel):
    temperature: float
    humidity: float
    soilMoisture: Optional[float] = None 


@app.post("/api/data")
async def receive_data(data: SensorData):
    await manager.broadcast_json(data.model_dump())
    return {"status": "sent"}


_file_index = count(1)

@app.post("/upload-image/")
async def upload_image(jpeg: bytes = Body(..., media_type="image/jpeg")):
    idx = next(_file_index)
    filename = f"./test_image/test{idx}.jpg"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(jpeg)
    return {"status": "ok", "size": len(jpeg), "file": filename}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
