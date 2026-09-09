import React from "react";
import { useRealtimeStore } from "../realtime/realtimeStore";
import {
  LayoutDashboard,
  Video,
  Eye,
  Sliders,
  Box,
  Activity,
  ListOrdered,
  AlertTriangle,
  BarChart3,
  Database,
  Cpu,
  PlaySquare,
  Stethoscope,
  Settings
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const { activeTab, setActiveTab } = useRealtimeStore();

  const menuItems = [
    { id: "mission_control", label: "Mission Control", icon: LayoutDashboard },
    { id: "live", label: "Live Experiment", icon: Video },
    { id: "ai_perception", label: "AI Perception", icon: Eye },
    { id: "sequence", label: "Sequence Validation", icon: Sliders },
    { id: "object_tracking", label: "Object Tracking", icon: Box },
    { id: "activity", label: "Activity Recognition", icon: Activity },
    { id: "timeline", label: "Event Timeline", icon: ListOrdered },
    { id: "alerts", label: "Alerts & Recovery", icon: AlertTriangle },
    { id: "telemetry", label: "Telemetry", icon: BarChart3 },
    { id: "dataset", label: "Dataset Manager", icon: Database },
    { id: "model_manager", label: "Model Manager", icon: Cpu },
    { id: "replay", label: "Session Replay", icon: PlaySquare },
    { id: "diagnostics", label: "System Diagnostics", icon: Stethoscope },
    { id: "settings", label: "Settings", icon: Settings }
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col justify-between h-[calc(100vh-61px)] font-mono text-xs sticky top-[61px]">
      <div className="space-y-1 overflow-y-auto">
        <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest px-3 mb-2">
          Payload Operations (14 Views)
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-2.5 px-3 py-2 rounded-lg transition-all text-left ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-semibold shadow-[0_0_10px_rgba(6,182,212,0.15)]"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-cyan-400" : "text-slate-500"}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="border-t border-slate-800 pt-3 px-3 text-[11px] text-slate-500 space-y-1">
        <div className="flex justify-between">
          <span>Target FPS:</span>
          <span className="text-slate-300">30.0</span>
        </div>
        <div className="flex justify-between">
          <span>Pipeline Latency:</span>
          <span className="text-cyan-400">&lt;65 ms</span>
        </div>
        <div className="flex justify-between">
          <span>Deployment:</span>
          <span className="text-emerald-400">100% Offline Edge</span>
        </div>
      </div>
    </aside>
  );
};
