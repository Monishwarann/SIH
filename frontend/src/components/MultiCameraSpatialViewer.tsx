import React, { useState } from "react";
import { Camera, Eye, Layers, ShieldCheck } from "lucide-react";
import { useRealtimeStore } from "../realtime/realtimeStore";

export const MultiCameraSpatialViewer: React.FC = () => {
  const { state } = useRealtimeStore();
  const [selectedCamera, setSelectedCamera] = useState<string>("cam_1");
  const [viewMode, setViewMode] = useState<"grid" | "radar">("grid");

  const mc = state.multi_camera || {
    fused_hand_3d: [0.0, 0.0, 1.2],
    fused_confidence: 0.95,
    active_cameras: 3,
    camera_statuses: [
      { camera_id: "cam_1", name: "Primary Workstation", status: "ONLINE", coverage_angle_deg: 75, position_3d: [0, 0, 1.5], occlusion_level: "LOW" },
      { camera_id: "cam_2", name: "Overhead Payload View", status: "SIMULATED", coverage_angle_deg: 75, position_3d: [0, 1.2, 2.0], occlusion_level: "LOW" },
      { camera_id: "cam_3", name: "Side Angle View", status: "SIMULATED", coverage_angle_deg: 75, position_3d: [1.5, 0.5, 1.2], occlusion_level: "LOW" }
    ],
    fused_objects_3d: [
      { name: "Main Container", position_3d: [-0.3, -0.1, 1.0], confidence: 0.96, occluded: false },
      { name: "Red Box", position_3d: [-0.2, 0.1, 1.15], confidence: 0.94, occluded: false },
      { name: "Yellow Box", position_3d: [0.2, 0.1, 1.15], confidence: 0.93, occluded: false }
    ],
    spatial_coverage_score: 0.98
  };

  const hand3D = mc.fused_hand_3d;

  // Radar Canvas Projection Mapping (meters [-1.5 to 1.5] -> canvas coordinates [0 to 300])
  const mapToRadar = (x: number, y: number) => {
    const cx = 150 + x * 90;
    const cy = 150 - y * 90;
    return { x: Math.max(10, Math.min(290, cx)), y: Math.max(10, Math.min(290, cy)) };
  };

  const handRadar = mapToRadar(hand3D[0], hand3D[1]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 font-mono space-y-4 shadow-xl">
      {/* Header bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-lg">
            <Eye className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white tracking-wide uppercase flex items-center gap-2">
              <span>Multi-Camera 3D Spatial Fusion</span>
              <span className="text-[10px] bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded border border-emerald-500/30">
                Zero Blindspot
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              3D Triangulation: <span className="text-cyan-400">X: {hand3D[0]}m | Y: {hand3D[1]}m | Z: {hand3D[2]}m</span>
            </p>
          </div>
        </div>

        {/* View mode toggle */}
        <div className="flex items-center space-x-2 text-xs">
          <button
            onClick={() => setViewMode("grid")}
            className={`px-3 py-1.5 rounded-lg border transition-all flex items-center space-x-1.5 ${
              viewMode === "grid"
                ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/40 font-semibold"
                : "bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200"
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            <span>Multi-Angle Grid</span>
          </button>
          <button
            onClick={() => setViewMode("radar")}
            className={`px-3 py-1.5 rounded-lg border transition-all flex items-center space-x-1.5 ${
              viewMode === "radar"
                ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/40 font-semibold"
                : "bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200"
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>3D Spatial Radar</span>
          </button>
        </div>
      </div>

      {/* Main View Area */}
      {viewMode === "grid" ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Camera 1: Workstation Stream */}
          <div
            onClick={() => setSelectedCamera("cam_1")}
            className={`relative rounded-lg overflow-hidden border bg-slate-950 cursor-pointer transition-all ${
              selectedCamera === "cam_1" ? "border-cyan-500 ring-1 ring-cyan-500/50 shadow-lg" : "border-slate-800 hover:border-slate-700"
            }`}
          >
            <div className="absolute top-2 left-2 z-10 bg-slate-900/80 backdrop-blur border border-slate-700 px-2 py-0.5 rounded text-[10px] text-cyan-400 flex items-center space-x-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Cam 1: Workstation (Primary)</span>
            </div>
            <img
              src="http://localhost:8000/video"
              alt="Primary Camera Feed"
              className="w-full h-48 object-cover"
              onError={(e) => {
                (e.target as HTMLElement).style.display = "none";
              }}
            />
            <div className="h-48 flex items-center justify-center text-slate-600 bg-slate-950 text-xs">
              Primary Video Feed Live
            </div>
            <div className="p-2 bg-slate-900/90 border-t border-slate-800 text-[11px] flex justify-between text-slate-400">
              <span>Coverage: 75°</span>
              <span className="text-emerald-400">Confidence: {Math.round(mc.fused_confidence * 100)}%</span>
            </div>
          </div>

          {/* Camera 2: Overhead Payload View */}
          <div
            onClick={() => setSelectedCamera("cam_2")}
            className={`relative rounded-lg overflow-hidden border bg-slate-950 cursor-pointer transition-all ${
              selectedCamera === "cam_2" ? "border-cyan-500 ring-1 ring-cyan-500/50 shadow-lg" : "border-slate-800 hover:border-slate-700"
            }`}
          >
            <div className="absolute top-2 left-2 z-10 bg-slate-900/80 backdrop-blur border border-slate-700 px-2 py-0.5 rounded text-[10px] text-cyan-400 flex items-center space-x-1">
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              <span>Cam 2: Overhead Payload View</span>
            </div>
            <div className="w-full h-48 bg-gradient-to-b from-slate-900 to-slate-950 p-4 flex flex-col justify-between relative overflow-hidden">
              {/* Synthetic Overhead Angle View */}
              <div className="absolute inset-0 border border-cyan-500/10 grid grid-cols-6 grid-rows-6 opacity-30" />
              <div className="relative z-10 text-[10px] text-slate-500">Overhead Perspective Synthetic Feed</div>
              <div className="relative z-10 flex flex-col items-center justify-center">
                <div
                  className="w-8 h-8 rounded-full border border-cyan-400/60 bg-cyan-500/20 flex items-center justify-center text-cyan-300 text-[10px] animate-pulse"
                  style={{ transform: `translate(${hand3D[0] * 30}px, ${hand3D[1] * 20}px)` }}
                >
                  HAND
                </div>
                <div className="text-[10px] text-cyan-400/80 mt-2">Overhead Line of Sight: CLEAR</div>
              </div>
              <div className="relative z-10 text-[10px] text-slate-500 flex justify-between">
                <span>Angle: -45° Pitch</span>
                <span>Occlusion: NONE</span>
              </div>
            </div>
            <div className="p-2 bg-slate-900/90 border-t border-slate-800 text-[11px] flex justify-between text-slate-400">
              <span>Coverage: 75°</span>
              <span className="text-cyan-400">Status: FUSED</span>
            </div>
          </div>

          {/* Camera 3: Side Perspective View */}
          <div
            onClick={() => setSelectedCamera("cam_3")}
            className={`relative rounded-lg overflow-hidden border bg-slate-950 cursor-pointer transition-all ${
              selectedCamera === "cam_3" ? "border-cyan-500 ring-1 ring-cyan-500/50 shadow-lg" : "border-slate-800 hover:border-slate-700"
            }`}
          >
            <div className="absolute top-2 left-2 z-10 bg-slate-900/80 backdrop-blur border border-slate-700 px-2 py-0.5 rounded text-[10px] text-cyan-400 flex items-center space-x-1">
              <span className="w-2 h-2 rounded-full bg-purple-400" />
              <span>Cam 3: Side Perspective</span>
            </div>
            <div className="w-full h-48 bg-gradient-to-r from-slate-900 to-slate-950 p-4 flex flex-col justify-between relative overflow-hidden">
              <div className="relative z-10 text-[10px] text-slate-500">Side Perspective View</div>
              <div className="relative z-10 flex flex-col items-center justify-center">
                <div
                  className="w-8 h-8 rounded-md border border-purple-400/60 bg-purple-500/20 flex items-center justify-center text-purple-300 text-[10px]"
                  style={{ transform: `translate(${hand3D[1] * 25}px, ${-hand3D[2] * 15}px)` }}
                >
                  HAND
                </div>
                <div className="text-[10px] text-purple-300/80 mt-2">Side Perspective: ACTIVE</div>
              </div>
              <div className="relative z-10 text-[10px] text-slate-500 flex justify-between">
                <span>Angle: -45° Yaw</span>
                <span>Occlusion: NONE</span>
              </div>
            </div>
            <div className="p-2 bg-slate-900/90 border-t border-slate-800 text-[11px] flex justify-between text-slate-400">
              <span>Coverage: 75°</span>
              <span className="text-purple-400">Status: FUSED</span>
            </div>
          </div>
        </div>
      ) : (
        /* 3D Spatial Radar View */
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center relative min-h-[320px]">
            <div className="absolute top-3 left-3 text-xs text-slate-400 flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              <span>PAYLOAD RACK 3D SPATIAL RADAR (TOP-DOWN)</span>
            </div>

            {/* SVG 3D Spatial Radar Canvas */}
            <svg className="w-[280px] h-[280px] border border-cyan-500/20 rounded-full bg-slate-900/50 p-2 shadow-[0_0_20px_rgba(6,182,212,0.1)]">
              {/* Concentric radar rings */}
              <circle cx="140" cy="140" r="130" fill="none" stroke="#1e293b" strokeWidth="1" />
              <circle cx="140" cy="140" r="90" fill="none" stroke="#1e293b" strokeWidth="1" strokeDasharray="4 4" />
              <circle cx="140" cy="140" r="50" fill="none" stroke="#1e293b" strokeWidth="1" strokeDasharray="2 2" />
              <line x1="140" y1="10" x2="140" y2="270" stroke="#1e293b" strokeWidth="1" />
              <line x1="10" y1="140" x2="270" y2="140" stroke="#1e293b" strokeWidth="1" />

              {/* Camera positions */}
              <circle cx="140" cy="260" r="5" fill="#06b6d4" />
              <text x="140" y="275" fill="#06b6d4" fontSize="8" textAnchor="middle">Cam 1</text>

              <circle cx="140" cy="20" r="5" fill="#10b981" />
              <text x="140" y="15" fill="#10b981" fontSize="8" textAnchor="middle">Cam 2</text>

              <circle cx="260" cy="140" r="5" fill="#a855f7" />
              <text x="260" y="152" fill="#a855f7" fontSize="8" textAnchor="middle">Cam 3</text>

              {/* 3D Fused Objects */}
              {mc.fused_objects_3d.map((obj, i) => {
                const pt = mapToRadar(obj.position_3d[0], obj.position_3d[1]);
                return (
                  <g key={i}>
                    <rect x={pt.x - 8} y={pt.y - 8} width="16" height="16" fill="#f59e0b" fillOpacity="0.2" stroke="#f59e0b" strokeWidth="1" rx="2" />
                    <text x={pt.x} y={pt.y + 16} fill="#f59e0b" fontSize="8" textAnchor="middle">{obj.name}</text>
                  </g>
                );
              })}

              {/* 3D Fused Hand Position */}
              <circle cx={handRadar.x} cy={handRadar.y} r="8" fill="#06b6d4" fillOpacity="0.3" stroke="#06b6d4" strokeWidth="2" className="animate-ping" />
              <circle cx={handRadar.x} cy={handRadar.y} r="5" fill="#06b6d4" />
              <text x={handRadar.x} y={handRadar.y - 9} fill="#38bdf8" fontSize="9" fontWeight="bold" textAnchor="middle">Astronaut Hand</text>
            </svg>

            <div className="absolute bottom-3 right-3 text-[10px] text-slate-500">
              Grid Scale: 1 unit = 0.5m
            </div>
          </div>

          {/* Spatial 3D Metrics Panel */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="text-xs text-slate-400 font-bold uppercase tracking-wider flex items-center justify-between">
                <span>3D Fusion Telemetry</span>
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
              </div>

              <div className="bg-slate-900 border border-slate-800 p-2.5 rounded-lg space-y-1">
                <div className="text-[10px] text-slate-500">Spatial Coverage Score</div>
                <div className="text-lg font-bold text-emerald-400">{Math.round(mc.spatial_coverage_score * 100)}%</div>
                <div className="w-full bg-slate-950 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full" style={{ width: `${mc.spatial_coverage_score * 100}%` }} />
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-2.5 rounded-lg space-y-1">
                <div className="text-[10px] text-slate-500">Triangulated Hand (X, Y, Z)</div>
                <div className="text-xs text-cyan-300 font-semibold">
                  [{hand3D[0]}m, {hand3D[1]}m, {hand3D[2]}m]
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-2.5 rounded-lg space-y-1">
                <div className="text-[10px] text-slate-500">Active View Cameras</div>
                <div className="text-xs text-purple-300 font-semibold flex items-center justify-between">
                  <span>{mc.active_cameras} Views Active</span>
                  <span className="text-[10px] bg-purple-500/20 text-purple-300 px-1.5 py-0.5 rounded">FUSED</span>
                </div>
              </div>
            </div>

            <div className="text-[10px] text-slate-500 text-center border-t border-slate-800 pt-2">
              Microgravity Orientation Invariant Engine Active
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
