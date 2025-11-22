# 🥊 SAMMO Fight IQ

**Personal AI Boxing Coach** Turns sparring video into actionable coaching feedback.

Built on Red Hat OpenShift AI with pose detection, risk assessment, and persistent memory.

---

## What It Does

1. **Analyzes sparring video** using MediaPipe pose detection
2. **Extracts boxing metrics**: guard height, hip rotation, stance width, head position
3. **Calculates risk scores**: `danger_score` (0-1), `form_score` (0-10)
4. **Recommends focus areas**: defense, ring cutting, pressure, body work
5. **Provides coaching feedback** via an AI agent with conversation memory

---

## Sample Output
```
🥊 SAMMO:
Your danger score of 0.65 is in the MODERATE-HIGH risk zone.

Main issue: Guard discipline - you're dropping it 38% of the time.
Your left guard averages 0.42 (should be 0.55+).

Fix: "Punch-and-return" drill
- 3 rounds on heavy bag
- Every combo ends with hands back to face
- Focus on form, not power

Hip rotation at 28° is weak - wider stance + resistance band work.
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Video Processing | MediaPipe, OpenCV |
| ML Models | scikit-learn (RandomForest) |
| AI Coaching | Local LLM (Ollama/Mistral) |
| Memory | Pure Python JSONL store |
| Infrastructure | Red Hat OpenShift AI |
| API | FastAPI (planned) |

---

## Project Structure
```
sammo-fight-iq/
├── data/                    # Round stats and video data
├── mem_data/                # Conversation history
├── models/                  # Trained ML models
│   ├── danger_predictor.joblib
│   └── focus_predictor.joblib
├── notebooks/
│   ├── 01_pose_detection_test.ipynb
│   ├── 02_video_processing.ipynb
│   └── 03_model_inference_test.ipynb
└── src/
    ├── simple_memory.py     # JSONL-based conversation store
    ├── llm_client.py        # OpenAI-compatible LLM client
    ├── memory_layer.py      # Memory-backed LLM wrapper
    └── agents/
        ├── base_coach.py
        └── boxing_coach.py  # SAMMO personality
```

---

## Key Metrics

The system tracks these per-round metrics:

| Metric | Description | Target |
|--------|-------------|--------|
| `danger_score` | Overall risk level (0-1) | < 0.5 |
| `guard_down_ratio` | % of time guard is dropped | < 20% |
| `avg_left_guard_height` | Left hand position (0-1) | > 0.55 |
| `avg_right_guard_height` | Right hand position (0-1) | > 0.55 |
| `avg_hip_rotation` | Rotation in degrees | > 35° |
| `avg_stance_width` | Normalized stance width | > 0.4 |
| `form_score` | Overall technique (0-10) | > 7.0 |

---

## Quick Start
```bash
# Clone
git clone https://github.com/ncode3/sammo-fight-iq.git
cd sammo-fight-iq

# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter lab notebooks/03_model_inference_test.ipynb
```

---

## Roadmap

- [x] Video pose detection pipeline
- [x] Risk scoring model
- [x] Agentic coach with memory
- [ ] Connect to production LLM (Ollama)
- [ ] FastAPI server deployment
- [ ] Web UI (Streamlit/Gradio)
- [ ] World model for predictive coaching
- [ ] Multi-round progress tracking

---

## About

Built by a 47-year-old boxer who wanted objective feedback on his sparring rounds.

**The problem:** Coaches can't watch every round. Generic advice like "keep your guard up" doesn't help.

**The solution:** AI that watches your video, measures what matters, and tells you exactly what to fix.

---

## License

MIT
EOF
![Architecture](docs/architecture.svg)
