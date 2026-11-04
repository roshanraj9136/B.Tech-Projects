# Video Deepfake Detection — Model Checkpoint Guide

This platform integrates the state-of-the-art **DFD-FCG** (CVPR 2025) video deepfake detector built on a frozen CLIP ViT-L/14 foundation model with Facial Component Guidance.

## Required Checkpoint Files

Place the following files in this `checkpoint/` directory:
- `checkpoint/weights.ckpt` — Released model weights (~1.2 GB)
- `checkpoint/setting.yaml` — Model architecture and hyperparameter settings

## Authorized Download Source

The official checkpoint is released by the DFD-FCG research authors (Academia Sinica, NTUST, Microsoft, NTU):
- **Official Google Drive Download**: [DFD-FCG Model Checkpoint (weights.ckpt)](https://drive.google.com/file/d/1ydD5rnaaF0i2zLE7NidLtAhjonHoVQOk/view?usp=sharing)
- **Official Paper (CVPR 2025)**: [arXiv:2404.05583](https://arxiv.org/abs/2404.05583)
- **Upstream Repository**: [https://github.com/aiiu-lab/DFD-FCG](https://github.com/aiiu-lab/DFD-FCG)
- **Explainability Research**: [https://github.com/roshanraj9136/dfd-fcg-explainability](https://github.com/roshanraj9136/dfd-fcg-explainability)

## Setup Steps

1. Download `weights.ckpt` from the link above.
2. Move `weights.ckpt` to:
   ```bash
   checkpoint/weights.ckpt
   ```
3. Copy or create `setting.yaml` (already preconfigured in `backend/` configs).
4. Restart the FastAPI backend or trigger the `/api/health` check to verify that `checkpoint_present: true` and the model is initialized.

## Offline / Demo Mode Support

If the checkpoint is not yet downloaded:
- The platform runs in forensic fallback & research audit mode.
- Complete audit results and exact Shapley attributions for the FaceForensics++ benchmark samples (`000.mp4` Pristine Authentic, `000_003.mp4` Face-Swapped Manipulated) are bundled and ready to inspect immediately.
- New video uploads will be evaluated using forensic quality assessment, face tracking, and landmark regional mapping with clear indicators that model weights must be placed for live neural inference.
