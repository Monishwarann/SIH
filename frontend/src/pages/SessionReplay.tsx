import React, { useState } from "react";
import { PlaySquare, Play, Pause } from "lucide-react";

export const SessionReplay: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(35);

  const timelineEvents = [
    { time: "00:10", label: "Observe Container", status: "SUCCESS" },
    { time: "00:25", label: "Access Container", status: "SUCCESS" },
    { time: "00:45", label: "Grasp Red Box", status: "SUCCESS" },
    { time: "01:05", label: "Move Red Box", status: "SUCCESS" },
    { time: "01:20", label: "Target Zone Check", status: "WARNING" },
    { time: "01:35", label: "Place Red Box", status: "SUCCESS" },
  ];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <PlaySquare className="w-5 h-5 text-cyan-400" />
          <span>SESSION REPLAY STUDIO — EXP_1757160000</span>
        </h2>
        <p className="text-xs text-slate-400">Interactive video playback synchronized with AI timelines and telemetry events</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Synchronized Video Player */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="relative bg-slate-950 rounded-lg aspect-video flex items-center justify-center border border-slate-800">
            <div className="text-slate-500 text-sm font-bold flex flex-col items-center">
              <PlaySquare className="w-12 h-12 mb-2 text-cyan-400 opacity-60" />
              <span>RECORDED EXPERIMENT SESSION VIDEO</span>
              <span className="text-xs text-slate-600">experiment_20260906_123010.mp4</span>
            </div>

            {/* Video overlay controls */}
            <div className="absolute bottom-4 left-4 right-4 bg-slate-900/90 border border-slate-700/60 backdrop-blur p-3 rounded-lg flex items-center justify-between text-xs">
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="p-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg"
                >
                  {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                </button>
                <span className="text-slate-300">01:05 / 03:20</span>
              </div>

              <input
                type="range"
                min="0"
                max="100"
                value={progress}
                onChange={(e) => setProgress(Number(e.target.value))}
                className="w-1/2 accent-cyan-400 cursor-pointer"
              />

              <div className="text-cyan-400 font-bold">1.0x SPEED</div>
            </div>
          </div>
        </div>

        {/* Synchronized Timeline Events */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold">Synchronized Event Timeline</div>
          <div className="space-y-2">
            {timelineEvents.map((evt, idx) => (
              <div
                key={idx}
                className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between text-xs hover:border-cyan-500/40 cursor-pointer"
              >
                <div>
                  <div className="text-cyan-400 font-bold">{evt.time}</div>
                  <div className="text-slate-200">{evt.label}</div>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${evt.status === 'SUCCESS' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'}`}>
                  {evt.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
