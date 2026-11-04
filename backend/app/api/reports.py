from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import AnalysisNotFoundError
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{analysis_id}/download")
def download_pdf_report(analysis_id: str):
    """Downloads the generated forensic PDF report for an analysis."""
    pdf_path = settings.REPORTS_DIR / f"{analysis_id}.pdf"
    
    if not pdf_path.exists():
        # Check if result exists, then regenerate PDF
        try:
            result = AnalysisService.get_analysis_result(analysis_id)
            ReportService.generate_pdf_report(result, pdf_path)
        except Exception:
            raise AnalysisNotFoundError(analysis_id)
            
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF report could not be generated.")
        
    return FileResponse(
        path=str(pdf_path),
        filename=f"Forensic_Deepfake_Report_{analysis_id[:8]}.pdf",
        media_type="application/pdf"
    )
