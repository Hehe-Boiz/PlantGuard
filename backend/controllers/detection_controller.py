from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any

def get_prod_service() -> Any:
    pass

def get_eval_service() -> Any:
    pass

router = APIRouter(
    prefix="/detect",
    tags=["Detection"]
)

@router.post("/image", summary="Run production model (unified)")
async def detect_image_production(
    image_bytes: bytes = Body(..., media_type="image/jpeg"),
    service = Depends(get_prod_service) 
):
    """
    Endpoint chính: Sử dụng model hợp nhất để phát hiện và phân loại.
    """
    try:
        results = service.process_image(image_bytes)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate", summary="Run evaluation models (1 detect + 3 classify)")
async def detect_image_evaluation(
    image_bytes: bytes = Body(..., media_type="image/jpeg"),
    service = Depends(get_eval_service)
):
    """
    Endpoint đánh giá: Sử dụng 1 model phát hiện và 3 model phân loại để so sánh.
    """
    try:
        results = service.process_image(image_bytes)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))