import React, { useState } from "react";
import { Sliders, Save, FileCode, Download, CheckCircle } from "lucide-react";

export const ExperimentConfig: React.FC = () => {
  const [yamlContent, setYamlContent] = useState(`experiment:
  id: "box_sorting_v1"
  name: "Box Sorting Experiment Protocol"
  organization: "ISRO Bio-Astronautics Division"
  mode: "100% OFFLINE EDGE INFERENCE"

objects:
  - id: "main_container"
    name: "Main Container"
  - id: "red_box"
    name: "Red Box"
  - id: "yellow_box"
    name: "Yellow Box"
  - id: "target_rack"
    name: "Target Payload Rack"

steps:
  - step: 1
    name: "Observe Payload Container"
    expected_activity: "OPEN_CONTAINER"
    target_object: "main_container"
    timeout_sec: 30.0

  - step: 2
    name: "Reach Toward Red Box"
    expected_activity: "REACH_RED_BOX"
    target_object: "red_box"
    timeout_sec: 25.0

  - step: 3
    name: "Grasp Red Box"
    expected_activity: "PICK_RED_BOX"
    target_object: "red_box"
    timeout_sec: 20.0

  - step: 4
    name: "Move Red Box to Target Rack"
    expected_activity: "MOVE_RED_BOX"
    target_object: "red_box"
    timeout_sec: 25.0

  - step: 5
    name: "Place Red Box into Target Slot"
    expected_activity: "PLACE_RED_BOX"
    target_object: "target_rack"
    timeout_sec: 20.0

  - step: 6
    name: "Release Red Box & Return Hand"
    expected_activity: "RELEASE_RED_BOX"
    target_object: "red_box"
    timeout_sec: 15.0
`);

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    fetch("http://localhost:8000/api/experiments/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: "box_sorting_v1",
        name: "Box Sorting Experiment Protocol",
        steps: [
          { name: "Observe Payload Container", activity: "OPEN_CONTAINER" },
          { name: "Reach Toward Red Box", activity: "REACH_RED_BOX" },
          { name: "Grasp Red Box", activity: "PICK_RED_BOX" },
          { name: "Move Red Box to Target Rack", activity: "MOVE_RED_BOX" },
          { name: "Place Red Box into Target Slot", activity: "PLACE_RED_BOX" },
          { name: "Release Red Box & Return Hand", activity: "RELEASE_RED_BOX" }
        ]
      })
    })
      .then(() => {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      })
      .catch(console.error);
  };

  const handleDownloadYaml = () => {
    const blob = new Blob([yamlContent], { type: "text/yaml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "experiment_protocol.yaml";
    a.click();
  };

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Sliders className="w-5 h-5 text-cyan-400" />
            <span>DECLARATIVE EXPERIMENT PROTOCOL EDITOR</span>
          </h2>
          <p className="text-xs text-slate-400">Configure experiment sequence steps, object classes, and interaction thresholds (100% offline)</p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleDownloadYaml}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-4 py-2 rounded-lg flex items-center space-x-1.5 font-bold"
          >
            <Download className="w-4 h-4" />
            <span>EXPORT PROTOCOL YAML</span>
          </button>
          <button
            onClick={handleSave}
            className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-4 py-2 rounded-lg flex items-center space-x-1.5 font-bold shadow-[0_0_10px_rgba(6,182,212,0.2)]"
          >
            <Save className="w-4 h-4" />
            <span>SAVE PROTOCOL</span>
          </button>
        </div>
      </div>

      {saved && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-4 py-2 rounded-lg text-xs flex items-center space-x-2 font-bold">
          <CheckCircle className="w-4 h-4" />
          <span>Experiment Protocol saved successfully! Loaded into runtime FSM.</span>
        </div>
      )}

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="flex items-center justify-between text-xs border-b border-slate-800 pb-2 text-slate-400">
          <div className="flex items-center space-x-2">
            <FileCode className="w-4 h-4 text-cyan-400" />
            <span className="font-bold text-white">experiments/box_sorting_v1.yaml</span>
          </div>
          <span className="text-emerald-400">STATUS: VALID FSM PROTOCOL</span>
        </div>

        <textarea
          value={yamlContent}
          onChange={(e) => setYamlContent(e.target.value)}
          className="w-full h-96 bg-slate-950 text-cyan-300 font-mono text-xs p-4 rounded-lg border border-slate-800 focus:outline-none focus:border-cyan-500/50 leading-relaxed"
        />
      </div>
    </div>
  );
};

