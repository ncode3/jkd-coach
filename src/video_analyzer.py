"""
Video Analysis Module for JKD Coach

Uses MediaPipe Pose to extract boxing metrics from sparring videos.
Based on logic from notebooks/02_video_processing.ipynb
"""
from typing import Dict, Any
import cv2
import mediapipe as mp
import numpy as np


class VideoAnalyzer:
    """Analyzes boxing videos using MediaPipe Pose detection."""

    def __init__(self):
        """Initialize MediaPipe Pose."""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def __del__(self):
        """Clean up MediaPipe resources."""
        if hasattr(self, 'pose'):
            self.pose.close()

    def _extract_frame_metrics(self, landmarks) -> Dict[str, float]:
        """
        Extract boxing metrics from pose landmarks for a single frame.

        Args:
            landmarks: MediaPipe pose landmarks

        Returns:
            Dict with per-frame metrics
        """
        lmk = landmarks

        # Get key landmarks
        left_shoulder = lmk[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lmk[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = lmk[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = lmk[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        left_hip = lmk[self.mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = lmk[self.mp_pose.PoseLandmark.RIGHT_HIP]
        nose = lmk[self.mp_pose.PoseLandmark.NOSE]
        left_ankle = lmk[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = lmk[self.mp_pose.PoseLandmark.RIGHT_ANKLE]

        # Guard height: wrist Y relative to shoulder Y
        # (lower value = hands higher, better guard)
        left_guard_height = left_wrist.y - left_shoulder.y
        right_guard_height = right_wrist.y - right_shoulder.y

        # Hip rotation: horizontal distance between hips
        hip_rotation = abs(left_hip.x - right_hip.x)

        # Stance width: horizontal distance between ankles
        stance_width = abs(left_ankle.x - right_ankle.x)

        # Head position
        head_y = nose.y

        # Calculate head movement (can use vertical displacement)
        # For now, just track Y position

        return {
            "left_guard_height": left_guard_height,
            "right_guard_height": right_guard_height,
            "hip_rotation": hip_rotation,
            "stance_width": stance_width,
            "head_y": head_y,
        }

    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze a boxing video and extract aggregate metrics.

        Args:
            video_path: Path to video file

        Returns:
            Dict with aggregated metrics:
                - total_frames: Total frames in video
                - pose_frames: Frames where pose was detected
                - pose_coverage: Ratio of pose_frames/total_frames
                - guard_down_ratio: % of frames where guard was down
                - avg_left_guard_height: Average left guard height
                - avg_right_guard_height: Average right guard height
                - avg_hip_rotation: Average hip rotation (degrees)
                - avg_stance_width: Average stance width
                - head_movement_score: Head movement metric
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        frame_idx = 0
        pose_detected_frames = 0
        guard_down_frames = 0

        # Accumulators for averaging
        left_guard_sum = 0.0
        right_guard_sum = 0.0
        hip_rotation_sum = 0.0
        stance_width_sum = 0.0
        head_y_sum = 0.0
        head_y_values = []

        # Guard "down" threshold (wrist below shoulder by this much)
        GUARD_DOWN_THRESHOLD = 0.15

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1

            # Convert BGR (OpenCV) to RGB (MediaPipe)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            if results.pose_landmarks:
                pose_detected_frames += 1

                # Extract metrics for this frame
                metrics = self._extract_frame_metrics(results.pose_landmarks.landmark)

                # Accumulate for averaging
                left_guard_sum += metrics["left_guard_height"]
                right_guard_sum += metrics["right_guard_height"]
                hip_rotation_sum += metrics["hip_rotation"]
                stance_width_sum += metrics["stance_width"]
                head_y_sum += metrics["head_y"]
                head_y_values.append(metrics["head_y"])

                # Check if guard is down
                if (metrics["left_guard_height"] > GUARD_DOWN_THRESHOLD or
                    metrics["right_guard_height"] > GUARD_DOWN_THRESHOLD):
                    guard_down_frames += 1

        cap.release()

        # Calculate aggregated metrics
        total_frames = frame_idx
        pose_coverage = pose_detected_frames / total_frames if total_frames > 0 else 0.0
        guard_down_ratio = guard_down_frames / pose_detected_frames if pose_detected_frames > 0 else 0.0

        # Averages (only over frames where pose was detected)
        if pose_detected_frames > 0:
            avg_left_guard = left_guard_sum / pose_detected_frames
            avg_right_guard = right_guard_sum / pose_detected_frames
            avg_hip_rotation = hip_rotation_sum / pose_detected_frames
            avg_stance_width = stance_width_sum / pose_detected_frames
            avg_head_y = head_y_sum / pose_detected_frames

            # Head movement score: standard deviation of head Y position
            # Higher = more head movement (good for defense)
            head_movement_score = float(np.std(head_y_values)) if len(head_y_values) > 1 else 0.0
        else:
            avg_left_guard = 0.0
            avg_right_guard = 0.0
            avg_hip_rotation = 0.0
            avg_stance_width = 0.0
            avg_head_y = 0.0
            head_movement_score = 0.0

        # Convert hip rotation from normalized distance to approximate degrees
        # Rough approximation: multiply by ~180 degrees
        avg_hip_rotation_degrees = avg_hip_rotation * 180.0

        # Normalize stance width (0-1 scale where ~0.4+ is good)
        # Already normalized by MediaPipe coordinates

        return {
            "total_frames": total_frames,
            "pose_frames": pose_detected_frames,
            "pose_coverage": float(pose_coverage),
            "guard_down_ratio": float(guard_down_ratio),
            "avg_left_guard_height": float(avg_left_guard),
            "avg_right_guard_height": float(avg_right_guard),
            "avg_hip_rotation": float(avg_hip_rotation_degrees),
            "avg_stance_width": float(avg_stance_width),
            "head_movement_score": head_movement_score,
        }


def analyze_video_file(video_path: str) -> Dict[str, Any]:
    """
    Convenience function to analyze a video file.

    Args:
        video_path: Path to video file

    Returns:
        Dict with video analysis metrics
    """
    analyzer = VideoAnalyzer()
    return analyzer.analyze_video(video_path)
