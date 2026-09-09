import React, { useState } from "react";
import { Terminal, Search } from "lucide-react";

export const Logs: React.FC = () => {
  const [filter, setFilter] = useState("");

  const mockLogs = [
    { time: "2026-09-06T12:30:10.120", type: "STEP_COMPLETED", step: "STEP 1: Observe Payload Container", conf: "0.96" },
    { time: "2026-09-06T12:30:14.920", type: "STEP_COMPLETED", step: "STEP 2: Access Container", conf: "0.95" },
    { time: "2026-09-06T12:30:17.820", type: "STEP_COMPLETED", step: "STEP 3: Identify Red Box", conf: "0.94" },
    { time: "2026-09-06T12:30:20.920", type: "STEP_COMPLETED", step: "STEP 4: Reach Red Box", conf: "0.93" },
    { time: "2026-09-06T12:30:25.420", type: "STEP_COMPLETED", step: "STEP 5: Grasp Red Box", conf: "0.94" },
  ];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-cyan-400" />
            <span>REAL-TIME SYSTEM EVENT LOGS</span>
          </h2>
          <p className="text-xs text-slate-400">Structured JSONL telemetry & AI decision explainability logs</p>
        </div>

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
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase tracking-wider">
            <tr>
              <th className="p-3">Timestamp</th>
              <th className="p-3">Event Type</th>
              <th className="p-3">Step Details</th>
              <th className="p-3 font-right">AI Confidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {mockLogs.map((log, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40">
                <td className="p-3 text-slate-400 font-mono">{log.time}</td>
                <td className="p-3 font-bold text-cyan-400">{log.type}</td>
                <td className="p-3">{log.step}</td>
                <td className="p-3 text-emerald-400">{log.conf}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
