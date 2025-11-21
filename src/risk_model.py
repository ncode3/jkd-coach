from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

import pandas as pd

@dataclass
class RoundVideoStats:
    round_id: str
    total_frames: int
    pose_frames: int
    pose_coverage: float
    guard_down_ratio: float
    avg_left_guard_height: float
    avg_right_guard_height: float
    avg_hip_rotation: float
    avg_stance_width: float
    avg_head_y: float

def video_form_and_danger(stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pure function used both in the notebook and later in the API.

    Input: dict with round-level video stats.
    Output: same dict plus video_danger_score, video_form_score, video_focus_next_round.
    """
    guard_down = stats.get("guard_down_ratio", 0.0)
    pose_cov   = stats.get("pose_coverage", 0.0)

    # Danger: higher if guard is down and tracking coverage is low
    danger = 0.6 * guard_down + 0.4 * (1.0 - pose_cov)
    danger = max(0.0, min(1.0, danger))

    # Form score: start at 10, subtract penalties
    form = 10.0
    form -= guard_down * 5.0        # big penalty for leaky guard
    form -= (1.0 - pose_cov) * 2.0  # smaller penalty for low coverage
    form = max(0.0, min(10.0, form))

    if danger >= 0.7:
        focus = "defense_first"
    elif danger >= 0.4:
        focus = "ring_cutting"
    else:
        focus = "pressure_and_body"

    out = dict(stats)
    out["video_danger_score"] = float(danger)
    out["video_form_score"] = float(form)
    out["video_focus_next_round"] = focus
    return out

def load_rounds_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Convenience loader for data/video_round_stats.csv
    """
    return pd.read_csv(csv_path)
