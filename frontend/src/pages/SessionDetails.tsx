import React from "react";
import { FileText, CheckCircle2 } from "lucide-react";

export const SessionDetails: React.FC = () => {
  const stepsData = [
    { step: 1, name: "Observe Payload Container", conf: "96.4%", time: "00:03.2", status: "SUCCESS" },
    { step: 2, name: "Access Container", conf: "95.1%", time: "00:04.8", status: "SUCCESS" },
    { step: 3, name: "Identify Red Box", conf: "94.8%", time: "00:02.9", status: "SUCCESS" },
    { step: 4, name: "Reach Red Box", conf: "93.5%", time: "00:03.1", status: "SUCCESS" },
    { step: 5, name: "Grasp Red Box", conf: "94.2%", time: "00:04.5", status: "SUCCESS" },
    { step: 6, name: "Move Red Box", conf: "92.7%", time: "00:06.1", status: "SUCCESS" },
    { step: 7, name: "Place Red Box", conf: "96.0%", time: "00:03.8", status: "SUCCESS" },
  ];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <FileText className="w-5 h-5 text-cyan-400" />
          <span>SESSION DETAILS — EXP_1757160000</span>
        </h2>
        <p className="text-xs text-slate-400">Step breakdown, timing evidence, and confidence scores</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400">SESSION DURATION</div>
          <div className="text-lg font-bold text-white">00:04:12.84</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400">STEPS COMPLETED</div>
          <div className="text-lg font-bold text-emerald-400">12 / 12 (100%)</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400">MEAN CONFIDENCE</div>
          <div className="text-lg font-bold text-cyan-400">94.2%</div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="text-xs text-slate-400 uppercase tracking-widest font-bold">Step Evidence Breakdown</div>
        <div className="space-y-2">
          {stepsData.map((s) => (
            <div key={s.step} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between text-xs">
              <div className="flex items-center space-x-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span className="font-bold text-slate-200">STEP {s.step}: {s.name}</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-slate-400">Duration: {s.time}</span>
                <span className="text-cyan-400 font-bold">Conf: {s.conf}</span>
                <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded">
                  {s.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
