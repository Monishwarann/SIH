class ExperimentStep {
  final int id;
  final String name;
  final String action;
  final String targetObject;
  final int timeoutSeconds;
  final String guidance;
  final String voiceAlert;

  ExperimentStep({
    required this.id,
    required this.name,
    required this.action,
    this.targetObject = '',
    this.timeoutSeconds = 30,
    this.guidance = '',
    this.voiceAlert = '',
  });

  factory ExperimentStep.fromJson(Map<String, dynamic> json) {
    return ExperimentStep(
      id: (json['id'] ?? 1).toInt(),
      name: json['name'] ?? json['action'] ?? 'Step ${json['id']}',
      action: json['action'] ?? 'APPROACH_OBJECT',
      targetObject: json['target_object'] ?? '',
      timeoutSeconds: (json['timeout'] ?? json['timeout_seconds'] ?? 30).toInt(),
      guidance: json['guidance'] ?? '',
      voiceAlert: json['voice_alert'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'action': action,
      'target_object': targetObject,
      'timeout_seconds': timeoutSeconds,
      'guidance': guidance,
      'voice_alert': voiceAlert,
    };
  }
}

class ExperimentProtocol {
  final String experimentId;
  final String name;
  final String description;
  final List<ExperimentStep> steps;
  final int timeoutSeconds;

  ExperimentProtocol({
    required this.experimentId,
    required this.name,
    required this.description,
    required this.steps,
    this.timeoutSeconds = 30,
  });

  factory ExperimentProtocol.fromJson(Map<String, dynamic> json) {
    var rawSteps = json['steps'] as List? ?? [];
    List<ExperimentStep> stepList = rawSteps.map((s) => ExperimentStep.fromJson(s)).toList();

    return ExperimentProtocol(
      experimentId: json['experiment_id'] ?? json['id'] ?? 'EXP_001',
      name: json['name'] ?? 'Two-Box Sorting Protocol',
      description: json['description'] ?? '',
      steps: stepList,
      timeoutSeconds: (json['timeout_seconds'] ?? 30).toInt(),
    );
  }
}
