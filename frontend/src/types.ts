export interface ExperimentObject {
  id: string;
  class: string;
  name: string;
  confidence: number;
  bbox: [number, number, number, number];
  center: { x: number; y: number };
  track_id: number;
  velocity: { vx: number; vy: number };
  state: string;
  last_seen: number;
}

export interface HandInfo {
  position: [number, number];
  velocity: [number, number];
  tracked: boolean;
}

export interface Interaction {
  hand: string;
  object: string;
  object_name?: string;
  state: string;
  contact: boolean;
  grasp_probability: number;
  distance_px: number;
  duration_ms: number;
}

export interface ActiveAlert {
  type: string;
  severity: "INFO" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  message: string;
}

export interface SystemState {
  schema_version: string;
  timestamp: string;
  unix_timestamp: number;
  session_id: string;
  frame_id: number;
  sequence: number;

  system: {
    status: string;
    mode: string;
    uptime: number;
    cpu_percent: number;
    ram_percent: number;
    gpu_percent: number;
    temperature: number;
  };

  camera: {
    connected: boolean;
    fps: number;
    resolution: string;
    brightness: number;
    blur_score: number;
    dropped_frames: number;
  };

  astronaut: {
    detected: boolean;
    track_id: number;
    confidence: number;
    position: { x: number; y: number };
    bbox: [number, number, number, number];
  };

  activity: {
    current: string;
    confidence: number;
    stable: boolean;
    duration_ms: number;
  };

  objects: ExperimentObject[];
  hands: Record<string, HandInfo>;
  interactions: Interaction[];

  experiment: {
    status: string;
    current_step: number;
    total_steps: number;
    step_name: string;
    progress: number;
    expected_action: string;
  };

  validation: {
    status: string;
    sequence_valid: boolean;
  };

  next_step: {
    id: number;
    name: string;
    description: string;
    guidance: string;
    confidence: number;
  };

  alerts: ActiveAlert[];
  active_alert: ActiveAlert | null;
  recovery_action: string | null;

  performance: {
    inference_ms: number;
    tracking_ms: number;
    sequence_ms: number;
    total_latency_ms: number;
    p50_ms: number;
    p95_ms: number;
    p99_ms: number;
    fps: number;
  };

  camera_status: string;
  model_status: string;
  mission_health_score: number;
}
