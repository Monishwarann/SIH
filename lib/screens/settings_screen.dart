import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  String _wsUrl = 'ws://localhost:8000/ws/experiment';
  String _httpUrl = 'http://localhost:8000';
  int _cameraIndex = 0;
  double _confidenceThreshold = 0.60;
  bool _voiceGuidanceEnabled = true;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("SYSTEM SETTINGS & CONFIGURATION", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const Text("Configure local Python AI engine endpoint, camera settings, and speech synthesis", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AppColors.cardBackground,
              border: Border.all(color: AppColors.cardBorder),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("AI ENGINE ENDPOINT CONFIGURATION", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const Divider(height: 20, color: AppColors.cardBorder),
                const Text("WebSocket URL:", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                const SizedBox(height: 4),
                TextField(
                  controller: TextEditingController(text: _wsUrl),
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: AppColors.background,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                  ),
                  onChanged: (v) => _wsUrl = v,
                ),
                const SizedBox(height: 16),
                const Text("REST API Base URL:", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                const SizedBox(height: 4),
                TextField(
                  controller: TextEditingController(text: _httpUrl),
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: AppColors.background,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                  ),
                  onChanged: (v) => _httpUrl = v,
                ),
                const SizedBox(height: 20),
                const Text("CAMERA & INFERENCE PREFERENCES", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const Divider(height: 20, color: AppColors.cardBorder),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Camera Source Index:", style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    DropdownButton<int>(
                      value: _cameraIndex,
                      dropdownColor: AppColors.cardBackground,
                      items: [0, 1, 2].map((i) => DropdownMenuItem(value: i, child: Text("Camera Index $i"))).toList(),
                      onChanged: (v) => setState(() => _cameraIndex = v!),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Offline TTS Voice Guidance:", style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    Switch(
                      value: _voiceGuidanceEnabled,
                      activeColor: AppColors.primaryCyan,
                      onChanged: (v) => setState(() => _voiceGuidanceEnabled = v),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
