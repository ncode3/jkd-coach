"""Tests for the risk model module."""
import pytest
from src.risk_model import video_form_and_danger

class TestVideoFormAndDanger:
    def test_low_danger_scenario(self):
        """Test that good stats result in low danger score."""
        stats = {
            "guard_down_ratio": 0.05,
            "pose_coverage": 0.9,
        }
        result = video_form_and_danger(stats)
        assert result["video_danger_score"] < 0.2
        assert result["video_form_score"] > 8.0
        assert result["video_focus_next_round"] == "pressure_and_body"

    def test_high_danger_scenario(self):
        """Test that poor stats result in high danger score."""
        stats = {
            "guard_down_ratio": 0.8,
            "pose_coverage": 0.3,
        }
        result = video_form_and_danger(stats)
        assert result["video_danger_score"] >= 0.7
        assert result["video_focus_next_round"] == "defense_first"

    def test_danger_score_bounds(self):
        """Test that danger score is always between 0 and 1."""
        stats = {
            "guard_down_ratio": 1.5,  # Invalid but should be handled
            "pose_coverage": -0.5,    # Invalid but should be handled
        }
        result = video_form_and_danger(stats)
        assert 0.0 <= result["video_danger_score"] <= 1.0
        assert 0.0 <= result["video_form_score"] <= 10.0
