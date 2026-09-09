import React from "react";
import { useRealtimeStore } from "../realtime/realtimeStore";
import { Eye, Hand, Box, Activity } from "lucide-react";
import type { Interaction, ExperimentObject } from "../types";

export const LiveExperiment: React.FC = () => {
  const { state } = useRealtimeStore();

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Eye className="w-5 h-5 text-cyan-400" />
            <span>LIVE EXPERIMENT MONITORING</span>
          </h2>
          <p className="text-xs text-slate-400">Real-time computer vision inference & hand-object interaction state tracking</p>
        </div>
        <div className="flex space-x-2 text-xs">
          <span className="bg-slate-900 border border-slate-800 text-cyan-400 px-3 py-1.5 rounded">
            FPS: {state.camera.fps}
          </span>
          <span className="bg-slate-900 border border-slate-800 text-slate-300 px-3 py-1.5 rounded">
            Latency: {state.performance.total_latency_ms} ms
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Full-width Video Canvas View */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="relative bg-slate-950 rounded-lg aspect-video flex items-center justify-center overflow-hidden border border-slate-800">
            {/* Live Camera Feed Image Stream from Backend */}
            <img
              src="http://localhost:8000/video"
              alt="ASTRA-HAR Live Feed"
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLElement).style.display = "none";
              }}
            />

            {/* Fallback Overlay */}
            <div className="absolute inset-0 p-6 flex flex-col justify-between pointer-events-none">
              <div className="bg-slate-900/90 border border-cyan-500/40 p-2.5 rounded max-w-xs text-xs space-y-1 backdrop-blur">
                <div className="text-cyan-400 font-bold flex items-center space-x-1">
                  <Activity className="w-3.5 h-3.5" />
                  <span>ACTIVITY: {state.activity.current}</span>
                </div>
                <div className="text-slate-300">Confidence: {(state.activity.confidence * 100).toFixed(1)}%</div>
                <div className="text-emerald-400">Sequence Status: {state.validation.status}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Live Interaction & Object Telemetry Cards */}
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="text-xs text-slate-400 uppercase tracking-widest flex items-center space-x-1.5">
              <Hand className="w-4 h-4 text-cyan-400" />
              <span>HAND-OBJECT INTERACTION</span>
            </div>

            {state.interactions.map((inter: Interaction, idx: number) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg text-xs space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-slate-400">Target Object:</span>
                  <span className="text-cyan-400 font-bold">{inter.object_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Interaction State:</span>
                  <span className="text-emerald-400 font-bold">{inter.state}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Hand Distance:</span>
                  <span className="text-amber-400">{inter.distance_px} px</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Grasp Probability:</span>
                  <span className="text-cyan-300">{(inter.grasp_probability * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>

          {/* Experiment Objects Checklist */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="text-xs text-slate-400 uppercase tracking-widest flex items-center space-x-1.5">
              <Box className="w-4 h-4 text-indigo-400" />
              <span>TRACKED EXPERIMENT OBJECTS</span>
            </div>

            <div className="space-y-2 text-xs">
              {state.objects.map((obj: ExperimentObject) => (
                <div key={obj.id} className="bg-slate-950 border border-slate-800 p-2.5 rounded-lg flex items-center justify-between">
                  <div>
                    <div className="text-white font-bold">{obj.name}</div>
                    <div className="text-[10px] text-slate-400">Conf: {(obj.confidence * 100).toFixed(0)}%</div>
                  </div>
                  <span className="bg-slate-900 border border-slate-700 text-cyan-400 px-2 py-0.5 rounded text-[11px]">
                    {obj.state}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
