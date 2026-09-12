class SessionRecord {
  final String sessionId;
  final String experimentName;
  final String timestamp;
  final double durationSeconds;
  final int totalSteps;
  final int completedSteps;
  final int skippedSteps;
  final int wrongActions;
  final int wrongObjects;
  final int timeouts;
  final double averageConfidence;
  final double averageFps;
  final double averageLatencyMs;
  final String finalStatus;

  SessionRecord({
    required this.sessionId,
    required this.experimentName,
    required this.timestamp,
    required this.durationSeconds,
    required this.totalSteps,
    required this.completedSteps,
    required this.skippedSteps,
    required this.wrongActions,
    required this.wrongObjects,
    required this.timeouts,
    required this.averageConfidence,
    required this.averageFps,
    required this.averageLatencyMs,
    required this.finalStatus,
  });

  factory SessionRecord.fromJson(Map<String, dynamic> json) {
    var metrics = json['metrics'] ?? {};
    return SessionRecord(
      sessionId: json['session_id'] ?? 'EXP_001',
      experimentName: json['experiment_name'] ?? json['experiment'] ?? 'Two-Box Sorting',
      timestamp: json['timestamp'] ?? DateTime.now().toIso8601String(),
      durationSeconds: (json['duration_seconds'] ?? json['duration'] ?? 120.0).toDouble(),
      totalSteps: (metrics['total_steps'] ?? json['total_steps'] ?? 5).toInt(),
      completedSteps: (metrics['completed_steps'] ?? json['completed_steps'] ?? 5).toInt(),
      skippedSteps: (metrics['skipped_steps'] ?? json['skipped_steps'] ?? 0).toInt(),
      wrongActions: (metrics['wrong_order_actions'] ?? json['wrong_actions'] ?? 0).toInt(),
      wrongObjects: (metrics['wrong_objects'] ?? json['wrong_objects'] ?? 0).toInt(),
      timeouts: (metrics['timeouts'] ?? json['timeouts'] ?? 0).toInt(),
      averageConfidence: (metrics['average_confidence'] ?? json['average_confidence'] ?? 0.94).toDouble(),
      averageFps: (metrics['average_fps'] ?? json['average_fps'] ?? 27.5).toDouble(),
      averageLatencyMs: (metrics['average_latency_ms'] ?? json['average_latency_ms'] ?? 55.0).toDouble(),
      finalStatus: json['final_status'] ?? json['status'] ?? 'PASSED',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'session_id': sessionId,
      'experiment_name': experimentName,
      'timestamp': timestamp,
      'duration_seconds': durationSeconds,
      'total_steps': totalSteps,
      'completed_steps': completedSteps,
      'skipped_steps': skippedSteps,
      'wrong_actions': wrongActions,
      'wrong_objects': wrongObjects,
      'timeouts': timeouts,
      'average_confidence': averageConfidence,
      'average_fps': averageFps,
      'average_latency_ms': averageLatencyMs,
      'final_status': finalStatus,
    };
  }
}
