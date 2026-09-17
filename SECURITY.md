# 🔒 Security Policy - ASTRA-HAR

## 🛰️ Security Overview

**ASTRA-HAR** (*Autonomous Space Payload HAR & Sequence Validation System*) is engineered for high-reliability, air-gapped microgravity payload operations in space station environments (**ISRO SIH 2026 PS 26174**). 

Given its deployment context on autonomous payload monitoring hardware, **data privacy, operational integrity, and zero cloud exposure** are foundational design principles of the platform architecture.

---

## 🛡️ Supported Versions

We provide security updates and patches for the following versions of ASTRA-HAR:

| Version | Supported | Security Patch Status |
| :--- | :---: | :--- |
| `1.0.x` (Current) | ✅ Yes | Active Security Maintenance |
| `< 1.0.0` | ❌ No | Deprecated |

---

## 🔐 Core Security Architectural Guarantees

### 1. 100% Air-Gapped & Offline Architecture
- **Zero Cloud Exposure**: All computer vision model inference (3D CNN / Keras BiLSTM / ONNX / PyTorch), hand tracking, sequence validation, and voice generation run strictly on local hardware edge nodes.
- **No External Outbound Calls**: No telemetry, analytics, frame clips, or diagnostic data are transmitted over the public Internet.

### 2. Local REST & WebSocket API Isolation
- By default, the REST and WebSocket API servers bind to `127.0.0.1` (local loopback) or configured isolated mission control LAN subnets.
- Cross-Origin Resource Sharing (CORS) policies are restricted to authorized local dashboard interfaces (`http://localhost:5173`, `http://localhost:8000`).

### 3. Model Weight & Artifact Integrity
- Model artifacts (`models/best_bilstm_model.keras`, `models/object_detector.onnx`, `models/activity_model.pt`) are loaded strictly from local verified paths.
- We recommend verifying model file SHA-256 hashes prior to deployment to prevent tampered or corrupted weight execution.

### 4. Local Telemetry & Video Encryption
- SQLite database logs (`data/sih_database.db`) and local video session recordings (`recordings/`) remain on local storage.
- In mission-critical environments, host file-system encryption (e.g., BitLocker / LUKS) should be enabled on the edge hardware storage drive.

---

## 🚨 Reporting a Vulnerability

We take the security of ASTRA-HAR seriously. If you discover a security vulnerability or potential threat vector, please report it responsibly.

### How to Submit a Security Report

1. **GitHub Private Vulnerability Reporting**:
   Navigate to the [Security Tab](https://github.com/Monishwarann/SIH/security/advisories/new) of this repository and click **"Report a vulnerability"**.

2. **Email Disclosure**:
   Alternatively, email the maintainers directly at:
   `k.monishwaran123@gmail.com`

### What to Include in Your Report

Please include as much of the following information as possible to help us triage and patch the issue promptly:
- Type of vulnerability (e.g., buffer overflow in C++ binding, privilege escalation in local API, model loading deserialization risk).
- Clear step-by-step instructions or proof-of-concept (PoC) to reproduce the vulnerability.
- Affected component (`ai/`, `backend/`, `core/`, `frontend/`, or `lib/`).
- System environment details (OS, Python version, Flutter runtime version).

### Disclosure Timeline Commitments

- **Initial Response**: Within **24 hours** of receiving the report.
- **Status & Assessment**: Update provided within **48 hours**.
- **Fix & Patch Target**: Released within **7 business days** for high/critical severity issues.

---

## 📋 Operational Security Checklist for Deployment

When deploying ASTRA-HAR on payload workstations or edge hardware:

- [ ] Verify host OS is hardened with disabled unnecessary remote services (SSH/RDP restricted to secure management LAN).
- [ ] Confirm Python virtual environment dependencies are built from verified `requirements.txt` packages.
- [ ] Ensure local REST/WebSocket server port (`8000`) is protected by host firewall rules.
- [ ] Verify `models/best_bilstm_model.keras` model file integrity prior to initiating mission runs.
- [ ] Keep local storage encrypted using full-disk encryption (FDE).
