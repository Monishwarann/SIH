import asyncio
import time
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from core.realtime.realtime_state import realtime_state
from core.pipeline.scenario_engine import ScenarioEngine
from core.pipeline.camera_worker import camera_worker
from backend.websocket.ws_manager import ws_manager
from backend.streaming.stream_manager import stream_manager
from backend.database.db_service import db_service
from backend.logging.logger_service import logger_service
from backend.voice.voice_engine import voice_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ASTRA-HAR.Backend")

app = FastAPI(
    title="ASTRA-HAR API",
    description="Autonomous Space Experiment Activity Recognition & Sequence Validation API (ISRO PS-26174)",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scenario_engine = ScenarioEngine(scenario_name="normal")
execution_mode = "live"  # "live" for laptop webcam, "demo" for scenario generator

@app.on_event("startup")
async def startup_event():
    """Background loop pushing real-time WebSocket state updates."""
    logger.info("ASTRA-HAR Backend started successfully.")

    # Start live laptop camera worker by default
    camera_worker.start()

    asyncio.create_task(realtime_background_loop())

async def realtime_background_loop():
    """Async background task updating state and broadcasting over WebSockets at 25 Hz."""
    while True:
        try:
            if execution_mode == "demo":
                state_dict = scenario_engine.tick()
            else:
                state_dict = realtime_state.to_dict()

            # Broadcast state over WebSockets
            await ws_manager.broadcast_state(state_dict)
        except Exception as e:
            logger.error(f"Error in realtime background loop: {e}")
        await asyncio.sleep(0.04)  # ~25 Hz

# ==================== REST API ENDPOINTS ====================

@app.get("/api/system/status")
def get_system_status():
    return {
        "status": "ONLINE",
        "system_name": "ASTRA-HAR",
        "organization": "ISRO",
        "mode": execution_mode,
        "camera": realtime_state.camera_status,
        "fps": realtime_state.fps,
        "inference_latency_ms": realtime_state.inference_latency_ms,
        "cpu_usage": realtime_state.cpu_usage,
        "ram_usage_gb": realtime_state.ram_usage_gb,
        "gpu_usage": realtime_state.gpu_usage,
        "vram_usage_gb": realtime_state.vram_usage_gb,
        "mission_health_score": realtime_state.mission_health_score
    }

@app.get("/api/experiment/status")
def get_experiment_status():
    return realtime_state.to_dict()

@app.post("/api/experiment/start")
def start_experiment():
    realtime_state.is_running = True
    realtime_state.is_paused = False
    realtime_state.session_id = f"EXP_{int(time.time())}"
    db_service.log_session_start(realtime_state.session_id, realtime_state.experiment_id, realtime_state.total_steps)
    voice_manager.success("Experiment started. Position yourself facing the container.")
    return {"status": "SUCCESS", "session_id": realtime_state.session_id}

@app.post("/api/video/start")
def start_camera():
    global execution_mode
    execution_mode = "live"
    camera_worker.start()
    return {"status": "CAMERA_STARTED", "source": 0}

@app.post("/api/video/stop")
def stop_camera():
    camera_worker.stop()
    return {"status": "CAMERA_STOPPED"}

@app.post("/api/experiment/stop")
def stop_experiment():
    realtime_state.is_running = False
    voice_manager.speak("Experiment stopped.")
    return {"status": "STOPPED"}

@app.post("/api/experiment/reset")
def reset_experiment():
    realtime_state.current_step = 1
    realtime_state.step_progress = 0.0
    realtime_state.safety_state = "CONFIRMED"
    realtime_state.active_alert = None
    voice_manager.speak("Experiment sequence reset to step 1.")
    return {"status": "RESET"}

@app.get("/api/experiment/current-step")
def get_current_step():
    return {
        "current_step": realtime_state.current_step,
        "total_steps": realtime_state.total_steps,
        "step_name": realtime_state.step_name,
        "step_status": realtime_state.step_status,
        "progress_pct": realtime_state.step_progress,
        "next_step": realtime_state.next_step,
        "next_step_name": realtime_state.next_step_name,
        "guidance": realtime_state.next_step_guidance
    }

@app.get("/api/experiment/history")
def get_experiment_history():
    return db_service.get_session_history()

@app.get("/api/logs")
def get_logs():
    return {
        "session_id": realtime_state.session_id,
        "current_step": realtime_state.current_step,
        "active_alert": realtime_state.active_alert
    }

@app.get("/api/models/status")
def get_models_status():
    return {
        "detector": "LIVE (YOLO / Lightweight Edge)",
        "pose": "LIVE (MediaPipe / Normalized Keypoints)",
        "activity": "LIVE (LSTM Temporal Sequence Model)",
        "hmr_3d": "READY (3D Human Mesh Recovery Extension)",
        "device": "CUDA / Edge GPU Acceleration",
        "precision": "FP16",
        "p50_latency_ms": realtime_state.latency_p50,
        "p95_latency_ms": realtime_state.latency_p95,
        "p99_latency_ms": realtime_state.latency_p99
    }

@app.get("/api/config")
def get_config():
    return {
        "experiment_id": realtime_state.experiment_id,
        "experiment_name": realtime_state.experiment_name,
        "total_steps": realtime_state.total_steps,
        "fps_target": 30,
        "stream_url": "http://localhost:8000/video"
    }

# ==================== WEBSOCKET & VIDEO STREAM ====================

@app.websocket("/ws/experiment")
async def websocket_experiment_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.get("/video")
def video_feed():
    return StreamingResponse(
        stream_manager.generate_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
