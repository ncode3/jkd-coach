"""
Centralized configuration for SAMMO Fight IQ.
"""
from pathlib import Path
import os

# Project paths - configurable via environment variables
PROJECT_ROOT = Path(os.getenv("SAMMO_PROJECT_ROOT", Path(__file__).parent.parent))
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
MEM_DATA_DIR = PROJECT_ROOT / "mem_data"

# Model configuration
DEFAULT_MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Boxing metrics thresholds
GUARD_DOWN_THRESHOLD = 0.15
DANGER_HIGH_THRESHOLD = 0.7
DANGER_MEDIUM_THRESHOLD = 0.4
