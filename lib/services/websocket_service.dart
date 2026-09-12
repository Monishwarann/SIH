import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/telemetry_model.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  final StreamController<TelemetryData> _telemetryController = StreamController<TelemetryData>.broadcast();
  final StreamController<bool> _connectionController = StreamController<bool>.broadcast();
  
  bool _isConnected = false;
  String _wsUrl = 'ws://localhost:8000/ws/experiment';
  Timer? _reconnectTimer;

  Stream<TelemetryData> get telemetryStream => _telemetryController.stream;
  Stream<bool> get connectionStream => _connectionController.stream;
  bool get isConnected => _isConnected;

  void connect({String? url}) {
    if (url != null) _wsUrl = url;
    _reconnectTimer?.cancel();

    try {
      _channel = WebSocketChannel.connect(Uri.parse(_wsUrl));
      _isConnected = true;
      _connectionController.add(true);
      debugPrint('[WebSocketService] Connected to $_wsUrl');

      _channel!.stream.listen(
        (message) {
          try {
            final Map<String, dynamic> data = jsonDecode(message);
            final telemetry = TelemetryData.fromJson(data);
            _telemetryController.add(telemetry);
          } catch (e) {
            debugPrint('[WebSocketService] Error parsing message: $e');
          }
        },
        onError: (error) {
          debugPrint('[WebSocketService] Connection error: $error');
          _handleDisconnect();
        },
        onDone: () {
          debugPrint('[WebSocketService] Connection closed');
          _handleDisconnect();
        },
      );
    } catch (e) {
      debugPrint('[WebSocketService] Failed to connect: $e');
      _handleDisconnect();
    }
  }

  void _handleDisconnect() {
    _isConnected = false;
    _connectionController.add(false);
    _channel?.sink.close();
    
    // Auto reconnect every 3 seconds
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(const Duration(seconds: 3), () {
      debugPrint('[WebSocketService] Attempting reconnection...');
      connect();
    });
  }

  void disconnect() {
    _reconnectTimer?.cancel();
    _channel?.sink.close();
    _isConnected = false;
    _connectionController.add(false);
  }

  void dispose() {
    disconnect();
    _telemetryController.close();
    _connectionController.close();
  }
}
