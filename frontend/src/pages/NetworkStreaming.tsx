import React from "react";
import { Wifi, Radio, Server } from "lucide-react";
import { useRealtimeStore } from "../realtime/realtimeStore";

export const NetworkStreaming: React.FC = () => {
  const { wsConnected } = useRealtimeStore();

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Wifi className="w-5 h-5 text-cyan-400" />
          <span>NETWORK & IP VIDEO STREAMING</span>
        </h2>
        <p className="text-xs text-slate-400">Configure local HTTP MJPEG streaming endpoints, RTSP forwarding, and WebSocket connections</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyan-400" />
            <span>HTTP MJPEG Video Streaming Endpoint</span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Stream Target URL:</span>
              <span className="text-cyan-400 font-bold">http://0.0.0.0:8080/video</span>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Streaming FPS:</span>
              <span className="text-emerald-400 font-bold">25.0 FPS</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Server className="w-4 h-4 text-emerald-400" />
            <span>WebSocket Telemetry Stream</span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Endpoint:</span>
              <span className="text-cyan-400 font-bold">ws://localhost:8000/ws/experiment</span>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex justify-between items-center">
              <span className="text-slate-400">Connection Status:</span>
              <span className={`font-bold ${wsConnected ? 'text-emerald-400' : 'text-amber-400'}`}>
                {wsConnected ? 'CONNECTED (25 Hz)' : 'RECONNECTING'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
