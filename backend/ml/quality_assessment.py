import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

def assess_video_quality(frames: List[np.ndarray], fps: float, width: int, height: int, detected_face_flags: List[bool]) -> Dict[str, Any]:
    """
    Evaluates video quality independently of deepfake manipulation probability.
    Inspects: Blur (Laplacian variance), Compression artifacts, Illumination/lighting,
    Resolution, FPS, and Face Detection consistency.
    """
    if not frames:
        return {
            "resolution": f"{width}x{height}",
            "fps": fps,
            "duration_s": 0.0,
            "total_frames": 0,
            "blur_score": 0.0,
            "blur_assessment": "Unknown",
            "compression_warning": False,
            "compression_level": "Unknown",
            "face_detection_consistency": 0.0,
            "lighting_warning": False,
            "lighting_assessment": "Unknown",
            "quality_notes": ["No frames provided for quality assessment."]
        }
    
    n_frames = len(frames)
    duration_s = n_frames / max(fps, 1.0)
    
    # 1. Blur Assessment via Laplacian Variance
    laplacian_vars = []
    brightnesses = []
    
    # Sample up to 30 evenly spaced frames for fast yet accurate metrics
    sample_indices = np.linspace(0, n_frames - 1, min(n_frames, 30), dtype=int)
    for idx in sample_indices:
        fr = frames[idx]
        gray = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY) if len(fr.shape) == 3 else fr
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        laplacian_vars.append(lap_var)
        brightnesses.append(float(np.mean(gray)))
        
    avg_blur_score = float(np.mean(laplacian_vars)) if laplacian_vars else 0.0
    if avg_blur_score < 70.0:
        blur_assessment = "Blurry"
        blur_note = f"Low sharpness detected (Laplacian variance {avg_blur_score:.1f} < 70). Motion or optical blur may degrade forensic confidence."
    elif avg_blur_score < 180.0:
        blur_assessment = "Acceptable"
        blur_note = f"Moderate sharpness (Laplacian variance {avg_blur_score:.1f})."
    else:
        blur_assessment = "Crisp"
        blur_note = f"High image sharpness (Laplacian variance {avg_blur_score:.1f}). Fine facial textures preserved."
        
    # 2. Lighting & Exposure
    avg_brightness = float(np.mean(brightnesses)) if brightnesses else 128.0
    lighting_warning = False
    if avg_brightness < 45.0:
        lighting_assessment = "Underexposed"
        lighting_warning = True
        lighting_note = f"Dark scene (mean luminance {avg_brightness:.1f}/255). Facial landmarks may be obscured."
    elif avg_brightness > 215.0:
        lighting_assessment = "Overexposed"
        lighting_warning = True
        lighting_note = f"Overexposed scene (mean luminance {avg_brightness:.1f}/255). Specular highlights may mimic synthesis artifacts."
    else:
        lighting_assessment = "Well-lit"
        lighting_note = f"Balanced lighting (mean luminance {avg_brightness:.1f}/255)."

    # 3. Face Detection Consistency
    if detected_face_flags:
        face_consistency = float(np.mean(detected_face_flags) * 100.0)
    else:
        face_consistency = 100.0
        
    # 4. Compression Warning (based on resolution and blockiness heuristic)
    compression_warning = False
    if width < 480 or height < 480:
        compression_level = "High"
        compression_warning = True
        comp_note = f"Low input resolution ({width}x{height}). Heavy downscaling or compression present."
    elif width < 720:
        compression_level = "Moderate"
        comp_note = f"Standard definition video ({width}x{height})."
    else:
        compression_level = "Low"
        comp_note = f"High definition video ({width}x{height})."

    quality_notes = [blur_note, lighting_note, comp_note]
    if face_consistency < 75.0:
        quality_notes.append(f"Face tracking intermittent ({face_consistency:.1f}% frames tracked). Video contains rapid turns or occlusions.")
    
    return {
        "resolution": f"{width}x{height}",
        "fps": round(float(fps), 2),
        "duration_s": round(float(duration_s), 2),
        "total_frames": int(n_frames),
        "blur_score": round(avg_blur_score, 2),
        "blur_assessment": blur_assessment,
        "compression_warning": compression_warning,
        "compression_level": compression_level,
        "face_detection_consistency": round(face_consistency, 1),
        "lighting_warning": lighting_warning,
        "lighting_assessment": lighting_assessment,
        "quality_notes": quality_notes
    }
