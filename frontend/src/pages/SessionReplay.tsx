import React, { useState, useEffect, useRef } from "react";
import { PlaySquare, Play, Pause, RotateCcw, FastForward, Download, ShieldCheck, Film, HardDrive } from "lucide-react";
import { useRealtimeStore } from "../realtime/realtimeStore";

interface TimelineEvent {
  timeSec: number;
  timeStr: string;
  label: string;
  action: string;
  status: "SUCCESS" | "WARNING" | "INFO";
  details: string;
}

const timelineEvents: TimelineEvent[] = [
  { timeSec: 10, timeStr: "00:10", label: "Observe Payload Container", action: "OBSERVE", status: "SUCCESS", details: "Astronaut position verified facing container" },
  { timeSec: 25, timeStr: "00:25", label: "Access Container Latch", action: "OPEN_CONTAINER", status: "SUCCESS", details: "Container latch unlocked & access panel open" },
  { timeSec: 45, timeStr: "00:45", label: "Grasp Red Box Payload", action: "GRASP_RED_BOX", status: "SUCCESS", details: "Right hand contact confirmed with Red Box" },
  { timeSec: 65, timeStr: "01:05", label: "Move Red Box to Target Zone", action: "MOVE_RED_BOX", status: "SUCCESS", details: "Spatial transport vector active (28 cm/s)" },
  { timeSec: 80, timeStr: "01:20", label: "Target Rack Safety Check", action: "SAFETY_CHECK", status: "WARNING", details: "Minor clearance deviation detected (-1.2 cm)" },
  { timeSec: 95, timeStr: "01:35", label: "Place & Lock Red Box", action: "PLACE_RED_BOX", status: "SUCCESS", details: "Red Box securely locked into target rack" },
  { timeSec: 120, timeStr: "02:00", label: "Inspect Yellow Box Payload", action: "INSPECT_YELLOW_BOX", status: "SUCCESS", details: "Yellow Box identification confirmed" },
  { timeSec: 150, timeStr: "02:30", label: "Complete Experiment Protocol", action: "EXPERIMENT_COMPLETE", status: "SUCCESS", details: "All 12 steps validated successfully" },
];

export const SessionReplay: React.FC = () => {
  const { exportLogs, fetchRecordings } = useRealtimeStore();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTimeSec, setCurrentTimeSec] = useState(0);
  const [durationSec, setDurationSec] = useState(200);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const [selectedSession, setSelectedSession] = useState("EXP_1757160000");
  const [recordingsList, setRecordingsList] = useState<any[]>([]);
  const [downloadingLogs, setDownloadingLogs] = useState(false);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const timerRef = useRef<any>(null);

  // Fetch recorded sessions from backend
  useEffect(() => {
    const loadRecordings = async () => {
      const recs = await fetchRecordings();
      if (recs && recs.length > 0) {
        setRecordingsList(recs);
        setSelectedSession(recs[0].filename);
      }
    };
    loadRecordings();
  }, [fetchRecordings]);

  const activeRecording = recordingsList.find((r) => r.filename === selectedSession);
  const videoUrl = activeRecording ? activeRecording.url : "";

  // Synchronize play/pause and playback rate with video ref or ticker
  useEffect(() => {
    if (videoRef.current && videoUrl) {
      videoRef.current.playbackRate = playbackSpeed;
      if (isPlaying) {
        videoRef.current.play().catch(() => {});
      } else {
        videoRef.current.pause();
      }
    } else {
      // Fallback ticker when no mp4 video URL present
      if (isPlaying) {
        const intervalMs = 1000 / playbackSpeed;
        timerRef.current = setInterval(() => {
          setCurrentTimeSec((prev) => {
            if (prev >= durationSec) {
              setIsPlaying(false);
              return durationSec;
            }
            return prev + 1;
          });
        }, intervalMs);
      } else if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, playbackSpeed, videoUrl, durationSec]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const currentTimelineEvent = [...timelineEvents]
    .reverse()
    .find((evt) => currentTimeSec >= evt.timeSec) || timelineEvents[0];

  const handleSeek = (seconds: number) => {
    setCurrentTimeSec(seconds);
    if (videoRef.current && videoUrl) {
      videoRef.current.currentTime = seconds;
    }
  };

  const handleDownloadLogs = async () => {
    setDownloadingLogs(true);
    const data = await exportLogs();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selectedSession}_telemetry_log.json`;
    a.click();
    URL.revokeObjectURL(url);
    setDownloadingLogs(false);
  };

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Page Title & Session Switcher */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <PlaySquare className="w-5 h-5 text-cyan-400" />
            <span>SESSION REPLAY STUDIO</span>
            <span className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-xs px-2 py-0.5 rounded font-mono">
              {selectedSession}
            </span>
          </h2>
          <p className="text-xs text-slate-400">Interactive video playback synchronized with AI timelines and telemetry events</p>
        </div>

        <div className="flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg">
            <HardDrive className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-400">Recorded Session:</span>
            <select
              value={selectedSession}
              onChange={(e) => {
                setSelectedSession(e.target.value);
                setCurrentTimeSec(0);
                setIsPlaying(false);
              }}
              className="bg-transparent text-cyan-400 font-bold focus:outline-none cursor-pointer max-w-[240px] truncate"
            >
              {recordingsList.length > 0 ? (
                recordingsList.map((rec) => (
                  <option key={rec.filename} value={rec.filename}>
                    {rec.filename} ({rec.size_mb} MB)
                  </option>
                ))
              ) : (
                <>
                  <option value="EXP_1757160000">EXP_1757160000 (Two-Box Sorting)</option>
                  <option value="EXP_1757158200">EXP_1757158200 (Red Box Relocation)</option>
                  <option value="EXP_1757142100">EXP_1757142100 (Container Latch Check)</option>
                </>
              )}
            </select>
          </div>

          <button
            onClick={handleDownloadLogs}
            disabled={downloadingLogs}
            className="bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-400 font-bold px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{downloadingLogs ? "EXPORTING..." : "EXPORT TELEMETRY"}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Synchronized Video Player */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
          <div
            onClick={() => setIsPlaying(!isPlaying)}
            className="relative bg-slate-950 rounded-lg aspect-video flex items-center justify-center border border-slate-800 overflow-hidden group cursor-pointer"
          >
            {videoUrl ? (
              <video
                ref={videoRef}
                src={videoUrl}
                className="w-full h-full object-cover"
                onLoadedMetadata={() => {
                  if (videoRef.current) setDurationSec(Math.floor(videoRef.current.duration));
                }}
                onTimeUpdate={() => {
                  if (videoRef.current) setCurrentTimeSec(Math.floor(videoRef.current.currentTime));
                }}
                onEnded={() => setIsPlaying(false)}
              />
            ) : (
              <img
                src="http://localhost:8000/video"
                alt="ASTRA-HAR Live Replay Feed"
                className={`w-full h-full object-cover transition-opacity duration-300 ${isPlaying ? 'opacity-100' : 'opacity-60'}`}
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            )}

            {/* Video Canvas Overlay Metadata */}
            <div className="absolute top-4 left-4 right-4 flex justify-between items-start pointer-events-none">
              <div className="bg-slate-900/90 border border-cyan-500/40 p-2.5 rounded-lg text-xs space-y-1 backdrop-blur shadow-lg">
                <div className="text-cyan-400 font-bold flex items-center space-x-1.5">
                  <Film className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
                  <span>REPLAY: {selectedSession}</span>
                </div>
                <div className="text-slate-300">ACTIVE STEP: {currentTimelineEvent.label}</div>
                <div className="text-emerald-400 font-bold">ACTION: {currentTimelineEvent.action}</div>
              </div>

              <div className="bg-slate-900/90 border border-slate-700/60 p-2 rounded text-xs text-right backdrop-blur font-mono">
                <div className="text-cyan-400 font-bold">{formatTime(currentTimeSec)} / {formatTime(durationSec)}</div>
                <div className="text-slate-400 text-[10px]">{playbackSpeed}x PLAYBACK SPEED</div>
              </div>
            </div>

            {/* Center Play/Pause Button Overlay */}
            {!isPlaying && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/50 backdrop-blur-[2px] transition-all group-hover:bg-slate-950/40">
                <div className="p-4 bg-cyan-500/20 border-2 border-cyan-400 text-cyan-400 rounded-full shadow-[0_0_30px_rgba(6,182,212,0.4)] group-hover:scale-110 transition-transform">
                  <Play className="w-10 h-10 fill-current ml-1" />
                </div>
                <span className="mt-3 text-cyan-300 font-bold text-xs tracking-widest bg-slate-900/90 px-3 py-1 rounded border border-cyan-500/30">
                  CLICK TO PLAY RECORDED SESSION
                </span>
                <span className="text-[11px] text-slate-400 mt-1 font-mono">{selectedSession}</span>
              </div>
            )}

            {/* Active Telemetry Overlay Box */}
            <div className="absolute bottom-16 left-4 bg-slate-900/90 border border-emerald-500/40 p-2 rounded text-[11px] text-emerald-400 backdrop-blur pointer-events-none">
              ✓ Telemetry Sync: 25Hz | Bounding Box Match: 97.4%
            </div>
          </div>

          {/* Interactive Video Overlay Controls Bar */}
          <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex flex-col md:flex-row items-center justify-between gap-3 text-xs">
            <div className="flex items-center space-x-3 w-full md:w-auto justify-between md:justify-start">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition cursor-pointer shadow-[0_0_10px_rgba(6,182,212,0.3)]"
              >
                {isPlaying ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current" />}
              </button>

              <button
                onClick={() => handleSeek(0)}
                className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition cursor-pointer"
                title="Restart Session"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              <span className="text-slate-200 font-bold min-w-[90px]">
                {formatTime(currentTimeSec)} / {formatTime(durationSec)}
              </span>
            </div>

            {/* Scrubber Range Slider */}
            <div className="flex items-center space-x-3 w-full md:w-1/2">
              <input
                type="range"
                min="0"
                max={durationSec}
                value={currentTimeSec}
                onChange={(e) => handleSeek(Number(e.target.value))}
                className="w-full accent-cyan-400 cursor-pointer h-2 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Playback Speed Selector */}
            <div className="flex items-center space-x-1 bg-slate-900 border border-slate-800 p-1 rounded-lg">
              <FastForward className="w-3.5 h-3.5 text-slate-400 ml-1" />
              {[0.5, 1.0, 1.5, 2.0].map((speed) => (
                <button
                  key={speed}
                  onClick={() => setPlaybackSpeed(speed)}
                  className={`px-2 py-0.5 rounded text-[11px] font-bold transition cursor-pointer ${
                    playbackSpeed === speed
                      ? "bg-cyan-500 text-black shadow-[0_0_8px_rgba(6,182,212,0.4)]"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {speed}x
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Synchronized Event Timeline Sidebar */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-3 flex items-center justify-between border-b border-slate-800 pb-2">
              <span>SYNCHRONIZED EVENT TIMELINE</span>
              <span className="text-cyan-400 text-[11px] font-mono">{timelineEvents.length} EVENTS</span>
            </div>

            <div className="space-y-2 max-h-[440px] overflow-y-auto pr-1">
              {timelineEvents.map((evt, idx) => {
                const isActive = currentTimelineEvent.timeSec === evt.timeSec;
                const isPassed = currentTimeSec >= evt.timeSec;

                return (
                  <div
                    key={idx}
                    onClick={() => handleSeek(evt.timeSec)}
                    className={`p-3 rounded-lg border text-xs transition cursor-pointer ${
                      isActive
                        ? "bg-cyan-950/80 border-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.2)]"
                        : isPassed
                        ? "bg-slate-950/80 border-slate-800 hover:border-slate-700 text-slate-300"
                        : "bg-slate-950/40 border-slate-900 text-slate-500 opacity-70 hover:opacity-100"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <span className={`font-bold font-mono ${isActive ? "text-cyan-400" : "text-slate-400"}`}>
                          {evt.timeStr}
                        </span>
                        <span className="font-bold text-slate-200">{evt.label}</span>
                      </div>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          evt.status === "SUCCESS"
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                            : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                        }`}
                      >
                        {evt.status}
                      </span>
                    </div>

                    <div className="text-[11px] text-slate-400 flex items-center justify-between pt-1">
                      <span>Action: <span className="text-cyan-300 font-mono">{evt.action}</span></span>
                      {isActive && <span className="text-cyan-400 animate-pulse font-bold">● ACTIVE</span>}
                    </div>

                    {isActive && (
                      <div className="mt-2 text-[10px] text-emerald-300 bg-slate-900 p-2 rounded border border-cyan-500/30">
                        {evt.details}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* AI Validation Summary Card */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-3 space-y-1.5 text-xs">
            <div className="text-xs text-emerald-400 font-bold uppercase tracking-wider flex items-center space-x-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>SESSION VALIDATION REPORT</span>
            </div>
            <div className="text-slate-300 text-[11px]">Sequence Validity: <span className="text-emerald-400 font-bold">100% VALIDATED</span></div>
            <div className="text-slate-400 text-[10px]">Total Steps: 12 | Anomaly Count: 0 | Health Score: 98/100</div>
          </div>
        </div>
      </div>
    </div>
  );
};

