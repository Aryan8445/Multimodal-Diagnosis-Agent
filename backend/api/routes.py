from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.pipelines.diagnosis import process_inputs

router = APIRouter()

@router.post("/diagnose")
async def diagnose(blood_report: UploadFile = File(...), xray_image: UploadFile = File(...)):
    try:
        result = await process_inputs(blood_report, xray_image)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
