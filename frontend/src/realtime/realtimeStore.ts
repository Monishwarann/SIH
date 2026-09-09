import { create } from "zustand";
import type { SystemState } from "../types";

interface RealtimeStore {
  state: SystemState;
  activeTab: string;
  wsConnected: boolean;
  wsError: string | null;
  scenario: string;

  setActiveTab: (tab: string) => void;
  setScenario: (scenario: string) => void;
  updateState: (newState: Partial<SystemState>) => void;
  connectWebSocket: () => void;
}

const defaultState: SystemState = {
  schema_version: "1.0",
  timestamp: new Date().toISOString(),
  unix_timestamp: Date.now() / 1000,
  session_id: "EXP-20260906-001",
  frame_id: 18452,
  sequence: 0,

  system: {
    status: "ONLINE",
    mode: "LIVE_AI",
    uptime: 5321,
    cpu_percent: 42.0,
    ram_percent: 58.0,
    gpu_percent: 67.0,
    temperature: 61.4
  },

  camera: {
    connected: true,
    fps: 29.7,
    resolution: "1280x720",
    brightness: 0.72,
    blur_score: 0.08,
    dropped_frames: 0
  },

  astronaut: {
    detected: true,
    track_id: 1,
    confidence: 0.97,
    position: { x: 0.48, y: 0.52 },
    bbox: [180, 100, 580, 680]
  },

  activity: {
    current: "OPEN_CONTAINER",
    confidence: 0.94,
    stable: true,
    duration_ms: 1250
  },

  objects: [
    { id: "main_container", class: "CONTAINER", name: "Main Container", confidence: 0.96, bbox: [120, 240, 420, 640], center: { x: 0.22, y: 0.57 }, track_id: 10, velocity: { vx: 0, vy: 0 }, state: "IN_CONTAINER", last_seen: Date.now() },
    { id: "red_box", class: "RED_BOX", name: "Red Box", confidence: 0.94, bbox: [160, 320, 260, 420], center: { x: 0.18, y: 0.47 }, track_id: 11, velocity: { vx: 0, vy: 0 }, state: "IN_CONTAINER", last_seen: Date.now() },
    { id: "yellow_box", class: "YELLOW_BOX", name: "Yellow Box", confidence: 0.93, bbox: [280, 320, 380, 420], center: { x: 0.27, y: 0.47 }, track_id: 12, velocity: { vx: 0, vy: 0 }, state: "IN_CONTAINER", last_seen: Date.now() },
    { id: "target_area", class: "TARGET_RACK", name: "Target Rack", confidence: 0.95, bbox: [750, 200, 1050, 600], center: { x: 0.77, y: 0.52 }, track_id: 13, velocity: { vx: 0, vy: 0 }, state: "EMPTY", last_seen: Date.now() }
  ],
  hands: {
    right_hand: { position: [420, 410], velocity: [0.02, -0.01], tracked: true }
  },
  interactions: [
    { hand: "RIGHT", object: "main_container", object_name: "Main Container", state: "APPROACHING", contact: true, grasp_probability: 0.94, distance_px: 38.0, duration_ms: 840 }
  ],

  experiment: {
    status: "RUNNING",
    current_step: 1,
    total_steps: 12,
    step_name: "Observe Payload Container",
    progress: 8.3,
    expected_action: "OPEN_CONTAINER"
  },

  validation: {
    status: "CONFIRMED",
    sequence_valid: true
  },

  next_step: {
    id: 2,
    name: "Access Container",
    description: "Open main container access latch",
    guidance: "Position yourself facing the main payload container.",
    confidence: 0.92
  },

  alerts: [],
  active_alert: null,
  recovery_action: null,

  performance: {
    inference_ms: 34,
    tracking_ms: 7,
    sequence_ms: 2,
    total_latency_ms: 43,
    p50_ms: 44.0,
    p95_ms: 67.0,
    p99_ms: 91.0,
    fps: 29.7
  },

  camera_status: "CONNECTED",
  model_status: "LIVE",
  mission_health_score: 96
};

export const useRealtimeStore = create<RealtimeStore>((set, get) => ({
  state: defaultState,
  activeTab: "mission_control",
  wsConnected: false,
  wsError: null,
  scenario: "normal",

  setActiveTab: (tab: string) => set({ activeTab: tab }),
  setScenario: (scenario: string) => set({ scenario }),
  updateState: (newState: Partial<SystemState>) => set((s) => ({ state: { ...s.state, ...newState } })),

  connectWebSocket: () => {
    const wsUrl = `ws://${window.location.hostname}:8000/ws/experiment`;
    let ws: WebSocket | null = null;

    try {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        set({ wsConnected: true, wsError: null });
        console.log("[ASTRA-HAR WS] Real-time telemetry WebSocket connected.");
      };

      ws.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          if (parsed.type === "STATE_UPDATE" && parsed.data) {
            set((s) => ({ state: { ...s.state, ...parsed.data } }));
          }
        } catch (err) {
          console.error("[ASTRA-HAR WS] Error parsing message:", err);
        }
      };

      ws.onerror = () => {
        set({ wsConnected: false, wsError: "WebSocket error" });
      };

      ws.onclose = () => {
        set({ wsConnected: false });
        setTimeout(() => get().connectWebSocket(), 3000);
      };
    } catch {
      set({ wsConnected: false, wsError: "Connection failed" });
    }
  }
}));
