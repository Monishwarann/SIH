import React, { useState } from "react";
import { Database, Play, Square, Video, Cpu, Download, CheckCircle, AlertTriangle, Layers, Plus, RefreshCw, BarChart2 } from "lucide-react";

export const DatasetManagement: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"create" | "record" | "dataset" | "train" | "export">("record");

  // Create Experiment Form State
  const [expName, setExpName] = useState("Box Sorting Experiment");
  const [expId, setExpId] = useState("EXP_BOX_SORTING_01");
  const [cameraSource, setCameraSource] = useState("0");
  const [resolution, setResolution] = useState("1280x720");
  const [fps, setFps] = useState(30);

  // Recording State
  const [selectedActivity, setSelectedActivity] = useState("PICK_RED_BOX");
  const [personId, setPersonId] = useState("Astronaut_01");
  const [isRecording, setIsRecording] = useState(false);
  const [samplesCount, setSamplesCount] = useState(24);
  const [recTimeSec, setRecTimeSec] = useState(12);

  // Training State
  const [isTraining, setIsTraining] = useState(false);
  const [trainingEpoch] = useState(50);
  const [currentEpoch] = useState(50);
  const [trainLoss, setTrainLoss] = useState(0.118);
  const [trainAccuracy, setTrainAccuracy] = useState(96.2);
  const [isModelExported, setIsModelExported] = useState(false);

  const handleStartRecording = () => {
    setIsRecording(true);
    fetch("http://localhost:8000/api/dataset/record/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ activity: selectedActivity, person_id: personId })
    }).catch(console.error);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    setSamplesCount(prev => prev + 1);
    fetch("http://localhost:8000/api/dataset/record/stop", { method: "POST" }).catch(console.error);
  };

  const handleGenerateDataset = () => {
    fetch("http://localhost:8000/api/dataset/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    })
      .then(res => res.json())
      .then(data => alert(`Dataset generated: ${data.details.splits.train_count} train samples, ${data.details.splits.val_count} val samples.`))
      .catch(console.error);
  };

  const handleStartTraining = () => {
    setIsTraining(true);
    fetch("http://localhost:8000/api/training/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ epochs: trainingEpoch })
    })
      .then(res => res.json())
      .then(data => {
        setIsTraining(false);
        setTrainLoss(data.results.final_loss);
        setTrainAccuracy(roundPct(data.results.final_accuracy));
      })
      .catch(() => setIsTraining(false));
  };

  const handleExportModel = () => {
    fetch("http://localhost:8000/api/training/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accuracy: trainAccuracy / 100, epochs: trainingEpoch })
    })
      .then(res => res.json())
      .then(() => setIsModelExported(true))
      .catch(console.error);
  };

  const roundPct = (val: number) => Math.round(val * 1000) / 10;

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <span>EXPERIMENT TRAINING STUDIO</span>
          </h2>
          <p className="text-xs text-slate-400">Record sample videos, generate sequence datasets, train offline AI activity models & export for edge runtime</p>
        </div>

        {/* Workflow Step Navigation Tabs */}
        <div className="flex items-center space-x-1 bg-slate-900 border border-slate-800 p-1 rounded-xl text-xs">
          <button
            onClick={() => setActiveTab("create")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${activeTab === "create" ? "bg-cyan-500 text-black shadow" : "text-slate-400 hover:text-white"}`}
          >
            1. CREATE EXP
          </button>
          <button
            onClick={() => setActiveTab("record")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${activeTab === "record" ? "bg-cyan-500 text-black shadow" : "text-slate-400 hover:text-white"}`}
          >
            2. RECORD SAMPLES
          </button>
          <button
            onClick={() => setActiveTab("dataset")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${activeTab === "dataset" ? "bg-cyan-500 text-black shadow" : "text-slate-400 hover:text-white"}`}
          >
            3. DATASET MANAGER
          </button>
          <button
            onClick={() => setActiveTab("train")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${activeTab === "train" ? "bg-cyan-500 text-black shadow" : "text-slate-400 hover:text-white"}`}
          >
            4. TRAIN AI
          </button>
          <button
            onClick={() => setActiveTab("export")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${activeTab === "export" ? "bg-cyan-500 text-black shadow" : "text-slate-400 hover:text-white"}`}
          >
            5. EXPORT MODEL
          </button>
        </div>
      </div>

      {/* TAB 1: CREATE EXPERIMENT */}
      {activeTab === "create" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="text-xs text-cyan-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Plus className="w-4 h-4 text-cyan-400" />
            <span>Create New Experiment Protocol</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Experiment Name:</label>
              <input
                type="text"
                value={expName}
                onChange={e => setExpName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-slate-400 block mb-1">Experiment ID:</label>
              <input
                type="text"
                value={expId}
                onChange={e => setExpId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-slate-400 block mb-1">Camera Source:</label>
              <select
                value={cameraSource}
                onChange={e => setCameraSource(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="0">Laptop Webcam (Index 0)</option>
                <option value="1">USB External Space Camera (Index 1)</option>
                <option value="recordings/sample.mp4">Local Video File (MP4)</option>
              </select>
            </div>
            <div>
              <label className="text-slate-400 block mb-1">Target Video Resolution & FPS:</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={resolution}
                  onChange={e => setResolution(e.target.value)}
                  className="w-1/2 bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
                />
                <input
                  type="number"
                  value={fps}
                  onChange={e => setFps(Number(e.target.value))}
                  className="w-1/2 bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
            </div>
          </div>

          <div className="pt-2">
            <button
              onClick={() => {
                fetch("http://localhost:8000/api/experiments/create", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ name: expName, id: expId, camera_source: cameraSource, resolution, fps })
                });
                alert("Experiment Created!");
                setActiveTab("record");
              }}
              className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2.5 px-6 rounded-lg text-xs flex items-center space-x-2 shadow-[0_0_15px_rgba(6,182,212,0.25)]"
            >
              <CheckCircle className="w-4 h-4" />
              <span>SAVE & PROCEED TO SAMPLE RECORDING</span>
            </button>
          </div>
        </div>
      )}

      {/* TAB 2: RECORD TRAINING SAMPLES */}
      {activeTab === "record" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <div className="flex items-center space-x-2">
                <span className={`w-2.5 h-2.5 rounded-full ${isRecording ? "bg-rose-500 animate-ping" : "bg-emerald-400"}`} />
                <span className="font-bold text-slate-200">SAMPLE RECORDING CAMERA STUDIO</span>
              </div>
              <span className="bg-slate-950 text-slate-400 px-2 py-0.5 rounded text-xs">
                {isRecording ? "● RECORDING LIVE" : "READY"}
              </span>
            </div>

            <div className="relative bg-slate-950 rounded-lg aspect-video flex items-center justify-center overflow-hidden border border-slate-800">
              <img
                src="http://localhost:8000/video"
                alt="Camera Live Stream"
                className="w-full h-full object-cover"
                onError={(e) => { (e.target as HTMLElement).style.display = "none"; }}
              />
              <div className="absolute top-4 left-4 bg-slate-900/90 border border-slate-700/60 p-2.5 rounded-lg text-xs space-y-1 backdrop-blur">
                <div className="text-cyan-400 font-bold">Target Activity: {selectedActivity}</div>
                <div className="text-slate-300">Recorded Time: 00:{recTimeSec < 10 ? `0${recTimeSec}` : recTimeSec}</div>
                <div className="text-emerald-400">Total Samples: {samplesCount}</div>
              </div>
            </div>

            {/* Recording Controls */}
            <div className="grid grid-cols-3 gap-3">
              <button
                disabled={isRecording}
                onClick={handleStartRecording}
                className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-2 text-xs shadow-[0_0_10px_rgba(16,185,129,0.2)]"
              >
                <Play className="w-4 h-4" />
                <span>[START] RECORD</span>
              </button>
              <button
                disabled={!isRecording}
                onClick={handleStopRecording}
                className="bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white font-bold py-2.5 rounded-lg flex items-center justify-center space-x-2 text-xs shadow-[0_0_10px_rgba(239,68,68,0.2)]"
              >
                <Square className="w-4 h-4" />
                <span>[STOP] SAVE SAMPLE</span>
              </button>
              <button
                onClick={() => setRecTimeSec(0)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2.5 rounded-lg flex items-center justify-center space-x-2 text-xs"
              >
                <RefreshCw className="w-4 h-4" />
                <span>[RETAKE] RESET</span>
              </button>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4 text-xs">
            <div className="text-slate-400 uppercase tracking-widest font-bold flex items-center space-x-2">
              <Video className="w-4 h-4 text-cyan-400" />
              <span>Sample Configuration</span>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-slate-400 block mb-1">Target Activity Label:</label>
                <select
                  value={selectedActivity}
                  onChange={e => setSelectedActivity(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
                >
                  <option value="REACH_RED_BOX">REACH_RED_BOX</option>
                  <option value="PICK_RED_BOX">PICK_RED_BOX</option>
                  <option value="MOVE_RED_BOX">MOVE_RED_BOX</option>
                  <option value="PLACE_RED_BOX">PLACE_RED_BOX</option>
                  <option value="RELEASE_RED_BOX">RELEASE_RED_BOX</option>
                  <option value="REACH_YELLOW_BOX">REACH_YELLOW_BOX</option>
                  <option value="PICK_YELLOW_BOX">PICK_YELLOW_BOX</option>
                  <option value="MOVE_YELLOW_BOX">MOVE_YELLOW_BOX</option>
                  <option value="PLACE_YELLOW_BOX">PLACE_YELLOW_BOX</option>
                  <option value="RELEASE_YELLOW_BOX">RELEASE_YELLOW_BOX</option>
                  <option value="RETURN_HAND">RETURN_HAND</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Person / Operator ID:</label>
                <input
                  type="text"
                  value={personId}
                  onChange={e => setPersonId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2.5 rounded text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg space-y-2">
                <div className="text-slate-400 font-bold uppercase">Recorded Samples List</div>
                <div className="space-y-1 text-[11px] text-slate-300">
                  <div className="flex justify-between"><span>PICK_RED_BOX (Person 1)</span><span className="text-emerald-400">Sample 001 ✓</span></div>
                  <div className="flex justify-between"><span>PICK_RED_BOX (Person 1)</span><span className="text-emerald-400">Sample 002 ✓</span></div>
                  <div className="flex justify-between"><span>PICK_RED_BOX (Person 2)</span><span className="text-emerald-400">Sample 003 ✓</span></div>
                  <div className="flex justify-between"><span>MOVE_RED_BOX (Person 1)</span><span className="text-emerald-400">Sample 004 ✓</span></div>
                  <div className="flex justify-between"><span>PLACE_RED_BOX (Person 2)</span><span className="text-emerald-400">Sample 005 ✓</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: DATASET GENERATOR */}
      {activeTab === "dataset" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div className="text-xs text-cyan-400 uppercase tracking-widest font-bold flex items-center space-x-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span>Dataset Generator & Splitter (70% Train / 15% Val / 15% Test)</span>
            </div>
            <button
              onClick={handleGenerateDataset}
              className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2 px-4 rounded-lg text-xs flex items-center space-x-2 shadow-[0_0_10px_rgba(6,182,212,0.2)]"
            >
              <RefreshCw className="w-4 h-4" />
              <span>GENERATE DATASET PIPELINE</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">TOTAL SAMPLES</div>
              <div className="text-2xl font-bold text-white">1,240</div>
              <div className="text-[11px] text-cyan-400">42,500 Extracted Frames</div>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">TRAINING (70%)</div>
              <div className="text-2xl font-bold text-emerald-400">868</div>
              <div className="text-[11px] text-slate-400">Grouped by session ID</div>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">VALIDATION (15%)</div>
              <div className="text-2xl font-bold text-amber-400">186</div>
              <div className="text-[11px] text-slate-400">Zero data leakage</div>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">TEST (15%)</div>
              <div className="text-2xl font-bold text-indigo-400">186</div>
              <div className="text-[11px] text-slate-400">Evaluation benchmark</div>
            </div>
          </div>

          {/* Dataset Quality Warnings */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2 text-xs">
            <div className="text-slate-400 font-bold uppercase">Dataset Balance & Quality Inspection</div>
            <div className="space-y-1 text-slate-300">
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span>MOVE_RED_BOX sequence samples balanced (240 samples)</span>
              </div>
              <div className="flex items-center space-x-2 text-amber-400">
                <AlertTriangle className="w-4 h-4" />
                <span>PICK_RED_BOX has slight variation imbalance across lighting conditions</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: TRAIN AI MODEL */}
      {activeTab === "train" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div className="text-xs text-cyan-400 uppercase tracking-widest font-bold flex items-center space-x-2">
              <BarChart2 className="w-4 h-4 text-cyan-400" />
              <span>Offline AI Model Training Studio (Temporal Transformer / LSTM)</span>
            </div>
            <button
              disabled={isTraining}
              onClick={handleStartTraining}
              className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-bold py-2.5 px-6 rounded-lg text-xs flex items-center space-x-2 shadow-[0_0_15px_rgba(16,185,129,0.25)]"
            >
              <Cpu className="w-4 h-4" />
              <span>{isTraining ? "TRAINING IN PROGRESS..." : "[ TRAIN AI MODEL ]"}</span>
            </button>
          </div>

          {/* Training Epoch Progress */}
          <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
            <div className="flex justify-between text-xs">
              <span className="text-slate-400">Epoch {currentEpoch} / {trainingEpoch}</span>
              <span className="text-emerald-400 font-bold">Loss: {trainLoss} | Accuracy: {trainAccuracy}%</span>
            </div>
            <div className="w-full bg-slate-900 h-3 rounded-full overflow-hidden border border-slate-800">
              <div className="bg-emerald-500 h-full transition-all duration-300" style={{ width: `${(currentEpoch / trainingEpoch) * 100}%` }} />
            </div>
          </div>

          {/* Model Metrics Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">PRECISION</div>
              <div className="text-xl font-bold text-cyan-400">96.5%</div>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">RECALL</div>
              <div className="text-xl font-bold text-emerald-400">95.8%</div>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
              <div className="text-slate-400">F1 SCORE</div>
              <div className="text-xl font-bold text-indigo-400">96.1%</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: EXPORT MODEL */}
      {activeTab === "export" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="text-xs text-cyan-400 uppercase tracking-widest font-bold flex items-center space-x-2">
            <Download className="w-4 h-4 text-cyan-400" />
            <span>Export Model for 100% Offline Edge Execution</span>
          </div>

          <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2 text-xs">
            <div className="font-bold text-white">Target Output Folder: <span className="text-cyan-400">models/</span></div>
            <div className="grid grid-cols-2 gap-2 text-slate-300 pt-2">
              <div>✓ activity_model.pt (PyTorch Weights)</div>
              <div>✓ activity_model.onnx (ONNX Optimized)</div>
              <div>✓ labels.json (Activity Class Mapping)</div>
              <div>✓ preprocessing.json (Feature Configuration)</div>
              <div>✓ model_metadata.json (Execution Specs)</div>
            </div>
          </div>

          <div className="pt-2">
            <button
              onClick={handleExportModel}
              className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-8 rounded-lg text-xs flex items-center space-x-2 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
            >
              <Download className="w-4 h-4" />
              <span>EXPORT MODEL ARTIFACTS</span>
            </button>
            {isModelExported && (
              <div className="mt-3 text-xs text-emerald-400 flex items-center space-x-2 font-bold">
                <CheckCircle className="w-4 h-4" />
                <span>Model artifacts exported successfully to models/ for 100% offline execution!</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

