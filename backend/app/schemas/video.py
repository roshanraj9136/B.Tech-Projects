from pydantic import BaseModel, Field
from typing import Optional

class VideoMetadata(BaseModel):
    video_id: str
    original_filename: str
    stored_filename: str
    file_size_bytes: int
    duration_seconds: float
    fps: float
    total_frames: int
    width: int
    height: int
    mime_type: str
    is_sample: bool = False
    sample_key: Optional[str] = None
    created_at: str

class VideoUploadResponse(BaseModel):
    success: bool
    message: str
    video: VideoMetadata
