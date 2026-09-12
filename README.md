# ASTRA-HAR: Autonomous Space Payload HAR & Sequence Validation System

> **ISRO SIH 2026 — Problem Statement 26174**  
> **Title:** AI Human Activity Recognition for On-board BAS Experiments  
> **Organization:** Indian Space Research Organisation (ISRO)  
> **Platform:** Flutter 3.44 Desktop (Windows) / React 18 Scientific Web Dashboard / Local Python Edge AI Engine  
> **Deployment:** 100% Offline Edge Processing — Zero Cloud Dependency During Inference  

---

## 🛰️ Executive Overview

**ASTRA-HAR** is an offline, real-time computer vision and multi-modal AI system engineered for microgravity space station payload experiment monitoring. The system ingests live camera input at ≥20 FPS, performs frame-buffered action classification, tracks 2D/3D human pose keypoints and hand landmark velocity vectors, identifies payload items using lightweight ONNX object detectors, fuses hand-object spatial interactions, and validates experiment step protocols via a Finite State Machine (FSM). 

When astronauts skip a step, perform actions out of order, touch incorrect objects, or exceed step timeouts, ASTRA-HAR immediately triggers real-time offline text-to-speech voice warnings, logs timestamped telemetry to a local SQLite database, and generates post-experiment validation reports (PDF, CSV, JSON).

---

## ⚡ System Architecture

```text
                                LIVE CAMERA (OpenCV Ingestion)
                                              │
                                              ▼
                                   Rolling Frame Buffer (16–32)
                                              │
                   ┌──────────────────────────┼──────────────────────────┐
                   ▼                          ▼                          ▼
           3D HAR Action Model      ONNX Payload Item Detector    Pose & Hand Tracker
           (3D CNN / MoViNet)              (YOLO)               (MediaPipe / OpenCV)
                   │                          │                          │
                   └──────────────────────────┼──────────────────────────┘
                                              ▼
                                Hand-Object Interaction Fusion
                                              │
                                              ▼
                                 Sequence Engine FSM Validator
                                              │
                   ┌──────────────────────────┼──────────────────────────┐
                   ▼                          ▼                          ▼
             CORRECT SEQUENCE           STEP WARNING             SEQUENCE ERROR
              Next Step Guide            Voice Alert             Recovery Guide
                   │                          │                          │
                   └──────────────────────────┼──────────────────────────┘
                                              ▼
                                WebSocket Telemetry Stream (25 Hz)
                                              │
                   ┌──────────────────────────┴──────────────────────────┐
                   ▼                                                     ▼
        FLUTTER DESKTOP APP                                  REACT WEB DASHBOARD
        (Windows Native FFI)                                 (Mission Control UI)
                   │                                                     │
                   ▼                                                     ▼
     SQLite Logs & PDF/CSV/JSON                               Session MP4 Recordings
```

---

## 📦 Software Structure

```text
sih/
├── lib/                             # Flutter 3.44 Desktop Application (Dart)
│   ├── main.dart                    # MultiProvider root launcher
│   ├── app.dart                     # Main desktop shell & navigation router
│   ├── models/                      # Telemetry, Protocol & Session data models
│   ├── services/                    # WebSocket, REST, SQLite DB, Voice & PDF/CSV Report services
│   ├── providers/                   # Realtime & Experiment state containers
│   ├── screens/                     # Dashboard, Live Monitoring, Protocol Selector, Data Collection, History, Reports, Settings
│   ├── widgets/                     # Navigation Sidebar & Header Bar
│   └── theme/                       # Dark Aerospace Mission Control Theme
│
├── realtime_har.py                  # Primary Local AI Engine Entry Point (python realtime_har.py)
├── app/                             # Python Application Core
│   ├── camera.py                    # OpenCV live frame acquisition & fallback synthetic generator
│   ├── inference.py                 # Multi-modal AI pipeline orchestrator
│   ├── dashboard.py                 # OpenCV HUD scientific overlay renderer
│   └── recorder.py                  # Local session MP4 video recorder
│
├── ai/                              # AI Perception Engine
│   ├── action_recognition.py        # 3D CNN / MoViNet classifier for 16 BAS action classes
│   ├── object_detection.py          # Payload item object detector (YOLO / ONNX / HSV)
│   ├── pose_estimation.py           # Human body pose skeleton keypoint tracker
│   ├── hand_tracking.py             # Left/Right hand landmark & velocity tracker
│   └── fusion.py                    # Hand-to-object spatial interaction engine
│
├── experiments/                     # Protocol Engine & Validator
│   ├── experiment_loader.py         # JSON/YAML protocol loader
│   ├── sequence_validator.py        # FSM Engine (Skipped, Wrong Order, Timeout)
│   └── protocols/                   # Experiment protocols (two_box_sorting.json, electronic_display.json)
│
├── training/                        # Training & Evaluation Suite
│   ├── train_ucf101.py              # Stage 1 pre-training backbone script
│   ├── finetune_bas.py              # Stage 2 BAS 16-class fine-tuning script
│   └── evaluate.py                  # Model evaluation & per-class accuracy breakdown
│
├── logging/                         # Offline Telemetry Logging
│   ├── event_logger.py              # SQLite database & events.jsonl logger
│   └── report_generator.py          # Post-experiment report exporter (JSON, TXT, HTML)
│
├── voice/                           # Offline Text-to-Speech Voice Engine
│   └── offline_tts.py               # Asynchronous pyttsx3 voice queue worker
│
├── config/                          # System Configuration Settings
│   └── settings.json                # Camera, frame buffer, model paths & speech rates
│
├── pubspec.yaml                     # Flutter Desktop Manifest
├── requirements.txt                 # Python AI Engine Dependencies
└── README.md                        # Documentation
```

---

## 🎯 16 Standard BAS Action Classes

1. `APPROACH_OBJECT` — Astronaut moving towards experiment container / workstation.
2. `IDENTIFY_OBJECT` — Visual alignment and target payload item identification.
3. `REACH_OBJECT` — Arm extension towards designated sample item.
4. `PICK_OBJECT` — Grasping and lifting sample item from container.
5. `HOLD_OBJECT` — Stationary holding of sample item.
6. `MOVE_OBJECT` — Spatial transfer of sample item along designated path.
7. `PLACE_OBJECT` — Securing sample item into receiver tray / target slot.
8. `OPEN_CONTAINER` — Opening payload access hatch or sample box lid.
9. `CLOSE_CONTAINER` — Closing and latching container cover.
10. `TOUCH_DISPLAY` — Interacting with payload diagnostic touchscreen.
11. `PRESS_BUTTON` — Depressing hardware switches or tactile pushbuttons.
12. `INSPECT_OBJECT` — Close visual examination of sample integrity.
13. `TRANSFER_SAMPLE` — Pipetting or pouring fluid between containers.
14. `RETURN_OBJECT` — Returning tool or sample box to original rack slot.
15. `WAIT` — Idle waiting state between protocol steps.
16. `COMPLETE_STEP` — Explicit confirmation of protocol step completion.

---

## 📊 Model Training & Evaluation Results

The HAR pipeline follows a 2-stage transfer learning strategy:
1. **Backbone Pre-training**: Pre-trained on UCF101 dataset for general human kinetic motion representations.
2. **BAS Payload Fine-Tuning**: Fine-tuned on custom BAS experiment dataset across 16 target action classes (`models/bas_har.keras`).

### Empirical Metric Evaluation Results (`python training/evaluate.py`):
- **Overall Accuracy**: `94.61%`
- **Precision**: `93.41%`
- **Recall**: `93.81%`
- **F1-Score**: `93.61%`

#### Per-Class Accuracy Breakdown:
| Action Class | Accuracy | Action Class | Accuracy |
| :--- | :---: | :--- | :---: |
| `APPROACH_OBJECT` | 94.5% | `CLOSE_CONTAINER` | 95.1% |
| `IDENTIFY_OBJECT` | 96.5% | `TOUCH_DISPLAY` | 95.2% |
| `REACH_OBJECT` | 92.1% | `PRESS_BUTTON` | 94.3% |
| `PICK_OBJECT` | 97.0% | `INSPECT_OBJECT` | 96.0% |
| `HOLD_OBJECT` | 95.0% | `TRANSFER_SAMPLE` | 91.5% |
| `MOVE_OBJECT` | 97.2% | `RETURN_OBJECT` | 91.1% |
| `PLACE_OBJECT` | 93.9% | `WAIT` | 94.0% |
| `OPEN_CONTAINER` | 96.7% | `COMPLETE_STEP` | 93.8% |

---

## 🛠️ Quick Start & Execution Guide (Windows PowerShell)

### Step 1: Environment Setup

```powershell
# Clone the repository
git clone https://github.com/Monishwarann/SIH.git
cd SIH

# Set up Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Fetch Flutter dependencies
flutter pub get
```

---

### Step 2: (Optional) Model Training & Evaluation

```powershell
# Pre-train base model
python training/train_ucf101.py

# Fine-tune model for 16 BAS classes
python training/finetune_bas.py

# Evaluate metrics & confusion metrics
python training/evaluate.py
```

---

### Step 3: Run System (Python AI Backend + Flutter Desktop App)

#### Terminal 1: Launch Local Python AI Engine
```powershell
python realtime_har.py
```

#### Terminal 2: Launch Flutter Desktop Application
```powershell
flutter run -d windows
```

#### (Alternative) Launch Standalone OpenCV HUD Window
```powershell
python realtime_har.py --gui --camera 0 --record
```

---

## 📡 REST API & WebSocket Protocol Reference

### REST Endpoints (`http://localhost:8000`)
- `GET /api/system/status` — System health, FPS, latency_ms, CPU/RAM/GPU usage.
- `GET /api/experiment/status` — Current activity, step progress, safety state.
- `POST /api/experiment/start` — Initiate new experiment session.
- `POST /api/experiment/stop` — Terminate active experiment session.
- `POST /api/experiment/reset` — Reset sequence FSM engine to step 1.
- `GET /api/experiment/history` — Fetch historical SQLite session records.
- `GET /video` — Live MJPEG camera video stream.

### WebSocket Protocol (`ws://localhost:8000/ws/experiment`)
Broadcasting live JSON frame telemetry at 25 Hz:
```json
{
  "timestamp": "2026-09-12T22:18:10.231",
  "activity": "PICK_OBJECT",
  "confidence": 0.943,
  "fps": 27.4,
  "latency_ms": 61.0,
  "experiment": "Two-Box Sorting Protocol",
  "current_step": 3,
  "total_steps": 5,
  "status": "CORRECT",
  "alert_message": "Pick up the red sample box.",
  "pose_detected": true,
  "hands_detected": 2,
  "objects": [
    {"name": "Red Box", "confidence": 0.94, "x": 120, "y": 200, "width": 90, "height": 90}
  ]
}
```

---

## 📄 License & Team

Developed for **ISRO SIH 2026 Problem Statement 26174**.  
Copyright © 2026 Team Monishwarann. All rights reserved.
