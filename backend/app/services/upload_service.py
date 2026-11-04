import uuid
import time
import shutil
from pathlib import Path
from fastapi import UploadFile
from typing import Optional

from app.core.config import settings
from app.core.exceptions import InvalidVideoFormatError, FileTooLargeError
from app.schemas.video import VideoMetadata
from ml.preprocessing import read_video_frames

class UploadService:
    @staticmethod
    async def save_uploaded_video(file: UploadFile) -> VideoMetadata:
        # Validate extension
        filename = file.filename or "video.mp4"
        ext = Path(filename).suffix.lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise InvalidVideoFormatError(
                f"File format '{ext}' not supported. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )

        video_id = str(uuid.uuid4())
        safe_filename = f"{video_id}{ext}"
        destination = settings.UPLOADS_DIR / safe_filename

        # Write to disk checking file size
        total_bytes = 0
        with open(destination, "wb") as buffer:
            while chunk := await file.read(1024 * 1024): # 1MB chunks
                total_bytes += len(chunk)
                if total_bytes > settings.MAX_UPLOAD_SIZE:
                    buffer.close()
                    if destination.exists():
                        destination.unlink()
                    raise FileTooLargeError(max_size_mb=settings.MAX_UPLOAD_SIZE // (1024 * 1024))
                buffer.write(chunk)

        # Inspect video metadata with OpenCV
        try:
            frames, fps, width, height = read_video_frames(destination, max_frames=2)
            # Duration via cap
            import cv2
            cap = cv2.VideoCapture(str(destination))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            duration_s = total_frames / max(fps, 1.0)
        except Exception as e:
            if destination.exists():
                destination.unlink()
            raise InvalidVideoFormatError(f"Uploaded file could not be parsed as a valid video: {str(e)}")

        return VideoMetadata(
            video_id=video_id,
            original_filename=filename,
            stored_filename=safe_filename,
            file_size_bytes=total_bytes,
            duration_seconds=round(duration_s, 2),
            fps=round(fps, 2),
            total_frames=total_frames,
            width=width,
            height=height,
            mime_type=file.content_type or "video/mp4",
            is_sample=False,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

    @staticmethod
    def register_sample_video(sample_key: str) -> VideoMetadata:
        """Registers bundled FaceForensics++ benchmark sample video."""
        sample_path = settings.SAMPLES_DIR / f"{sample_key}.mp4"
        if not sample_path.exists():
            raise InvalidVideoFormatError(f"Sample video '{sample_key}.mp4' not found in {settings.SAMPLES_DIR}")
            
        import cv2
        cap = cv2.VideoCapture(str(sample_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        video_id = f"sample_{sample_key}"
        file_size = sample_path.stat().st_size
        
        return VideoMetadata(
            video_id=video_id,
            original_filename=f"{sample_key}.mp4",
            stored_filename=f"{sample_key}.mp4",
            file_size_bytes=file_size,
            duration_seconds=round(total_frames / max(fps, 1.0), 2),
            fps=round(fps, 2),
            total_frames=total_frames,
            width=width,
            height=height,
            mime_type="video/mp4",
            is_sample=True,
            sample_key=sample_key,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
