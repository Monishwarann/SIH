import { useEffect } from "react";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { useRealtimeStore } from "./realtime/realtimeStore";

import { Dashboard } from "./pages/Dashboard";
import { LiveExperiment } from "./pages/LiveExperiment";
import { ExperimentConfig } from "./pages/ExperimentConfig";
import { ExperimentHistory } from "./pages/ExperimentHistory";
import { SessionDetails } from "./pages/SessionDetails";
import { SessionReplay } from "./pages/SessionReplay";
import { AIModelStatus } from "./pages/AIModelStatus";
import { DatasetManagement } from "./pages/DatasetManagement";
import { NetworkStreaming } from "./pages/NetworkStreaming";
import { SystemSettings } from "./pages/SystemSettings";
import { Logs } from "./pages/Logs";
import { PerformanceMonitor } from "./pages/PerformanceMonitor";
import { SystemDiagnostics } from "./pages/SystemDiagnostics";

export function App() {
  const { activeTab, connectWebSocket } = useRealtimeStore();

  useEffect(() => {
    connectWebSocket();
  }, [connectWebSocket]);

  const renderContent = () => {
    switch (activeTab) {
      case "mission_control":
      case "dashboard":
        return <Dashboard />;
      case "live":
      case "ai_perception":
      case "object_tracking":
        return <LiveExperiment />;
      case "sequence":
      case "config":
        return <ExperimentConfig />;
      case "activity":
      case "ai_status":
      case "model_manager":
        return <AIModelStatus />;
      case "history":
        return <ExperimentHistory />;
      case "details":
        return <SessionDetails />;
      case "streaming":
        return <NetworkStreaming />;
      case "timeline":
      case "alerts":
      case "logs":
        return <Logs />;
      case "telemetry":
      case "performance":
        return <PerformanceMonitor />;
      case "dataset":
        return <DatasetManagement />;
      case "replay":
        return <SessionReplay />;
      case "diagnostics":
        return <SystemDiagnostics />;
      case "settings":
        return <SystemSettings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-mono selection:bg-cyan-500 selection:text-black">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-slate-950">{renderContent()}</main>
      </div>
    </div>
  );
}

export default App;
