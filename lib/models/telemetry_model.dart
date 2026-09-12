class DetectedObject {
  final String name;
  final double confidence;
  final int x;
  final int y;
  final int width;
  final int height;

  DetectedObject({
    required this.name,
    required this.confidence,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
  });

  factory DetectedObject.fromJson(Map<String, dynamic> json) {
    List<dynamic> bbox = json['bbox'] ?? [0, 0, 0, 0];
    int x1 = (json['x'] ?? (bbox.isNotEmpty ? bbox[0] : 0)).toInt();
    int y1 = (json['y'] ?? (bbox.length > 1 ? bbox[1] : 0)).toInt();
    int x2 = (json['width'] != null ? x1 + (json['width'] as num).toInt() : (bbox.length > 2 ? bbox[2] : x1 + 100)).toInt();
    int y2 = (json['height'] != null ? y1 + (json['height'] as num).toInt() : (bbox.length > 3 ? bbox[3] : y1 + 100)).toInt();

    return DetectedObject(
      name: json['name'] ?? json['id'] ?? 'object',
      confidence: (json['confidence'] ?? 0.90).toDouble(),
      x: x1,
      y: y1,
      width: (x2 - x1).abs(),
      height: (y2 - y1).abs(),
    );
  }
}

class TelemetryData {
  final String timestamp;
  final String activity;
  final double confidence;
  final double fps;
  final double latencyMs;
  final String experiment;
  final int currentStep;
  final int totalSteps;
  final String status;
  final String alertMessage;
  final bool poseDetected;
  final int handsDetected;
  final List<DetectedObject> objects;

  TelemetryData({
    required this.timestamp,
    required this.activity,
    required this.confidence,
    required this.fps,
    required this.latencyMs,
    required this.experiment,
    required this.currentStep,
    required this.totalSteps,
    required this.status,
    required this.alertMessage,
    required this.poseDetected,
    required this.handsDetected,
    required this.objects,
  });

  factory TelemetryData.fromJson(Map<String, dynamic> json) {
    var rawObjects = json['objects'] as List? ?? [];
    List<DetectedObject> objs = rawObjects.map((o) => DetectedObject.fromJson(o)).toList();

    return TelemetryData(
      timestamp: json['timestamp']?.toString() ?? DateTime.now().toIso8601String(),
      activity: json['activity'] ?? json['current_activity'] ?? 'APPROACH_OBJECT',
      confidence: (json['confidence'] ?? json['activity_confidence'] ?? 0.94).toDouble(),
      fps: (json['fps'] ?? 30.0).toDouble(),
      latencyMs: (json['latency_ms'] ?? json['inference_latency_ms'] ?? 45.0).toDouble(),
      experiment: json['experiment'] ?? json['experiment_name'] ?? 'Two-Box Sorting',
      currentStep: (json['current_step'] ?? 1).toInt(),
      totalSteps: (json['total_steps'] ?? 5).toInt(),
      status: json['status'] ?? json['safety_state'] ?? 'CORRECT',
      alertMessage: json['alert_message'] ?? json['next_step_guidance'] ?? 'Step Active',
      poseDetected: json['pose_detected'] ?? true,
      handsDetected: (json['hands_detected'] ?? 2).toInt(),
      objects: objs,
    );
  }

  factory TelemetryData.initial() {
    return TelemetryData(
      timestamp: DateTime.now().toIso8601String(),
      activity: 'APPROACH_OBJECT',
      confidence: 0.945,
      fps: 30.0,
      latencyMs: 42.5,
      experiment: 'Two-Box Sorting',
      currentStep: 1,
      totalSteps: 5,
      status: 'CORRECT',
      alertMessage: 'Position sample facing main container.',
      poseDetected: true,
      handsDetected: 2,
      objects: [
        DetectedObject(name: 'Main Container', confidence: 0.96, x: 50, y: 150, width: 300, height: 250),
        DetectedObject(name: 'Red Box', confidence: 0.94, x: 120, y: 200, width: 90, height: 90),
        DetectedObject(name: 'Yellow Box', confidence: 0.93, x: 230, y: 200, width: 90, height: 90),
      ],
    );
  }
}
