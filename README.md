<div align="center">

# 💧 JKD Coach

### *Be Water. Train Smarter.*

**AI-Powered Boxing Coach** — From video analysis to actionable coaching, blending Bruce Lee's adaptability with decades of ring wisdom.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenShift AI](https://img.shields.io/badge/OpenShift_AI-EE0000?style=for-the-badge&logo=redhat&logoColor=white)](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Bruce_Lee_1973.jpg/440px-Bruce_Lee_1973.jpg" alt="Bruce Lee" width="300">

*"Be water, my friend. Empty your mind. Be formless, shapeless, like water. You put water into a cup, it becomes the cup. You put water into a bottle, it becomes the bottle. You put it into a teapot, it becomes the teapot. Now water can flow, or it can crash. Be water, my friend."*

**— Bruce Lee**, Founder of Jeet Kune Do

</div>

---

## 🏆 The Legacy

<div align="center">

![Jimmy Carter - 3x World Lightweight Champion](docs/jimmy_carter_hof.jpg)

**Jimmy Carter** — *3x World Lightweight Champion (1950s)*
*International Boxing Hall of Fame Inductee*
</div>

Before JKD Coach was an AI, there was **Jimmy Carter** — not the president, but my grandfather, a legend in the ring.

In the 1950s, Jimmy Carter stood at the pinnacle of boxing. **Three-time World Lightweight Champion** and later inducted into the **International Boxing Hall of Fame**, he wasn't just a fighter — he was a *student* of the sweet science. His teachings passed down through generations: *"Watch your opponent's hips, not their hands. The hips don't lie."*

I'm 47 years old now, still stepping into the ring, still chasing that perfect round. When I spar, I hear my grandfather's voice in my head. But coaches can't watch every round. Video sits on phones, unreviewed. The wisdom that took a lifetime to accumulate — *how do we preserve it? How do we pass it on?*

---

## 🌊 Two Philosophies, One Vision

**JKD Coach** fuses two legendary approaches to combat:

### Bruce Lee's "Be Water" Philosophy
Adaptability. Fluidity. No fixed form. Jeet Kune Do teaches us to flow with the situation, absorbing what is useful and rejecting what is useless. In the ring, rigidity gets you knocked out. The fighter who can *adapt* — who can read, adjust, and flow — is the one who survives.

### Jimmy Carter's Ring Wisdom
*"The hips don't lie."* Technical precision. Pattern recognition. My grandfather knew that true mastery comes from understanding the fundamentals deeply enough to *see* what others miss. Every subtle shift in stance, every rotation of the hip, every dropped guard — these tell the story of a round.

**JKD Coach** is my answer. It's not just an AI coach. It's a way to encode the knowledge that made champions — the *adaptability* of Bruce Lee and the *precision* of Jimmy Carter — and make it available to every fighter willing to learn.

---

## ⚡ What JKD Coach Does

JKD Coach turns raw sparring footage into the kind of feedback a hall-of-fame coach would give:

| Step | What Happens |
|:----:|--------------|
| 📹 | **Analyzes sparring video** using MediaPipe pose detection |
| 📊 | **Extracts boxing metrics**: guard height, hip rotation, stance width, head position |
| ⚠️ | **Calculates risk scores**: `danger_score` (0-1), `form_score` (0-10) |
| 🎯 | **Recommends focus areas**: defense, ring cutting, pressure, body work |
| 🤖 | **Provides coaching feedback** via an AI agent with conversation memory |

The AI remembers your previous sessions. It knows your patterns. It *adapts* to you. It becomes *your* coach.

---

## 💬 Sample Coaching Session

```
💧 JKD Coach:

Your danger score of 0.65 is in the MODERATE-HIGH risk zone.

Main issue: Guard discipline - you're dropping it 38% of the time.
Your left guard averages 0.42 (should be 0.55+).

"Be water" - flow with your defense, don't force it.

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

The metrics my grandfather would track with his eyes, JKD Coach tracks with computer vision:

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
jkd-coach/
├── 📂 src/                     # Core source code
│   ├── agents/                 # AI coaching agents
│   ├── auth/                   # Authentication module
│   └── utilities/              # Helper functions
├── 📂 deployments/             # Deployment configurations
│   ├── openshift/              # OpenShift/Kubernetes
│   ├── cloud-functions/        # Google Cloud Functions
│   └── fastapi-auth/           # FastAPI with JWT auth
├── 📂 docs/                    # Complete documentation
├── 📂 notebooks/               # Jupyter notebooks for analysis
├── 📂 tests/                   # Test suites
├── 📂 data/                    # Training data and videos
├── 📂 models/                  # Trained ML models
└── 📂 mem_data/                # Conversation history
```

**[📖 Full Project Structure](docs/PROJECT_STRUCTURE.md)**

---

## 🚀 Quick Start

### Option 1: Deploy to OpenShift (5 minutes)

```bash
# Set your Firestore credentials
export FIRESTORE_CREDENTIALS=/path/to/credentials.json

# Deploy
cd deployments/openshift
./deploy.sh
```

**[📘 OpenShift Quick Start](docs/OPENSHIFT_QUICKSTART.md)**

### Option 2: Run API with Authentication

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your JWT_SECRET_KEY and GOOGLE_APPLICATION_CREDENTIALS

# Start API server
cd deployments/fastapi-auth
python api_server.py
# Visit http://localhost:8000/docs
```

**[📘 API Quick Start](docs/API_QUICKSTART.md)**

### Option 3: Explore with Jupyter

```bash
# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter lab notebooks/03_model_inference_test.ipynb
```

---

## 📦 Deployment Options

JKD Coach can be deployed in multiple ways:

| Deployment | Best For | Quick Start |
|------------|----------|-------------|
| **[OpenShift/Kubernetes](deployments/openshift/)** | On-premises, enterprise | [Deploy Now](docs/OPENSHIFT_QUICKSTART.md) |
| **[FastAPI + JWT Auth](deployments/fastapi-auth/)** | API-first, user authentication | [Setup Guide](docs/AUTH_SETUP.md) |
| **[Cloud Functions](deployments/cloud-functions/)** | Serverless, pay-per-use | [Deploy Guide](docs/DEPLOYMENT.md) |

**[🔍 Compare Deployments](deployments/README.md)**

---

## 📚 Documentation

### Quick Links
- **[📖 All Documentation](docs/README.md)** - Complete docs index
- **[🚀 OpenShift Deployment](docs/OPENSHIFT_DEPLOYMENT.md)** - Container deployment guide
- **[🔐 Authentication Guide](docs/AUTH_SETUP.md)** - JWT auth setup
- **[⚡ Quick Commands](docs/DEPLOYMENT_COMMANDS.md)** - CLI reference

### By Topic
- **Getting Started**: [Deployment Options](deployments/README.md)
- **API Development**: [API Quick Start](docs/API_QUICKSTART.md)
- **DevOps**: [OpenShift Guide](docs/OPENSHIFT_DEPLOYMENT.md)
- **Reference**: [Project Structure](docs/PROJECT_STRUCTURE.md)

---

## 🗺️ Roadmap

**Completed:**
- [x] ✅ Video pose detection pipeline
- [x] ✅ Risk scoring model
- [x] ✅ Agentic coach with memory
- [x] ✅ JWT authentication system
- [x] ✅ FastAPI server with auth
- [x] ✅ OpenShift containerization
- [x] ✅ Cloud Functions deployment

**In Progress:**
- [ ] 🔄 Connect to production LLM (Ollama)
- [ ] 🔄 Email verification flow
- [ ] 🔄 OAuth integration

**Future:**
- [ ] 📋 Web UI (Streamlit/Gradio)
- [ ] 📋 World model for predictive coaching
- [ ] 📋 Multi-round progress tracking
- [ ] 📋 Multi-fighter comparison analytics
- [ ] 📋 Real-time video analysis

---

## 🙏 About This Project

This isn't just code. It's a continuation of a family tradition.

My grandfather spent his life mastering the sweet science, then passing that knowledge to the next generation. I've spent decades in the gym, absorbing what I could, trying to be worthy of that legacy.

**The problem I faced:** At 47, I still spar regularly. But coaches can't watch every round. Video piles up on my phone. Generic advice like "keep your guard up" doesn't cut it when you need to know *exactly* what's breaking down and *when*.

**JKD Coach is the solution:** An AI that watches your video, measures what matters, and tells you exactly what to fix — with the kind of specificity that would make Jimmy Carter proud and the adaptability that Bruce Lee embodied.

The philosophy behind JKD Coach honors both legends: **Be water** in your approach — adapt, flow, evolve. But also **watch the hips** — measure everything, understand the fundamentals, leave nothing to chance.

---

<div align="center">

### 💧 *"Be water, my friend."*
— Bruce Lee

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

![JKD Coach Architecture](docs/sammo_architecture.svg)
