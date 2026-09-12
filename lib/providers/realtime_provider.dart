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
  String _activeTab = 'dashboard';
  List<String> _alerts = [];

  TelemetryData get currentTelemetry => _currentTelemetry;
  bool get isWsConnected => _isWsConnected;
  bool get isExperimentRunning => _isExperimentRunning;
  String get activeTab => _activeTab;
  List<String> get alerts => List.unmodifiable(_alerts);

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
      
      // Voice alert trigger if status changed
      if (data.status != 'CORRECT' && data.alertMessage.isNotEmpty) {
        _voiceService.speak(data.alertMessage);
        if (!_alerts.contains(data.alertMessage)) {
          _alerts.insert(0, '${data.timestamp.substring(11, 19)} - ${data.alertMessage}');
          if (_alerts.length > 20) _alerts.removeLast();
        }
      }
      notifyListeners();
    });

    _wsService.connect();
  }

  void setActiveTab(String tab) {
    _activeTab = tab;
    notifyListeners();
  }

  Future<void> startExperiment() async {
    final success = await _aiService.startExperiment();
    if (success) {
      _isExperimentRunning = true;
      _voiceService.speak("Experiment started. Position yourself facing the container.");
      notifyListeners();
    }
  }

  Future<void> stopExperiment() async {
    final success = await _aiService.stopExperiment();
    if (success) {
      _isExperimentRunning = false;
      _voiceService.speak("Experiment session stopped.");
      notifyListeners();
    }
  }

  Future<void> resetExperiment() async {
    final success = await _aiService.resetExperiment();
    if (success) {
      _voiceService.speak("Experiment sequence reset to step 1.");
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _wsService.dispose();
    super.dispose();
  }
}
