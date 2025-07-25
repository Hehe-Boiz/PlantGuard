from fastapi import APIRouter, Body, Depends
from services.detection_service import DetectionService

# Hàm này vẫn giữ nguyên, FastAPI sẽ sử dụng nó để inject service
def get_detection_service():
    pass

router = APIRouter(
    prefix="/detect",
    tags=["Detection"]
)

@router.post("/image")
async def detect_image_from_upload(
    image_bytes: bytes = Body(..., media_type="image/jpeg"),
    service: DetectionService = Depends(get_detection_service) 
):
    results = service.process_image(image_bytes)
    return results