import sys
import os
import time
import cv2
import argparse
import uvicorn
import logging

# Ensure root path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.camera import CameraCapture
from app.inference import inference_pipeline
from app.dashboard import dashboard_hud
from app.recorder import app_recorder
from voice.offline_tts import offline_tts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ASTRA-HAR.RealtimeHAR")

def main():
    parser = argparse.ArgumentParser(description="ASTRA-HAR: Real-Time AI Human Activity Recognition for On-board BAS Experiments (SIH 2026 PS 26174)")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0 for laptop webcam)")
    parser.add_argument("--experiment", default="two_box_sorting", help="Experiment protocol name or path")
    parser.add_argument("--gui", action="store_true", help="Launch live standalone OpenCV HUD window display")
    parser.add_argument("--record", action="store_true", help="Record session video feed locally to recordings/")
    parser.add_argument("--host", default="0.0.0.0", help="REST & WebSocket API host IP")
    parser.add_argument("--port", type=int, default=8000, help="REST & WebSocket API server port")

    args = parser.parse_args()

    print("==========================================================================")
    print("      REAL-TIME AI HUMAN ACTIVITY RECOGNITION (HAR) - BAS PAYLOAD         ")
    print("      ISRO SIH 2026 - Problem Statement 26174: On-board Experiments       ")
    print("==========================================================================")
    print(f" Camera Source  : LAPTOP WEBCAM / USB CAMERA (INDEX {args.camera})")
    print(f" Experiment     : {args.experiment}")
    print(f" Mode           : 100% OFFLINE EDGE INFERENCE")
    print(f" GUI Overlay    : {'ENABLED' if args.gui else 'REST / WEBSOCKET DASHBOARD'}")
    print(f" REST & WS API  : http://{args.host}:{args.port}")
    print(f" Video Stream   : http://{args.host}:{args.port}/video")
    print("==========================================================================")

    offline_tts.speak("ASTRA HAR real-time activity recognition initialized.")

    if args.record:
        app_recorder.start_recording(inference_pipeline.session_id)

    if args.gui:
        logger.info("Opening live OpenCV camera capture & HUD display window...")
        cam = CameraCapture(source=args.camera)
        cam.open()

        try:
            while True:
                ret, frame = cam.read_frame()
                if not ret:
                    break

                res = inference_pipeline.process_frame(frame)
                annotated = dashboard_hud.render(frame, res)

                if app_recorder.is_recording:
                    app_recorder.write_frame(annotated)

                cv2.imshow("ASTRA-HAR :: Real-Time AI Experiment Monitor", annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nUser quit camera stream.")
                    break
        finally:
            cam.release()
            cv2.destroyAllWindows()
            if app_recorder.is_recording:
                app_recorder.stop_recording()
    else:
        logger.info("Starting REST API & WebSocket server for React scientific dashboard...")
        uvicorn.run("backend.main:app", host=args.host, port=args.port, reload=False)

if __name__ == "__main__":
    main()
