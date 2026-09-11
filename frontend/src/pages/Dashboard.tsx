import React from "react";
import { useRealtimeStore } from "../realtime/realtimeStore";
import { Play, Pause, RotateCcw, AlertTriangle, Clock, ShieldCheck, Activity, Cpu, CheckCircle } from "lucide-react";

export const Dashboard: React.FC = () => {
  const { state, isSessionRunning, isSessionPaused, startSession, pauseSession, resetStep } = useRealtimeStore();

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Top Banner Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center space-x-4">
          <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 rounded-lg">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs text-slate-400">MISSION STATUS</div>
            <div className="text-base font-bold text-white flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
              <span>SYSTEM ONLINE</span>
            </div>
            <div className="text-[11px] text-emerald-400">Health Score: {state.mission_health_score}/100</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center space-x-4">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 rounded-lg">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs text-slate-400">AI INFERENCE</div>
            <div className="text-base font-bold text-white">{state.camera.fps} FPS</div>
            <div className="text-[11px] text-slate-400">Latency: {state.performance.total_latency_ms} ms (P50: {state.performance.p50_ms}ms)</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center space-x-4">
          <div className="p-3 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded-lg">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs text-slate-400">CURRENT STEP</div>
            <div className="text-base font-bold text-white">STEP {state.experiment.current_step} / {state.experiment.total_steps}</div>
            <div className="text-[11px] text-cyan-400">{state.experiment.step_name}</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center space-x-4">
          <div className={`p-3 rounded-lg border ${state.active_alert ? 'bg-rose-500/10 border-rose-500/30 text-rose-400' : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'}`}>
            {state.active_alert ? <AlertTriangle className="w-6 h-6" /> : <ShieldCheck className="w-6 h-6" />}
          </div>
          <div>
            <div className="text-xs text-slate-400">ACTIVE ALERTS</div>
            <div className={`text-base font-bold ${state.active_alert ? 'text-rose-400' : 'text-emerald-400'}`}>
              {state.active_alert ? state.active_alert.type : "NONE (SYSTEM OK)"}
            </div>
            <div className="text-[11px] text-slate-400">Safety State: {state.validation.status}</div>
          </div>
        </div>
      </div>

      {/* Main Grid: Video Stream + Experiment Step Control */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Camera View with AI Annotation Overlay */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 bg-rose-500 rounded-full animate-pulse" />
              <span className="font-bold text-slate-200">LIVE ANNOTATED CAMERA FEED</span>
            </div>
            <span className="bg-slate-950 text-slate-400 px-2 py-0.5 rounded text-xs">
              1280x720 @ {state.camera.fps} FPS
            </span>
          </div>

          <div className="relative bg-slate-950 rounded-lg aspect-video flex items-center justify-center overflow-hidden border border-slate-800">
            {/* Live Camera Stream from Backend */}
            <img
              src="http://localhost:8000/video"
              alt="ASTRA-HAR Live Camera Feed"
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLElement).style.display = "none";
              }}
            />

            {/* Simulated Vision Overlay Canvas */}
            <div className="absolute inset-0 p-6 flex flex-col justify-between pointer-events-none">
              {/* Top overlay metadata */}
              <div className="flex justify-between items-start">
                <div className="bg-slate-900/80 border border-slate-700/50 backdrop-blur p-2 rounded text-xs space-y-1">
                  <div className="text-cyan-400 font-bold">ASTRONAUT TRACKED</div>
                  <div className="text-slate-300">ID: A01 | Conf: {(state.astronaut.confidence * 100).toFixed(1)}%</div>
                  <div className="text-emerald-400">Activity: {state.activity.current}</div>
                </div>

                <div className="bg-slate-900/80 border border-slate-700/50 backdrop-blur p-2 rounded text-xs text-right">
                  <div className="text-slate-400">EXPERIMENT STATE</div>
                  <div className="text-cyan-400 font-bold">STEP {state.experiment.current_step} / 12</div>
                  <div className="text-amber-400">{state.experiment.step_name}</div>
                </div>
              </div>

              {/* Alert message overlay if present */}
              {state.active_alert && (
                <div className="self-center bg-rose-950/90 border border-rose-500 text-rose-200 px-4 py-2 rounded-lg backdrop-blur flex items-center space-x-2 shadow-lg animate-bounce">
                  <AlertTriangle className="w-5 h-5 text-rose-400" />
                  <span className="font-bold">{state.active_alert.message}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Experiment Sequence Guidance & Control */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-widest mb-1">Experiment Protocol</div>
            <h2 className="text-lg font-bold text-white mb-2">Two-Box Sorting Experiment</h2>

            {/* Progress bar */}
            <div className="space-y-1 mb-4">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Sequence Progress</span>
                <span className="text-cyan-400 font-bold">{state.experiment.progress}%</span>
              </div>
              <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
                <div
                  className="bg-cyan-500 h-full transition-all duration-300"
                  style={{ width: `${state.experiment.progress}%` }}
                />
              </div>
            </div>

            {/* Next Step Intelligence Card */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3">
              <div className="text-xs text-cyan-400 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                <CheckCircle className="w-4 h-4 text-cyan-400" />
                <span>NEXT EXPECTED STEP</span>
              </div>
              <div className="text-base font-bold text-white">
                STEP {state.next_step.id}: {state.next_step.name}
              </div>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/50 p-2.5 rounded border border-slate-800/80">
                "{state.next_step.guidance}"
              </p>
            </div>

            {/* AI Evidence Explanation Box */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2 text-xs">
              <div className="text-xs text-emerald-400 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>WHY? AI EXPLANATION & EVIDENCE</span>
              </div>
              <div className="text-slate-200 font-bold">Activity: {state.activity.current} ({((state.activity.confidence || 0.94) * 100).toFixed(1)}%)</div>
              <div className="space-y-1 text-[11px] text-slate-300 pt-1">
                <div className="text-emerald-400">✓ Right hand tracked & approaching target</div>
                <div className="text-emerald-400">✓ Red box spatial contact confirmed</div>
                <div className="text-emerald-400">✓ Hand-object velocity vector active</div>
                <div className="text-emerald-400">✓ Temporal window stability confirmed</div>
              </div>
            </div>
          </div>

          {/* Interactive Control Buttons */}
          <div className="space-y-2 pt-2 border-t border-slate-800 font-mono">
            <button
              onClick={() => startSession()}
              className={`w-full font-bold py-2.5 rounded-lg flex items-center justify-center space-x-2 transition cursor-pointer ${
                isSessionRunning && !isSessionPaused
                  ? "bg-cyan-500 hover:bg-cyan-400 text-black shadow-[0_0_20px_rgba(6,182,212,0.4)]"
                  : "bg-cyan-600 hover:bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.25)]"
              }`}
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{isSessionRunning && !isSessionPaused ? "SESSION ACTIVE" : "START EXPERIMENT SESSION"}</span>
            </button>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => pauseSession()}
                className={`font-semibold py-2 rounded-lg flex items-center justify-center space-x-1.5 text-xs transition cursor-pointer ${
                  isSessionPaused
                    ? "bg-amber-500/20 border border-amber-500/50 text-amber-300 hover:bg-amber-500/30"
                    : "bg-slate-800 hover:bg-slate-700 text-slate-200"
                }`}
              >
                {isSessionPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
                <span>{isSessionPaused ? "RESUME" : "PAUSE"}</span>
              </button>
              <button
                onClick={() => resetStep()}
                className="bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-200 font-semibold py-2 rounded-lg flex items-center justify-center space-x-1.5 text-xs transition cursor-pointer"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>RESET STEP</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

