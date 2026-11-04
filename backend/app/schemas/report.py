from pydantic import BaseModel
from typing import Optional, Any, Dict

class DownloadReportResponse(BaseModel):
    analysis_id: str
    filename: str
    file_path: str
    content_type: str = "application/pdf"
