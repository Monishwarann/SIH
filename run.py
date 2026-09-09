import sys
import argparse
import uvicorn
import logging

def main():
    parser = argparse.ArgumentParser(description="ASTRA-HAR: Autonomous Space Experiment Activity Recognition & Sequence Validation System (ISRO PS-26174)")
    parser.add_argument("--demo", action="store_true", help="Launch in Demonstration Mode with simulated camera & activity telemetry")
    parser.add_argument("--mode", choices=["live", "demo"], default="live", help="Execution mode ('live' for laptop camera ingestion, 'demo' for simulation)")
    parser.add_argument("--scenario", default="normal", help="Failure-injection scenario for demo mode ('normal', 'skip', 'wrong-object', 'out-of-sequence', 'timeout', 'low-confidence', 'camera-loss', 'model-failure')")
    parser.add_argument("--host", default="0.0.0.0", help="Backend host IP address")
    parser.add_argument("--port", type=int, default=8000, help="Backend API & WebSocket server port")
    parser.add_argument("--config", default="config/config.yaml", help="Path to system configuration YAML file")

    args = parser.parse_args()

    mode = "demo" if args.demo else args.mode

    print("==========================================================================")
    print("                     ASTRA-HAR SYSTEM INITIALIZATION                      ")
    print("      ISRO SIH 2026 - Problem Statement 26174: On-board BAS HAR           ")
    print("==========================================================================")
    print(f" Execution Mode : {mode.upper()} MODE")
    print(f" Camera Source  : LAPTOP WEBCAM (INDEX 0)")
    print(f" Demo Scenario  : {args.scenario}")
    print(f" Config File    : {args.config}")
    print(f" REST API & WS  : http://{args.host}:{args.port}")
    print(f" Video Stream   : http://{args.host}:{args.port}/video")
    print("==========================================================================")

    if mode == "live":
        print("\n[!] LIVE CAMERA INGESTION ACTIVE: Capturing live webcam feed & running real-time AI vision pipeline.\n")
    else:
        print("\n[!] DEMONSTRATION MODE ACTIVE: Pushing real-time space experiment simulation data.\n")

    uvicorn.run("backend.main:app", host=args.host, port=args.port, reload=False)

if __name__ == "__main__":
    main()
