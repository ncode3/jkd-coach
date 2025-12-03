<div align="center">

# 🥊 SAMMO Fight IQ

### *Carrying On a Legacy, One Round at a Time*

**AI-Powered Boxing Coach** — From video analysis to actionable coaching, built on decades of ring wisdom.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenShift AI](https://img.shields.io/badge/OpenShift_AI-EE0000?style=for-the-badge&logo=redhat&logoColor=white)](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

*"Boxing is the ultimate truth. Nobody can hide in the ring."*

</div>

---

## 🏆 The Legacy

<div align="center">

<img src="docs/jimmy_carter_boxer.jpg" alt="Jimmy Carter - 3x World Lightweight Champion" width="400">

**Jimmy Carter** — *3x World Lightweight Champion (1950s)*  
*International Boxing Hall of Fame Inductee*
</div>

Before SAMMO was an AI, there was **Jimmy Carter** not the president, but my grandfather, a legend in the ring.

In the 1950s, Jimmy Carter stood at the pinnacle of boxing. **Three-time World Lightweight Champion** and later inducted into the **International Boxing Hall of Fame**, he wasn't just a fighter he was a *student* of the sweet science. His teachings passed down through generations: *"Watch your opponent's hips, not their hands. The hips don't lie."*

I'm 47 years old now, still stepping into the ring, still chasing that perfect round. When I spar, I hear my grandfather's voice in my head. But coaches can't watch every round. Video sits on phones, unreviewed. The wisdom that took a lifetime to accumulate *how do we preserve it? How do we pass it on?*

**SAMMO** is my answer. It's not just an AI coach. It's a way to encode the knowledge that made champions, and make it available to every fighter willing to learn.

---

## ⚡ What SAMMO Does

SAMMO turns raw sparring footage into the kind of feedback a hall-of-fame coach would give:

| Step | What Happens |
|:----:|--------------|
| 📹 | **Analyzes sparring video** using MediaPipe pose detection |
| 📊 | **Extracts boxing metrics**: guard height, hip rotation, stance width, head position |
| ⚠️ | **Calculates risk scores**: `danger_score` (0-1), `form_score` (0-10) |
| 🎯 | **Recommends focus areas**: defense, ring cutting, pressure, body work |
| 🤖 | **Provides coaching feedback** via an AI agent with conversation memory |

The AI remembers your previous sessions. It knows your patterns. It becomes *your* coach.

---

## 💬 Sample Coaching Session

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

Remember: "The hips don't lie." - Jimmy Carter
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| 📹 Video Processing | MediaPipe, OpenCV | Pose detection & frame analysis |
| 🧠 ML Models | scikit-learn (RandomForest) | Risk scoring & focus prediction |
| 💬 AI Coaching | Local LLM (Ollama/Mistral) | Natural language feedback |
| 💾 Memory | Pure Python JSONL store | Conversation & session history |
| ☁️ Infrastructure | Red Hat OpenShift AI | Scalable deployment |
| 🔌 API | FastAPI (planned) | REST endpoints |

---

## 📈 Key Metrics

The metrics my grandfather would track with his eyes, SAMMO tracks with computer vision:

| Metric | Description | Target | Why It Matters |
|--------|-------------|--------|----------------|
| `danger_score` | Overall risk level (0-1) | < 0.5 | High scores = you're getting hit |
| `guard_down_ratio` | % of time guard drops | < 20% | Dropping guard = knockout risk |
| `avg_left_guard_height` | Left hand position (0-1) | > 0.55 | Jab defense readiness |
| `avg_right_guard_height` | Right hand position (0-1) | > 0.55 | Power hand protection |
| `avg_hip_rotation` | Rotation in degrees | > 35° | Power generation |
| `avg_stance_width` | Normalized stance width | > 0.4 | Balance & mobility |
| `form_score` | Overall technique (0-10) | > 7.0 | Compound quality metric |

---

## 📁 Project Structure

```
sammo-fight-iq/
├── 📂 data/                    # Round stats and video data
├── 📂 mem_data/                # Conversation history
├── 📂 models/                  # Trained ML models
│   ├── danger_predictor.joblib
│   └── focus_predictor.joblib
├── 📓 notebooks/
│   ├── 01_pose_detection_test.ipynb
│   ├── 02_video_processing.ipynb
│   └── 03_model_inference_test.ipynb
└── 📂 src/
    ├── simple_memory.py        # JSONL-based conversation store
    ├── llm_client.py           # OpenAI-compatible LLM client
    ├── memory_layer.py         # Memory-backed LLM wrapper
    └── agents/
        ├── base_coach.py
        └── boxing_coach.py     # SAMMO personality
```

---

## 🚀 Quick Start

```bash
# Clone the legacy
git clone https://github.com/ncode3/sammo-fight-iq.git
cd sammo-fight-iq

# Install dependencies
pip install -r requirements.txt

# Start training
jupyter lab notebooks/03_model_inference_test.ipynb
```

---

## 🗺️ Roadmap

**Completed:**
- [x] ✅ Video pose detection pipeline
- [x] ✅ Risk scoring model
- [x] ✅ Agentic coach with memory

**In Progress:**
- [ ] 🔄 Connect to production LLM (Ollama)
- [ ] 🔄 FastAPI server deployment

**Future:**
- [ ] 📋 Web UI (Streamlit/Gradio)
- [ ] 📋 World model for predictive coaching
- [ ] 📋 Multi-round progress tracking
- [ ] 📋 Multi-fighter comparison analytics

---

## 🙏 About This Project

This isn't just code. It's a continuation of a family tradition.

My grandfather spent his life mastering the sweet science, then passing that knowledge to the next generation. I've spent decades in the gym, absorbing what I could, trying to be worthy of that legacy.

**The problem I faced:** At 47, I still spar regularly. But coaches can't watch every round. Video piles up on my phone. Generic advice like "keep your guard up" doesn't cut it when you need to know *exactly* what's breaking down and *when*.

**SAMMO is the solution:** An AI that watches your video, measures what matters, and tells you exactly what to fix—with the kind of specificity that would make Jimmy Carter proud.

The name "SAMMO" honors the style of analysis my grandfather taught: **S**tance, **A**ngle, **M**ovement, **M**etrics, **O**utput. Watch everything. Measure everything. Leave nothing to chance.

---

<div align="center">

### 🥊 *"Champions aren't made in the ring—they're recognized there."*
— Jimmy Carter, Hall of Fame

---

**Built with 💪 and Python**

[![GitHub](https://img.shields.io/badge/GitHub-ncode3-181717?style=flat-square&logo=github)](https://github.com/ncode3)

</div>

---

## 📄 License

MIT License — Use it, learn from it, pass it on.

---

![SAMMO Architecture](docs/sammo_architecture.svg)
