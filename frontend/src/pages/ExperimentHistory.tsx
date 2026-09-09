import React from "react";
import { History, Download, FileText } from "lucide-react";

export const ExperimentHistory: React.FC = () => {
  const mockSessions = [
    { id: "EXP_1757160000", date: "2026-09-06 12:30:10", status: "COMPLETED", steps: "12 / 12", errors: 0, conf: "94.2%" },
    { id: "EXP_1757156400", date: "2026-09-06 11:30:00", status: "COMPLETED", steps: "12 / 12", errors: 1, conf: "91.8%" },
    { id: "EXP_1757152800", date: "2026-09-06 10:30:00", status: "ABORTED", steps: "5 / 12", errors: 2, conf: "88.5%" },
  ];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <History className="w-5 h-5 text-cyan-400" />
          <span>EXPERIMENT HISTORY</span>
        </h2>
        <p className="text-xs text-slate-400">Past astronaut session logs, JSON/TXT reports, and metrics</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase tracking-wider">
            <tr>
              <th className="p-4">Session ID</th>
              <th className="p-4">Start Time</th>
              <th className="p-4">Status</th>
              <th className="p-4">Steps Completed</th>
              <th className="p-4">Anomalies</th>
              <th className="p-4">Avg Confidence</th>
              <th className="p-4 text-right">Reports</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {mockSessions.map((session) => (
              <tr key={session.id} className="hover:bg-slate-800/40">
                <td className="p-4 font-bold text-cyan-400">{session.id}</td>
                <td className="p-4 text-slate-400">{session.date}</td>
                <td className="p-4">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${session.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'}`}>
                    {session.status}
                  </span>
                </td>
                <td className="p-4">{session.steps}</td>
                <td className="p-4">{session.errors}</td>
                <td className="p-4 text-amber-400">{session.conf}</td>
                <td className="p-4 text-right space-x-2">
                  <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded text-xs inline-flex items-center space-x-1">
                    <FileText className="w-3.5 h-3.5" />
                    <span>JSON</span>
                  </button>
                  <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded text-xs inline-flex items-center space-x-1">
                    <Download className="w-3.5 h-3.5" />
                    <span>TXT</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
