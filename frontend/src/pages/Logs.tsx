import React, { useState } from "react";
import { Terminal, Search, Download, CheckCircle } from "lucide-react";

export const Logs: React.FC = () => {
  const [filter, setFilter] = useState("");
  const [exported, setExported] = useState(false);

  const mockLogs = [
    { time: "2026-09-09T10:21:08.120", type: "STEP_COMPLETED", step: "STEP 1: Reach Red Box", conf: "94.7%", status: "SUCCESS" },
    { time: "2026-09-09T10:21:11.450", type: "STEP_COMPLETED", step: "STEP 2: Pick Red Box", conf: "96.2%", status: "SUCCESS" },
    { time: "2026-09-09T10:21:15.890", type: "STEP_COMPLETED", step: "STEP 3: Move Red Box", conf: "93.8%", status: "SUCCESS" },
    { time: "2026-09-09T10:21:19.230", type: "STEP_COMPLETED", step: "STEP 4: Place Red Box", conf: "95.1%", status: "SUCCESS" },
    { time: "2026-09-09T10:21:22.010", type: "EXPERIMENT_COMPLETE", step: "STEP 5: Release Red Box", conf: "97.4%", status: "COMPLETE" },
  ];

  const handleExportLogs = () => {
    fetch("http://localhost:8000/api/logs/export")
      .then(res => res.json())
      .then(data => {
        const blob = new Blob([data.experiment_log_text], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "experiment_log.txt";
        a.click();
        setExported(true);
        setTimeout(() => setExported(false), 3000);
      })
      .catch(console.error);
  };

  const filtered = mockLogs.filter(l =>
    l.step.toLowerCase().includes(filter.toLowerCase()) ||
    l.type.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-cyan-400" />
            <span>REAL-TIME SYSTEM EVENT LOGS & TELEMETRY</span>
          </h2>
          <p className="text-xs text-slate-400">Structured JSONL telemetry & AI decision explainability logs (100% offline)</p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search logs..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="bg-slate-900 border border-slate-800 text-xs text-white pl-9 pr-4 py-2 rounded-lg focus:outline-none focus:border-cyan-500"
            />
          </div>

          <button
            onClick={handleExportLogs}
            className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs px-4 py-2 rounded-lg flex items-center space-x-1.5 shadow-[0_0_10px_rgba(6,182,212,0.2)]"
          >
            <Download className="w-4 h-4" />
            <span>EXPORT MISSION REPORT</span>
          </button>
        </div>
      </div>

      {exported && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-4 py-2 rounded-lg text-xs flex items-center space-x-2 font-bold">
          <CheckCircle className="w-4 h-4" />
          <span>Structured Experiment Logs exported successfully (experiment_log.txt, events.jsonl, session.json)!</span>
        </div>
      )}

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase tracking-wider">
            <tr>
              <th className="p-3">Timestamp</th>
              <th className="p-3">Event Type</th>
              <th className="p-3">Step Details</th>
              <th className="p-3">AI Confidence</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {filtered.map((log, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40">
                <td className="p-3 text-slate-400 font-mono">{log.time}</td>
                <td className="p-3 font-bold text-cyan-400">{log.type}</td>
                <td className="p-3">{log.step}</td>
                <td className="p-3 text-emerald-400">{log.conf}</td>
                <td className="p-3">
                  <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
                    {log.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

