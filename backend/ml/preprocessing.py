import math
import cv2
import numpy as np
import torch
from pathlib import Path
from typing import List, Tuple, Optional

# CLIP ViT-L/14 standard normalization constants
CLIP_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
CLIP_STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)

def read_video_frames(video_path: Path, max_frames: Optional[int] = None) -> Tuple[List[np.ndarray], float, int, int]:
    """
    Reads video frames using OpenCV in RGB format.
    Returns: (frames_list, fps, width, height)
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or math.isnan(fps):
        fps = 25.0
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frames = []
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
        count += 1
        if max_frames and count >= max_frames:
            break
            
    cap.release()
    if not frames:
        raise RuntimeError(f"No frames could be decoded from {video_path}")
        
    return frames, float(fps), width, height

def compute_clip_indices(
    n_frames: int,
    fps: float,
    num_frames: int = 10,
    stride: float = 0.333,
    max_clips: Optional[int] = 30
) -> Tuple[List[int], List[int]]:
    """
    Calculates frame offsets and clip start indices matching the upstream DFD-FCG protocol:
    Frame offsets = floor(i * stride * fps) for i in 0..num_frames-1 (approx 3-second window).
    """
    offsets = [int(math.floor(i * stride * fps)) for i in range(num_frames)]
    max_offset = offsets[-1]
    
    n_possible_clips = n_frames - max_offset
    if n_possible_clips <= 0:
        # Fallback if video is very short: adjust stride to fit
        if n_frames >= num_frames:
            step = (n_frames - 1) / (num_frames - 1)
            offsets = [int(math.floor(i * step)) for i in range(num_frames)]
            starts = [0]
            return offsets, starts
        else:
            raise RuntimeError(f"Video is too short ({n_frames} frames). Minimum {num_frames} frames required.")

    all_starts = list(range(n_possible_clips))
    if max_clips and len(all_starts) > max_clips:
        # Evenly spaced subset across the video
        indices = np.linspace(0, len(all_starts) - 1, max_clips).round().astype(int)
        selected_starts = [all_starts[i] for i in sorted(set(indices.tolist()))]
    else:
        selected_starts = all_starts
        
    return offsets, selected_starts

def preprocess_face_for_clip(face_crop_150: np.ndarray, target_size: int = 224) -> torch.Tensor:
    """
    Resizes 150x150 face crop to 224x224 and normalizes with CLIP mean/std.
    Returns: Tensor of shape (3, 224, 224)
    """
    resized = cv2.resize(face_crop_150, (target_size, target_size), interpolation=cv2.INTER_LINEAR)
    arr = resized.astype(np.float32) / 255.0
    normalized = (arr - CLIP_MEAN) / CLIP_STD
    tensor = torch.from_numpy(normalized).permute(2, 0, 1).contiguous()
    return tensor
