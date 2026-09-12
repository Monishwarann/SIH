import sys
import os
import argparse
import uvicorn
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.camera import CameraCapture
from app.inference import inference_pipeline
from app.dashboard import dashboard_hud
from app.recorder import app_recorder

logger = logging.getLogger("ASTRA-HAR.AppMain")

def run_app():
    parser = argparse.ArgumentParser(description="ASTRA-HAR: Offline Real-Time AI Human Activity Recognition System (SIH 2026 PS 26174)")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (0 for laptop webcam)")
    parser.add_argument("--gui", action="store_true", help="Launch standalone OpenCV HUD window")
    parser.add_argument("--host", default="0.0.0.0", help="FastAPI host IP")
    parser.add_argument("--port", type=int, default=8000, help="FastAPI port")

    args = parser.parse_args()

    print("==========================================================================")
    print("                ASTRA-HAR OFFLINE HAR EXPERIMENT MONITOR                  ")
    print("          ISRO SIH 2026 - Problem Statement 26174 (BAS Payload)           ")
    print("==========================================================================")

    if args.gui:
        print("\n[!] Launching Standalone OpenCV Real-Time HUD Dashboard window...\n")
        cam = CameraCapture(source=args.camera)
        cam.open()
        import cv2

        while True:
            ret, frame = cam.read_frame()
            if not ret:
                break
            res = inference_pipeline.process_frame(frame)
            annotated = dashboard_hud.render(frame, res)
            cv2.imshow("ASTRA-HAR :: Real-Time AI Experiment Monitor", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
    else:
        print(f"\n[!] Starting FastAPI REST & WebSocket Backend Server on http://{args.host}:{args.port}\n")
        uvicorn.run("backend.main:app", host=args.host, port=args.port, reload=False)

if __name__ == "__main__":
    run_app()
