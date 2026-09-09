import React from "react";
import { Database, Play, Square, Tag, Sparkles } from "lucide-react";

export const DatasetManagement: React.FC = () => {
  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Database className="w-5 h-5 text-cyan-400" />
          <span>DATASET RECORDING & SYNTHETIC GENERATOR</span>
        </h2>
        <p className="text-xs text-slate-400">Record custom experiment video sequences, annotate activity steps, and generate synthetic visual data</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Tag className="w-4 h-4 text-cyan-400" />
            <span>Dataset Sequence Recorder</span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Sequence Label:</label>
              <input
                type="text"
                defaultValue="normal_two_box_sorting_01"
                className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <button className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-1.5 shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                <Play className="w-4 h-4" />
                <span>START RECORDING</span>
              </button>
              <button className="bg-rose-600 hover:bg-rose-500 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-1.5 shadow-[0_0_10px_rgba(239,68,68,0.2)]">
                <Square className="w-4 h-4" />
                <span>STOP & SAVE</span>
              </button>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>Synthetic Augmentation Generator</span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Number of Synthetic Samples:</label>
              <input
                type="number"
                defaultValue={100}
                className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            <button className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-1.5 shadow-[0_0_10px_rgba(99,102,241,0.2)]">
              <Sparkles className="w-4 h-4" />
              <span>GENERATE SYNTHETIC AUGMENTATIONS</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
