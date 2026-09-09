import React from "react";
import { Settings } from "lucide-react";

export const SystemSettings: React.FC = () => {
  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Settings className="w-5 h-5 text-cyan-400" />
          <span>SYSTEM & HARDWARE SETTINGS</span>
        </h2>
        <p className="text-xs text-slate-400">Configure camera inputs, voice TTS parameters, recording options, and edge hardware options</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
        <div className="text-xs text-slate-400 uppercase tracking-widest font-bold">Offline Text-to-Speech (TTS) Voice Engine</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="text-slate-400 block mb-1">Voice Volume:</label>
            <input type="range" min="0" max="100" defaultValue="100" className="w-full accent-cyan-400" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Cooldown Duration (Seconds):</label>
            <input type="number" defaultValue={3.0} className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-white" />
          </div>
        </div>
      </div>
    </div>
  );
};
