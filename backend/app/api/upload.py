from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any

from app.schemas.video import VideoUploadResponse, VideoMetadata
from app.services.upload_service import UploadService
from app.core.config import settings

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """Uploads a video for deepfake explainability analysis."""
    metadata = await UploadService.save_uploaded_video(file)
    return VideoUploadResponse(
        success=True,
        message="Video uploaded and validated successfully.",
        video=metadata
    )

@router.get("/samples")
def get_sample_videos():
    """Lists preloaded FaceForensics++ benchmark research samples."""
    samples = [
        {
            "sample_key": "000",
            "name": "000.mp4 (FaceForensics++ Original)",
            "ground_truth": "REAL",
            "description": "Authentic pristine target video with natural facial features and temporal continuity.",
            "duration": "15.84s",
            "url": "/storage/samples/000.mp4"
        },
        {
            "sample_key": "000_003",
            "name": "000_003.mp4 (FaceForensics++ FaceSwap)",
            "ground_truth": "FAKE",
            "description": "Manipulated face swap deepfake with source identity 003 transferred onto actor 000.",
            "duration": "15.84s",
            "url": "/storage/samples/000_003.mp4"
        }
    ]
    return {"samples": samples}

@router.post("/sample/{sample_key}", response_model=VideoUploadResponse)
def select_sample_video(sample_key: str):
    """Selects a preloaded sample video for instant analysis."""
    if sample_key not in ("000", "000_003"):
        raise HTTPException(status_code=404, detail=f"Sample '{sample_key}' not found.")
        
    metadata = UploadService.register_sample_video(sample_key)
    return VideoUploadResponse(
        success=True,
        message=f"Sample video '{sample_key}' selected successfully.",
        video=metadata
    )
