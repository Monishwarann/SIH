import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class AIService {
  final String baseUrl;

  AIService({this.baseUrl = 'http://localhost:8000'});

  Future<Map<String, dynamic>> getSystemStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/system/status')).timeout(const Duration(seconds: 3));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('[AIService] Failed to fetch system status: $e');
    }
    return {'status': 'OFFLINE', 'fps': 0.0, 'inference_latency_ms': 0.0};
  }

  Future<bool> startExperiment() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/api/experiment/start'));
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('[AIService] Failed to start experiment: $e');
      return false;
    }
  }

  Future<bool> stopExperiment() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/api/experiment/stop'));
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('[AIService] Failed to stop experiment: $e');
      return false;
    }
  }

  Future<bool> resetExperiment() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/api/experiment/reset'));
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('[AIService] Failed to reset experiment: $e');
      return false;
    }
  }

  Future<List<dynamic>> getSessionHistory() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/experiment/history'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data is List ? data : (data['history'] ?? []);
      }
    } catch (e) {
      debugPrint('[AIService] Failed to fetch session history: $e');
    }
    return [];
  }

  Future<Map<String, dynamic>> getModelsStatus() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/models/status'));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('[AIService] Failed to fetch models status: $e');
    }
    return {'activity': 'LIVE (models/best_bilstm_model.keras)', 'device': 'CUDA / CPU Edge'};
  }

  Future<List<dynamic>> getRecordingsList() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/recordings/list'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['recordings'] ?? [];
      }
    } catch (e) {
      debugPrint('[AIService] Failed to fetch recordings list: $e');
    }
    return [];
  }

  Future<Map<String, dynamic>> startLiveRecording() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/api/recording/live/start'));
      return jsonDecode(response.body);
    } catch (e) {
      debugPrint('[AIService] Failed to start live recording: $e');
      return {'status': 'ERROR'};
    }
  }

  Future<Map<String, dynamic>> stopLiveRecording() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/api/recording/live/stop'));
      return jsonDecode(response.body);
    } catch (e) {
      debugPrint('[AIService] Failed to stop live recording: $e');
      return {'status': 'ERROR'};
    }
  }

  Future<Map<String, dynamic>> exportLogs() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/logs/export'));
      return jsonDecode(response.body);
    } catch (e) {
      debugPrint('[AIService] Failed to export logs: $e');
      return {'status': 'ERROR'};
    }
  }
}
