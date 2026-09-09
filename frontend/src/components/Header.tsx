import React, { useEffect, useState } from "react";
import { useRealtimeStore } from "../realtime/realtimeStore";
import { Radio, Cpu, Camera } from "lucide-react";

export const Header: React.FC = () => {
  const { state, wsConnected, scenario, setScenario } = useRealtimeStore();
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-slate-900/90 border-b border-slate-800 backdrop-blur px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      {/* Title & Organization Branding */}
      <div className="flex items-center space-x-4">
        <div className="bg-cyan-950 border border-cyan-500/30 text-cyan-400 p-2 rounded-lg flex items-center justify-center font-bold tracking-widest text-lg shadow-[0_0_15px_rgba(6,182,212,0.2)]">
          ISRO
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-lg font-bold tracking-wider text-white">ASTRA-HAR</h1>
            <span className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-[10px] uppercase tracking-widest px-2 py-0.5 rounded font-mono">
              ON-BOARD BAS
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            Autonomous Space Experiment Activity Recognition & Sequence Validation (PS-26174)
          </p>
        </div>
      </div>

      {/* Demo Scenario Selector & Real-Time Indicators */}
      <div className="flex items-center space-x-6 font-mono text-xs">
        <div className="flex items-center space-x-2 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-md">
          <span className="text-slate-400">Scenario:</span>
          <select
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="bg-transparent text-cyan-400 font-semibold focus:outline-none cursor-pointer"
          >
            <option value="normal">Normal Execution</option>
            <option value="skip">Step Skipped Anomaly</option>
            <option value="wrong-object">Wrong Object Interaction</option>
            <option value="out-of-sequence">Out-of-Sequence Error</option>
            <option value="timeout">Step Timeout Warning</option>
            <option value="low-confidence">Low AI Confidence</option>
            <option value="camera-loss">Camera Loss (Astronaut Lost)</option>
            <option value="model-failure">Model Inference Failure</option>
          </select>
        </div>

        {/* Real-time status indicators */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1.5">
            <Camera className={`w-3.5 h-3.5 ${state.camera_status === 'CONNECTED' ? 'text-emerald-400' : 'text-rose-400'}`} />
            <span className="text-slate-300">CAM:</span>
            <span className={state.camera_status === 'CONNECTED' ? 'text-emerald-400' : 'text-rose-400'}>{state.camera_status}</span>
          </div>

          <div className="flex items-center space-x-1.5">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-300">AI:</span>
            <span className="text-cyan-400">{state.model_status}</span>
          </div>

          <div className="flex items-center space-x-1.5">
            <Radio className={`w-3.5 h-3.5 ${wsConnected ? 'text-emerald-400 animate-pulse' : 'text-amber-400'}`} />
            <span className="text-slate-300">WS:</span>
            <span className={wsConnected ? 'text-emerald-400' : 'text-amber-400'}>{wsConnected ? 'LIVE (25Hz)' : 'RECONNECTING'}</span>
          </div>
        </div>

        {/* Clock */}
        <div className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-md text-slate-300">
          <span className="text-cyan-400 font-bold">{currentTime.toLocaleTimeString()}</span>
          <span className="text-slate-500 ml-1">UTC+5:30</span>
        </div>
      </div>
    </header>
  );
};
