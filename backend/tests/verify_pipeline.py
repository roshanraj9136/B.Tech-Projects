import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.services.upload_service import UploadService
from app.services.analysis_service import AnalysisService
from app.core.config import settings

def main():
    print("Testing end-to-end video deepfake forensic analysis pipeline...")
    
    # 1. Register sample 000_003 (Manipulated FaceForensics++ benchmark)
    print("Registering sample video '000_003'...")
    meta = UploadService.register_sample_video("000_003")
    print(f"Video registered: {meta.video_id} ({meta.duration_seconds}s, {meta.fps} FPS, {meta.width}x{meta.height})")
    
    # 2. Create analysis job
    analysis_id = AnalysisService.create_analysis_job(meta.video_id, sample_key="000_003")
    print(f"Analysis job started: {analysis_id}")
    
    # 3. Wait for background worker to complete
    max_wait = 30
    start = time.time()
    while time.time() - start < max_wait:
        status = AnalysisService.get_analysis_status(analysis_id)
        print(f"  Stage: {status.current_stage} | Progress: {status.progress}% | Elapsed: {status.elapsed_seconds}s")
        if status.status in ("completed", "failed"):
            break
        time.sleep(1)
        
    assert status.status == "completed", f"Analysis failed or timed out: {status.error_message}"
    print("\nAnalysis completed successfully!")
    
    # 4. Fetch full result
    result = AnalysisService.get_analysis_result(analysis_id)
    verdict = result["verdict"]
    print(f"VERDICT: {verdict['verdict']}")
    print(f"P(FAKE): {verdict['p_fake']:.3f} | P(REAL): {verdict['p_real']:.3f}")
    print(f"Spatial Share: {result['branch_analysis']['pct_spatial']}% | Temporal Share: {result['branch_analysis']['pct_temporal']}%")
    print(f"Dominant Facial Component: {result['facial_components']['dominant_component']}")
    print(f"PDF Report Path: {settings.REPORTS_DIR / f'{analysis_id}.pdf'}")
    
    # Check if PDF exists and has non-zero size
    pdf_path = settings.REPORTS_DIR / f"{analysis_id}.pdf"
    assert pdf_path.exists() and pdf_path.stat().st_size > 5000, f"PDF report missing or too small: {pdf_path}"
    print(f"PDF verified: {pdf_path.stat().st_size} bytes")
    
    # Check heatmaps
    spatial_hm = settings.HEATMAPS_DIR / f"{analysis_id}_spatial_hm.png"
    temporal_hm = settings.HEATMAPS_DIR / f"{analysis_id}_temporal_hm.png"
    assert spatial_hm.exists(), "Spatial heatmap missing"
    assert temporal_hm.exists(), "Temporal heatmap missing"
    print("Heatmaps verified!")
    print("\nPIPELINE VERIFICATION PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
