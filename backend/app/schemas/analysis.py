from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProcessingStage(BaseModel):
    id: str
    name: str
    status: str # "pending", "in_progress", "completed", "failed"
    progress: int # 0 to 100
    message: Optional[str] = None

class AnalysisStatus(BaseModel):
    analysis_id: str
    video_id: str
    status: str # "queued", "processing", "completed", "failed"
    current_stage: str
    progress: int
    stages: List[ProcessingStage]
    elapsed_seconds: float
    error_message: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

class Probabilities(BaseModel):
    final_mean: float
    final_std: float
    p_fake: float
    p_real: float
    spatial_mean: float
    temporal_mean: float
    fusion_mean: float

class BranchShapley(BaseModel):
    pct_spatial: float
    pct_temporal: float
    phi_spatial: float
    phi_temporal: float
    dominant_branch: str
    explanation: str

class FacialComponentDetail(BaseModel):
    name: str
    signed_contribution: float
    normalized_share_pct: float
    evidence_direction: str # "FAKE" or "REAL"
    relative_importance: str # "HIGH", "MEDIUM", "LOW"
    description: str

class FacialComponentsReport(BaseModel):
    components: Dict[str, FacialComponentDetail]
    dominant_component: str
    interpretation: str

class RegionDetail(BaseModel):
    name: str
    patch_count: int
    signed: Optional[float] = 0.0
    share_pct: Optional[float] = 0.0
    spatial_signed: Optional[float] = 0.0
    spatial_share_pct: Optional[float] = 0.0
    temporal_signed: Optional[float] = 0.0
    temporal_share_pct: Optional[float] = 0.0
    density: Optional[float] = 0.0

class FacialRegionsReport(BaseModel):
    regions: Dict[str, RegionDetail]
    dominant_spatial_region: str
    dominant_temporal_region: str
    grid_size: int = 16
    patch_spatial_attributions: Optional[List[List[float]]] = None
    patch_temporal_attributions: Optional[List[List[float]]] = None
    face_crop_url: Optional[str] = None
    heatmap_spatial_url: Optional[str] = None
    heatmap_temporal_url: Optional[str] = None

class ClipDetail(BaseModel):
    clip_index: int
    start_frame: int
    end_frame: int
    start_timestamp_s: float
    end_timestamp_s: float
    p_final: float
    p_real: float
    verdict: str
    pct_spatial: float
    pct_temporal: float
    phi_spatial: float
    phi_temporal: float

class FrameInspectionDetail(BaseModel):
    frame_index: int
    timestamp_s: float
    face_detected: bool
    face_crop_url: Optional[str] = None
    landmark_count: int
    p_fake: float
    dominant_part: str
    components: Dict[str, float]

class VideoQualityReport(BaseModel):
    resolution: str
    fps: float
    duration_s: float
    total_frames: int
    blur_score: float # Laplacian variance
    blur_assessment: str # "Crisp", "Acceptable", "Blurry"
    compression_warning: bool
    compression_level: str # "Low", "Moderate", "High"
    face_detection_consistency: float # percentage of frames with detected face
    lighting_warning: bool
    lighting_assessment: str # "Well-lit", "Underexposed", "Overexposed"
    quality_notes: List[str]

class OverallVerdict(BaseModel):
    verdict: str # "LIKELY AUTHENTIC", "LIKELY MANIPULATED", "INCONCLUSIVE"
    p_fake: float
    p_real: float
    threshold_authentic: float
    threshold_manipulated: float
    n_clips_analyzed: int
    video_duration_s: float
    processing_time_s: float
    model_architecture: str = "DFD-FCG (CLIP ViT-L/14 + FCG)"
    checkpoint_status: str

class AnalysisResult(BaseModel):
    analysis_id: str
    video_id: str
    filename: str
    created_at: str
    verdict: OverallVerdict
    branch_analysis: BranchShapley
    facial_components: FacialComponentsReport
    facial_regions: FacialRegionsReport
    clips: List[ClipDetail]
    frames: List[FrameInspectionDetail]
    quality_report: VideoQualityReport
    final_explanation: str
    research_citations: List[str]
    report_pdf_url: str
