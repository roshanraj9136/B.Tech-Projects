from fastapi import APIRouter
import torch
import cv2
import sys
from app.core.config import settings
from ml.model_loader import model_loader

router = APIRouter(tags=["Health"])

@router.get("/health")
def get_health_status():
    status_info = model_loader.get_status()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "python_version": sys.version.split()[0],
        "torch_version": torch.__version__,
        "opencv_version": cv2.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device": status_info.get("device", "cpu"),
        "remote_gpu_worker": {
            "configured": bool(settings.COLAB_GPU_URL),
            "endpoint": settings.COLAB_GPU_URL
        },
        "checkpoint_status": {
            "checkpoint_present": status_info.get("checkpoint_present", False),
            "weights_path": status_info.get("weights_path"),
            "model_loaded": status_info.get("model_loaded", False),
            "message": status_info.get("message")
        },
        "thresholds": {
            "authentic": settings.THRESHOLD_AUTHENTIC,
            "manipulated": settings.THRESHOLD_MANIPULATED
        }
    }
