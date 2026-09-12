import 'package:flutter/foundation.dart';
import 'package:flutter_tts/flutter_tts.dart';

class VoiceService {
  final FlutterTts _tts = FlutterTts();
  bool _enabled = true;

  VoiceService() {
    _initTts();
  }

  void _initTts() async {
    try {
      await _tts.setLanguage("en-US");
      await _tts.setSpeechRate(0.5);
      await _tts.setVolume(1.0);
      await _tts.setPitch(1.0);
    } catch (e) {
      debugPrint('[VoiceService] Failed to initialize TTS: $e');
    }
  }

  void setEnabled(bool enabled) {
    _enabled = enabled;
  }

  Future<void> speak(String text) async {
    if (!_enabled || text.isEmpty) return;
    try {
      await _tts.speak(text);
    } catch (e) {
      debugPrint('[VoiceService] TTS Error: $e');
    }
  }

  Future<void> stop() async {
    try {
      await _tts.stop();
    } catch (e) {
      debugPrint('[VoiceService] TTS Stop Error: $e');
    }
  }
}
