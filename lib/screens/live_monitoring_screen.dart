import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/theme.dart';
import '../models/telemetry_model.dart';
import '../widgets/widgets.dart';


class LiveMonitoringScreen extends StatefulWidget {
  const LiveMonitoringScreen({super.key});

  @override
  State<LiveMonitoringScreen> createState() => _LiveMonitoringScreenState();
}

class _LiveMonitoringScreenState extends State<LiveMonitoringScreen> {
  bool _showSpatialRadar = false;

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final telemetry = provider.currentTelemetry;
    final safety = telemetry.safetyStatus;

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // Top Quick Toolbar & Controls
          _buildQuickToolbar(provider),

          const SizedBox(height: 12),

          // Main Center Workspace (Left: Live Feed / Radar, Right: Telemetry & Radar)
          Expanded(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Left Panel: Live Camera or Spatial Radar
                Expanded(
                  flex: 3,
                  child: GlassCard(
                    padding: EdgeInsets.zero,
                    borderColor: safety.color.withOpacity(0.5),
                    child: Stack(
                      children: [
                        // View Switcher: Live MJPEG Video Stream or Interactive Spatial Radar
                        Positioned.fill(
                          child: _showSpatialRadar
                              ? SpatialRadarWidget(telemetry: telemetry)
                              : Image.network(
                                  'http://localhost:8000/video',
                                  fit: BoxFit.contain,
                                  errorBuilder: (context, error, stackTrace) {
                                    return Container(
                                      color: const Color(0xFF070D18),
                                      child: Center(
                                        child: Column(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: const [
                                            Icon(Icons.videocam_off,
                                                size: 52,
                                                color: AppColors.textMuted),
                                            SizedBox(height: 12),
                                            Text(
                                              "CONNECTING TO EDGE AI CAMERA STREAM...",
                                              style: TextStyle(
                                                color: AppColors.primaryCyan,
                                                fontSize: 12,
                                                fontWeight: FontWeight.bold,
                                                letterSpacing: 1.1,
                                              ),
                                            ),
                                            SizedBox(height: 6),
                                            Text(
                                              "http://localhost:8000/video",
                                              style: TextStyle(
                                                  color: AppColors.textMuted,
                                                  fontSize: 11),
                                            ),
                                          ],
                                        ),
                                      ),
                                    );
                                  },
                                ),
                        ),

                        // View Mode Toggle Overlay (Top Right)
                        Positioned(
                          top: 12,
                          right: 12,
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.8),
                              borderRadius: BorderRadius.circular(6),
                              border: Border.all(color: AppColors.cardBorder),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                _buildViewOption(
                                  icon: Icons.videocam,
                                  label: "CAMERA",
                                  isSelected: !_showSpatialRadar,
                                  onTap: () =>
                                      setState(() => _showSpatialRadar = false),
                                ),
                                _buildViewOption(
                                  icon: Icons.radar,
                                  label: "RADAR",
                                  isSelected: _showSpatialRadar,
                                  onTap: () =>
                                      setState(() => _showSpatialRadar = true),
                                ),
                              ],
                            ),
                          ),
                        ),

                        // Telemetry Badge (Top Left)
                        Positioned(
                          top: 12,
                          left: 12,
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.85),
                              border: Border.all(color: AppColors.primaryCyan),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Row(
                              children: [
                                Icon(Icons.circle,
                                    size: 8,
                                    color: telemetry.isHealthy
                                        ? AppColors.successEmerald
                                        : AppColors.warningAmber),
                                const SizedBox(width: 8),
                                Text(
                                  "${telemetry.formattedFps} | LATENCY: ${telemetry.formattedLatency}",
                                  style: const TextStyle(
                                    fontSize: 10,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),

                        // Bottom HUD Overlay Banner
                        Positioned(
                          bottom: 12,
                          left: 12,
                          right: 12,
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: AppColors.cardBackground.withOpacity(0.92),
                              border: Border.all(color: safety.color),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  children: [
                                    Icon(safety.icon,
                                        color: safety.color, size: 20),
                                    const SizedBox(width: 10),
                                    Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Text(
                                          "CURRENT ACTION: ${telemetry.activity}",
                                          style: TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.bold,
                                            color: safety.color,
                                          ),
                                        ),
                                        Text(
                                          telemetry.alertMessage,
                                          style: const TextStyle(
                                            fontSize: 11,
                                            color: AppColors.textSecondary,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 10, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: AppColors.primaryCyan.withOpacity(0.15),
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: Text(
                                    "CONFIDENCE: ${telemetry.confidencePercent}",
                                    style: const TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                      color: AppColors.primaryCyan,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(width: 16),

                // Right Panel: Sequence Status & Realtime Waveforms
                Expanded(
                  flex: 2,
                  child: Column(
                    children: [
                      // Sequence Protocol FSM Status Card
                      GlassCard(
                        borderColor: safety.color,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                const Text(
                                  "SEQUENCE FSM ENGINE",
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.textMuted,
                                    letterSpacing: 1.1,
                                  ),
                                ),
                                _buildStatusBadge(safety),
                              ],
                            ),
                            const SizedBox(height: 12),
                            Text(
                              "Step ${telemetry.currentStep} of ${telemetry.totalSteps}",
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: AppColors.textPrimary,
                              ),
                            ),
                            const SizedBox(height: 6),
                            LinearProgressIndicator(
                              value: telemetry.stepProgress,
                              backgroundColor: AppColors.background,
                              color: safety.color,
                              minHeight: 6,
                              borderRadius: BorderRadius.circular(3),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 12),

                      // Rolling Performance Waveform Graphs
                      SizedBox(
                        height: 110,
                        child: Row(
                          children: [
                            Expanded(
                              child: LiveWaveformGraph(
                                dataPoints: provider.fpsHistory,
                                title: "FPS Throughput",
                                unit: "FPS",
                                lineColor: AppColors.successEmerald,
                                minValue: 0.0,
                                maxValue: 40.0,
                              ),
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: LiveWaveformGraph(
                                dataPoints: provider.latencyHistory,
                                title: "Inference Latency",
                                unit: "ms",
                                lineColor: AppColors.warningAmber,
                                minValue: 0.0,
                                maxValue: 100.0,
                              ),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 12),

                      // Detected Payload Items List
                      Expanded(
                        child: GlassCard(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  const Text(
                                    "PAYLOAD OBJECTS & HANDS",
                                    style: TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                      color: AppColors.textMuted,
                                      letterSpacing: 1.1,
                                    ),
                                  ),
                                  Text(
                                    "HANDS: ${telemetry.handsDetected}",
                                    style: const TextStyle(
                                      fontSize: 10,
                                      fontWeight: FontWeight.bold,
                                      color: AppColors.primaryCyan,
                                    ),
                                  ),
                                ],
                              ),
                              const Divider(
                                  height: 16, color: AppColors.cardBorder),
                              Expanded(
                                child: telemetry.objects.isEmpty
                                    ? const Center(
                                        child: Text(
                                          "No payload items in FOV.",
                                          style: TextStyle(
                                              color: AppColors.textMuted,
                                              fontSize: 12),
                                        ),
                                      )
                                    : ListView.builder(
                                        itemCount: telemetry.objects.length,
                                        itemBuilder: (context, index) {
                                          final obj = telemetry.objects[index];
                                          return Container(
                                            margin: const EdgeInsets.only(
                                                bottom: 8),
                                            padding: const EdgeInsets.all(10),
                                            decoration: BoxDecoration(
                                              color: AppColors.background
                                                  .withOpacity(0.6),
                                              border: Border.all(
                                                  color: AppColors.cardBorder),
                                              borderRadius:
                                                  BorderRadius.circular(6),
                                            ),
                                            child: Row(
                                              mainAxisAlignment:
                                                  MainAxisAlignment
                                                      .spaceBetween,
                                              children: [
                                                Row(
                                                  children: [
                                                    const Icon(
                                                        Icons.crop_square,
                                                        size: 16,
                                                        color: AppColors
                                                            .primaryCyan),
                                                    const SizedBox(width: 8),
                                                    Text(
                                                      obj.name.toUpperCase(),
                                                      style: const TextStyle(
                                                        fontSize: 11,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                        color: AppColors
                                                            .textPrimary,
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                                Text(
                                                  "${(obj.confidence * 100).toStringAsFixed(0)}%",
                                                  style: const TextStyle(
                                                    fontSize: 11,
                                                    fontWeight: FontWeight.bold,
                                                    color: AppColors
                                                        .successEmerald,
                                                  ),
                                                ),
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
          ),
        ],
      ),
    );
  }

  Widget _buildQuickToolbar(RealtimeProvider provider) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.cardBackground.withOpacity(0.85),
        border: Border.all(color: AppColors.cardBorder),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              const Icon(Icons.science_outlined,
                  color: AppColors.primaryCyan, size: 20),
              const SizedBox(width: 10),
              Text(
                provider.currentTelemetry.experiment.toUpperCase(),
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          Row(
            children: [
              IconButton(
                tooltip: provider.isVoiceMuted
                    ? "Unmute Voice Warnings"
                    : "Mute Voice Warnings",
                icon: Icon(
                  provider.isVoiceMuted ? Icons.volume_off : Icons.volume_up,
                  color: provider.isVoiceMuted
                      ? AppColors.warningAmber
                      : AppColors.primaryCyan,
                  size: 20,
                ),
                onPressed: provider.toggleVoiceMute,
              ),
              const SizedBox(width: 8),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: provider.isExperimentRunning
                      ? AppColors.warningAmber
                      : AppColors.successEmerald,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(6)),
                ),
                onPressed: provider.isExperimentRunning
                    ? provider.stopExperiment
                    : provider.startExperiment,
                icon: Icon(provider.isExperimentRunning
                    ? Icons.pause
                    : Icons.play_arrow),
                label: Text(
                  provider.isExperimentRunning ? "STOP" : "START PROTOCOL",
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(width: 8),
              OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppColors.textSecondary,
                  side: const BorderSide(color: AppColors.cardBorder),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(6)),
                ),
                onPressed: provider.resetExperiment,
                icon: const Icon(Icons.refresh, size: 18),
                label: const Text("RESET FSM"),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildViewOption({
    required IconData icon,
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.primaryCyan : Colors.transparent,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Row(
          children: [
            Icon(icon,
                size: 14,
                color: isSelected ? Colors.black : AppColors.textMuted),
            const SizedBox(width: 4),
            Text(
              label,
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: isSelected ? Colors.black : AppColors.textMuted,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusBadge(SafetyStatus safety) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: safety.color.withOpacity(0.2),
        border: Border.all(color: safety.color),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(safety.icon, size: 12, color: safety.color),
          const SizedBox(width: 4),
          Text(
            safety.label,
            style: TextStyle(
                fontSize: 10, fontWeight: FontWeight.bold, color: safety.color),
          ),
        ],
      ),
    );
  }
}
