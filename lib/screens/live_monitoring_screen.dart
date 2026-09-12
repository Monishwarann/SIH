import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/app_theme.dart';

class LiveMonitoringScreen extends StatelessWidget {
  const LiveMonitoringScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final telemetry = provider.currentTelemetry;

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Left: Live Camera View
          Expanded(
            flex: 3,
            child: Container(
              decoration: BoxDecoration(
                color: Colors.black,
                border: Border.all(color: AppColors.cardBorder),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Stack(
                children: [
                  // Camera / MJPEG Stream view
                  Center(
                    child: Image.network(
                      'http://localhost:8000/video',
                      fit: BoxFit.contain,
                      errorBuilder: (context, error, stackTrace) {
                        return Container(
                          color: const Color(0xFF0B132B),
                          child: Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: const [
                                Icon(Icons.videocam_off, size: 48, color: AppColors.textMuted),
                                SizedBox(height: 12),
                                Text("LIVE VIDEO STREAM CONNECTING...", style: TextStyle(color: AppColors.primaryCyan, fontSize: 13, fontWeight: FontWeight.bold)),
                                SizedBox(height: 4),
                                Text("http://localhost:8000/video", style: TextStyle(color: AppColors.textMuted, fontSize: 11)),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),

                  // Top Left Telemetry Overlay Badge
                  Positioned(
                    top: 12,
                    left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.75),
                        border: Border.all(color: AppColors.primaryCyan),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.circle, size: 8, color: AppColors.successEmerald),
                          const SizedBox(width: 6),
                          Text("FPS: ${telemetry.fps.toStringAsFixed(1)} | LATENCY: ${telemetry.latencyMs.toStringAsFixed(1)} ms", style: const TextStyle(fontSize: 10, color: Colors.white, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ),
                  ),

                  // Bottom Camera HUD Overlay
                  Positioned(
                    bottom: 12,
                    left: 12,
                    right: 12,
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: AppColors.cardBackground.withOpacity(0.90),
                        border: Border.all(color: AppColors.cardBorder),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.directions_run, color: AppColors.successEmerald, size: 18),
                              const SizedBox(width: 8),
                              Text("ACTIVITY: ${telemetry.activity}", style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.successEmerald)),
                            ],
                          ),
                          Text("CONFIDENCE: ${(telemetry.confidence * 100).toStringAsFixed(1)}%", style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.primaryCyan)),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(width: 16),

          // Right Panel: Step Telemetry & Status
          Expanded(
            flex: 2,
            child: Column(
              children: [
                // Sequence Status Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    border: Border.all(color: AppColors.cardBorder),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text("EXPERIMENT SEQUENCE", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textMuted)),
                          _buildStatusBadge(telemetry.status),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Text("Step ${telemetry.currentStep} of ${telemetry.totalSteps}", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                      const SizedBox(height: 4),
                      Text(telemetry.alertMessage, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // Detected Objects Card
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      border: Border.all(color: AppColors.cardBorder),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("DETECTED PAYLOAD OBJECTS", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textMuted)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        Expanded(
                          child: telemetry.objects.isEmpty
                              ? const Center(child: Text("No payload items in view.", style: TextStyle(color: AppColors.textMuted, fontSize: 12)))
                              : ListView.builder(
                                  itemCount: telemetry.objects.length,
                                  itemBuilder: (context, index) {
                                    final obj = telemetry.objects[index];
                                    return Container(
                                      margin: const EdgeInsets.only(bottom: 8),
                                      padding: const EdgeInsets.all(10),
                                      decoration: BoxDecoration(
                                        color: AppColors.background,
                                        border: Border.all(color: AppColors.cardBorder),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Row(
                                            children: [
                                              const Icon(Icons.crop_square, size: 16, color: AppColors.primaryCyan),
                                              const SizedBox(width: 8),
                                              Text(obj.name.toUpperCase(), style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                                            ],
                                          ),
                                          Text("${(obj.confidence * 100).toStringAsFixed(0)}%", style: const TextStyle(fontSize: 11, color: AppColors.successEmerald)),
                                        ],
                                      ),
                                    );
                                  },
                                ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusBadge(String status) {
    Color bg = AppColors.successEmerald;
    if (status.contains("SKIPPED") || status.contains("WRONG") || status.contains("TIMEOUT")) {
      bg = AppColors.warningAmber;
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg.withOpacity(0.2),
        border: Border.all(color: bg),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        status.toUpperCase(),
        style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: bg),
      ),
    );
  }
}
