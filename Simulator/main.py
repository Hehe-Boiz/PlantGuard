from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients: List[WebSocket] = []

class SensorData(BaseModel):
    temperature: float
    humidity: float
    wind: float
    soilMoisture: float
    pH: float

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)