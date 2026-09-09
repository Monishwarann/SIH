import React from "react";
import { Sliders, Save, FileCode } from "lucide-react";

export const ExperimentConfig: React.FC = () => {
  const yamlContent = `experiment:
  id: "two_box_sorting"
  name: "Two-Box Sorting Experiment"
  author: "ISRO Bio-Astronautics Division"

objects:
  - id: "main_container"
    name: "Main Container"
  - id: "red_box"
    name: "Red Box"
  - id: "yellow_box"
    name: "Yellow Box"
  - id: "target_area"
    name: "Target Rack"

steps:
  - id: 1
    name: "Observe Payload Container"
    expected_object: "main_container"
    expected_activity: "OPEN_CONTAINER"
    timeout_sec: 30.0
    confidence_threshold: 0.70

  - id: 2
    name: "Access Container"
    expected_object: "main_container"
    expected_activity: "OPEN_CONTAINER"
    timeout_sec: 30.0

  - id: 3
    name: "Identify Red Box"
    expected_object: "red_box"
    expected_activity: "IDENTIFY_OBJECT"
    timeout_sec: 25.0`;

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Sliders className="w-5 h-5 text-cyan-400" />
            <span>EXPERIMENT CONFIGURATION</span>
          </h2>
          <p className="text-xs text-slate-400">Declarative YAML experiment protocol editor (zero code modification required)</p>
        </div>
        <button className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-4 py-2 rounded-lg flex items-center space-x-1.5 font-bold shadow-[0_0_10px_rgba(6,182,212,0.2)]">
          <Save className="w-4 h-4" />
          <span>SAVE CONFIGURATION</span>
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="flex items-center justify-between text-xs border-b border-slate-800 pb-2 text-slate-400">
          <div className="flex items-center space-x-2">
            <FileCode className="w-4 h-4 text-cyan-400" />
            <span className="font-bold text-white">experiments/two_box_experiment.yaml</span>
          </div>
          <span>Declarative FSM Schema v1.0</span>
        </div>

        <textarea
          defaultValue={yamlContent}
          className="w-full h-96 bg-slate-950 text-cyan-300 font-mono text-xs p-4 rounded-lg border border-slate-800 focus:outline-none focus:border-cyan-500/50 leading-relaxed"
        />
      </div>
    </div>
  );
};
