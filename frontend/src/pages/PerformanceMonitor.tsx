import React from "react";
import { Activity } from "lucide-react";
import { useRealtimeStore } from "../realtime/realtimeStore";

export const PerformanceMonitor: React.FC = () => {
  const { state } = useRealtimeStore();

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          <span>REAL-TIME PERFORMANCE MONITOR</span>
        </h2>
        <p className="text-xs text-slate-400">FPS, CPU, RAM, GPU, VRAM, and pipeline latency breakdowns</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-3">
          <div className="text-xs text-slate-400 uppercase font-bold flex justify-between">
            <span>CPU UTILIZATION</span>
            <span className="text-cyan-400">{state.system.cpu_percent}%</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden border border-slate-800">
            <div className="bg-cyan-500 h-full" style={{ width: `${state.system.cpu_percent}%` }} />
          </div>
          <div className="text-[11px] text-slate-400">RAM: {state.system.ram_percent}% (3.4 GB)</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-3">
          <div className="text-xs text-slate-400 uppercase font-bold flex justify-between">
            <span>GPU UTILIZATION</span>
            <span className="text-emerald-400">{state.system.gpu_percent}%</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden border border-slate-800">
            <div className="bg-emerald-500 h-full" style={{ width: `${state.system.gpu_percent}%` }} />
          </div>
          <div className="text-[11px] text-slate-400">Temp: {state.system.temperature}°C</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-3">
          <div className="text-xs text-slate-400 uppercase font-bold flex justify-between">
            <span>PIPELINE LATENCY</span>
            <span className="text-amber-400">{state.performance.total_latency_ms} ms</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden border border-slate-800">
            <div className="bg-amber-400 h-full" style={{ width: `${(state.performance.total_latency_ms / 150) * 100}%` }} />
          </div>
          <div className="text-[11px] text-slate-400">P95: {state.performance.p95_ms} ms | P99: {state.performance.p99_ms} ms</div>
        </div>
      </div>
    </div>
  );
};
