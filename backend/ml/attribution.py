import math
import numpy as np
import torch
from typing import Tuple, Dict, Any, List

REAL = 0
FAKE = 1
FACE_PARTS = ["lips", "skin", "eyes", "nose"]

def ln_linear_decomp(y_components: torch.Tensor, ln: Any, head: Any) -> Tuple[np.ndarray, float, float]:
    """
    Exact additive decomposition of logit difference:
        d = (head(ln(y))[FAKE] - head(ln(y))[REAL])
    over an additive split y = sum_k y_components[k].
    
    y_components: (K, D) tensor
    Returns: (contribs (K,), const, d_total)
    """
    y_components = y_components.double()
    y = y_components.sum(0)
    D = y.shape[0]

    g = ln.weight.detach().double().cpu()
    b = ln.bias.detach().double().cpu()
    eps = ln.eps

    mu = y.mean()
    var = y.var(unbiased=False)
    sig = torch.sqrt(var + eps)

    W = head.weight.detach().double().cpu()
    bias = head.bias.detach().double().cpu()
    w = W[FAKE] - W[REAL]
    bias_diff = (bias[FAKE] - bias[REAL]).item()

    mu_k = y_components.mean(dim=1, keepdim=True)                 # (K,1)
    centred = y_components - mu_k                                 # (K,D)
    contribs = (centred * (w * g).unsqueeze(0)).sum(dim=1) / sig  # (K,)
    const = (w * b).sum().item() + bias_diff
    d_total = contribs.sum().item() + const
    return contribs.numpy(), const, d_total

def softmax2(d: float) -> float:
    """P(FAKE) for a 2-class logit difference d = logit_fake - logit_real."""
    return 1.0 / (1.0 + math.exp(-d))

def shapley_two_branch(p_s: float, p_t: float, p_full: float, prior: float = 0.5) -> Tuple[float, float]:
    """
    Exact Shapley values of the {spatial, temporal} branch pair:
        v(empty) = prior (0.5)
        v({S})   = p_s (spatial head alone)
        v({T})   = p_t (temporal head alone)
        v({S,T}) = p_full (ensemble)
        
    Efficiency property: phi_s + phi_t = p_full - prior
    """
    phi_s = 0.5 * ((p_s - prior) + (p_full - p_t))
    phi_t = 0.5 * ((p_t - prior) + (p_full - p_s))
    return float(phi_s), float(phi_t)

def compute_component_shares(contrib_parts: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Computes absolute normalized percentage shares and directions for 4 facial components.
    """
    abs_sum = sum(abs(v) for v in contrib_parts.values())
    if abs_sum == 0:
        abs_sum = 1e-9
        
    result = {}
    for part, val in contrib_parts.items():
        share = 100.0 * abs(val) / abs_sum
        direction = "FAKE" if val > 0 else "REAL"
        if share >= 35.0:
            importance = "HIGH"
        elif share >= 15.0:
            importance = "MEDIUM"
        else:
            importance = "LOW"
            
        desc = (
            f"Pushes towards {direction} verdict with {share:.1f}% evidence share "
            f"(signed logit contribution {val:+.3f})."
        )
        result[part] = {
            "name": part,
            "signed_contribution": round(val, 4),
            "normalized_share_pct": round(share, 2),
            "evidence_direction": direction,
            "relative_importance": importance,
            "description": desc
        }
    return result
