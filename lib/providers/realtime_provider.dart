import 'package:flutter/foundation.dart';
import '../models/telemetry_model.dart';
import '../services/websocket_service.dart';
import '../services/ai_service.dart';
import '../services/voice_service.dart';

class RealtimeProvider with ChangeNotifier {
  final WebSocketService _wsService = WebSocketService();
  final AIService _aiService = AIService();
  final VoiceService _voiceService = VoiceService();

  TelemetryData _currentTelemetry = TelemetryData.initial();
  bool _isWsConnected = false;
  bool _isExperimentRunning = false;
  bool _isVoiceMuted = false;
  String _activeTab = 'dashboard';
  final List<String> _alerts = [];

  // Rolling Telemetry Waveform Buffers (30 samples)
  final List<double> _fpsHistory = List.filled(30, 30.0);
  final List<double> _latencyHistory = List.filled(30, 42.0);
  final List<double> _confidenceHistory = List.filled(30, 0.94);

  TelemetryData get currentTelemetry => _currentTelemetry;
  bool get isWsConnected => _isWsConnected;
  bool get isExperimentRunning => _isExperimentRunning;
  bool get isVoiceMuted => _isVoiceMuted;
  String get activeTab => _activeTab;
  List<String> get alerts => List.unmodifiable(_alerts);

  List<double> get fpsHistory => List.unmodifiable(_fpsHistory);
  List<double> get latencyHistory => List.unmodifiable(_latencyHistory);
  List<double> get confidenceHistory => List.unmodifiable(_confidenceHistory);

  RealtimeProvider() {
    _initConnection();
  }

  void _initConnection() {
    _wsService.connectionStream.listen((connected) {
      _isWsConnected = connected;
      notifyListeners();
    });

    _wsService.telemetryStream.listen((data) {
      _currentTelemetry = data;

      // Append rolling history buffers
      _fpsHistory.removeAt(0);
      _fpsHistory.add(data.fps);

      _latencyHistory.removeAt(0);
      _latencyHistory.add(data.latencyMs);

      _confidenceHistory.removeAt(0);
      _confidenceHistory.add(data.confidence);

      // Voice alert trigger if status changed
      if (!_isVoiceMuted && data.status != 'CORRECT' && data.alertMessage.isNotEmpty) {
        _voiceService.speak(data.alertMessage);
        final timestampStr = data.timestamp.length >= 19
            ? data.timestamp.substring(11, 19)
            : DateTime.now().toIso8601String().substring(11, 19);

        final alertEntry = '$timestampStr - [${data.status}] ${data.alertMessage}';
        if (!_alerts.contains(alertEntry)) {
          _alerts.insert(0, alertEntry);
          if (_alerts.length > 30) _alerts.removeLast();
        }
      }
      notifyListeners();
    });

    _wsService.connect();
  }

  void toggleVoiceMute() {
    _isVoiceMuted = !_isVoiceMuted;
    notifyListeners();
  }

  void setActiveTab(String tab) {
    _activeTab = tab;
    notifyListeners();
  }

  Future<void> startExperiment() async {
    final success = await _aiService.startExperiment();
    if (success) {
      _isExperimentRunning = true;
      if (!_isVoiceMuted) {
        _voiceService.speak("Experiment started. Position yourself facing the container.");
      }
      notifyListeners();
    }
  }

  Future<void> stopExperiment() async {
    final success = await _aiService.stopExperiment();
    if (success) {
      _isExperimentRunning = false;
      if (!_isVoiceMuted) {
        _voiceService.speak("Experiment session stopped.");
      }
      notifyListeners();
    }
  }

  Future<void> resetExperiment() async {
    final success = await _aiService.resetExperiment();
    if (success) {
      if (!_isVoiceMuted) {
        _voiceService.speak("Experiment sequence reset to step 1.");
      }
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _wsService.dispose();
    super.dispose();
  }
}
