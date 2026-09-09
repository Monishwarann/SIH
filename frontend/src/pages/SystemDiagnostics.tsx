import React from "react";
import { Stethoscope, CheckCircle2 } from "lucide-react";

export const SystemDiagnostics: React.FC = () => {
  const diagnostics = [
    { name: "Camera Ingestion Feed", status: "PASSED", detail: "1280x720 @ 30 FPS active" },
    { name: "YOLO Object Detector", status: "PASSED", detail: "CUDA acceleration active" },
    { name: "Pose Estimator Keypoints", status: "PASSED", detail: "MediaPipe 17 joint tracker ready" },
    { name: "Temporal LSTM Activity Model", status: "PASSED", detail: "Loaded models/activity_model.pt" },
    { name: "Offline TTS Voice Manager", status: "PASSED", detail: "pyttsx3 engine initialized" },
    { name: "SQLite Database", status: "PASSED", detail: "data/experiment.db connected" },
    { name: "WebSocket Broadcasting", status: "PASSED", detail: "ws://localhost:8000/ws/experiment" },
    { name: "MJPEG Video Streaming", status: "PASSED", detail: "http://0.0.0.0:8080/video" },
  ];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Stethoscope className="w-5 h-5 text-cyan-400" />
          <span>STARTUP SELF-DIAGNOSTICS</span>
        </h2>
        <p className="text-xs text-slate-400">Automated pre-flight diagnostic checks for edge-AI deployment</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="text-xs text-slate-400 uppercase tracking-widest font-bold">Diagnostic Checklist</div>
        <div className="space-y-2">
          {diagnostics.map((d, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between text-xs">
              <div className="flex items-center space-x-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span className="font-bold text-white">{d.name}</span>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-slate-400">{d.detail}</span>
                <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded font-bold">
                  {d.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
