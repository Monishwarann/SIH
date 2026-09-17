# 📜 Copyright & Intellectual Property Notice

## 🛰️ Project Ownership

**ASTRA-HAR** (*Autonomous Space Payload HAR & Sequence Validation System*)  
**ISRO Smart India Hackathon (SIH) 2026 — Problem Statement 26174**

- **Copyright Owner**: © 2026 K. Monishwaran (Monishwarann)
- **Official Repository**: [https://github.com/Monishwarann/SIH](https://github.com/Monishwarann/SIH)
- **Primary Maintainer Contact**: `k.monishwaran123@gmail.com`

---

## 📄 License & Distribution Terms

This software and associated documentation files are distributed under the **MIT License**.

### Summary of Rights:
- **Permission**: Granted free of charge to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
- **Attribution Condition**: The above copyright notice, repository link, and this permission notice shall be included in all copies or substantial portions of the Software.

For full license terms, refer to the [`LICENSE`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/LICENSE) file in the root directory.

---

## 🧠 Intellectual Property Allocation

### 1. Source Code Architecture
All custom source code written for ASTRA-HAR, including:
- **AI Core & Vision Pipeline**: [`ai/action_recognition.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/ai/action_recognition.py), [`ai/object_detection.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/ai/object_detection.py), [`ai/pose_estimation.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/ai/pose_estimation.py), [`ai/fusion.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/ai/fusion.py).
- **Sequence Validation Engine (FSM)**: [`experiments/sequence_validator.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/experiments/sequence_validator.py), [`core/sequence/sequence_engine.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/core/sequence/sequence_engine.py).
- **Flutter Desktop Interface**: [`lib/`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/lib) (Glassmorphism design tokens, telemetry screens, custom canvas painters).
- **React Scientific Dashboard**: [`frontend/src/`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/frontend/src) (Vite/React components, WebSocket streaming engine).
- **REST & WebSocket API Backend**: [`backend/main.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/backend/main.py), [`app/inference.py`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/app/inference.py).

### 2. Trained Machine Learning Models
- **Keras BiLSTM Model**: [`models/best_bilstm_model.keras`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/models/best_bilstm_model.keras) (3D CNN + TimeDistributed BiLSTM architecture for 16-frame BAS activity classification).
- **ONNX Payload Detectors**: [`models/object_detector.onnx`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/models/object_detector.onnx).
- **PyTorch Activity Representations**: [`models/activity_model.pt`](file:///c:/Users/kmoni/Downloads/SIH-main/SIH-main/models/activity_model.pt).

---

## 🤝 Third-Party Framework & Library Acknowledgments

ASTRA-HAR builds upon leading open-source software libraries:

| Library / Framework | License | Project Role |
| :--- | :--- | :--- |
| **TensorFlow / Keras** | Apache 2.0 | Deep Learning Neural Network Training & Inference |
| **OpenCV** | Apache 2.0 | Real-Time Video Frame Ingestion & Image Processing |
| **MediaPipe** | Apache 2.0 | Body Skeleton & Hand Kinematic Pose Extraction |
| **Flutter** | BSD 3-Clause | Windows Native Desktop Mission Control UI |
| **React & Vite** | MIT License | Scientific Web Telemetry Dashboard |
| **FastAPI & Uvicorn** | MIT License | High-Performance REST & WebSocket Telemetry Server |
| **pyttsx3** | MPL 2.0 | Asynchronous Offline Voice Synthesis |

---

## 📬 Contact for Licensing Enquiries

For inquiries regarding commercial usage, research collaboration, or custom deployment rights beyond the MIT License:

**K. Monishwaran**  
Email: `k.monishwaran123@gmail.com`  
GitHub: [https://github.com/Monishwarann](https://github.com/Monishwarann)
