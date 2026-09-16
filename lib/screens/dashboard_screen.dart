import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/theme.dart';
import '../widgets/widgets.dart';


class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final telemetry = provider.currentTelemetry;

    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text("MISSION CONTROL DASHBOARD",
                      style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                          letterSpacing: 1.1)),
                  Text(
                      "Real-Time Autonomous Space Payload HAR System Overview",
                      style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                ],
              ),
              ElevatedButton.icon(
                onPressed: () => provider.setActiveTab('live'),
                icon: const Icon(Icons.videocam, size: 16),
                label: const Text("OPEN LIVE MONITORING"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryCyan,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(
                      horizontal: 18, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Status Cards Grid with Glassmorphism
          GridView.count(
            crossAxisCount: 4,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            shrinkWrap: true,
            childAspectRatio: 2.2,
            children: [
              _buildGlassStatCard("ACTIVE EXPERIMENT", telemetry.experiment,
                  Icons.science, AppColors.primaryCyan),
              _buildGlassStatCard("CURRENT ACTIVITY", telemetry.activity,
                  Icons.directions_run, AppColors.successEmerald),
              _buildGlassStatCard(
                  "SEQUENCE STEP",
                  "${telemetry.currentStep} / ${telemetry.totalSteps}",
                  Icons.format_list_numbered,
                  AppColors.accentPurple),
              _buildGlassStatCard(
                  "CONFIDENCE",
                  "${(telemetry.confidence * 100).toStringAsFixed(1)}%",
                  Icons.verified,
                  AppColors.warningAmber),
            ],
          ),

          const SizedBox(height: 24),

          // Main View split: System Health & Recent Alerts
          Expanded(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  flex: 3,
                  child: GlassCard(
                    borderColor: AppColors.primaryCyan.withValues(alpha: 0.4),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("SYSTEM HEALTH & TELEMETRY METRICS",
                            style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: AppColors.textPrimary,
                                letterSpacing: 1.1)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        const SizedBox(height: 6),
                        _buildHealthRow("Camera Pipeline:",
                            "ONLINE (1280x720 @ 30 FPS)", AppColors.successEmerald),
                        _buildHealthRow("3D HAR Model:",
                            "ACTIVE (models/bas_har.keras)", AppColors.successEmerald),
                        _buildHealthRow("Object Detector:",
                            "ONLINE (models/object_detector.onnx)", AppColors.successEmerald),
                        _buildHealthRow("Pose Skeleton:", "TRACKING ACTIVE",
                            AppColors.successEmerald),
                        _buildHealthRow("Hand Tracker:",
                            "${telemetry.handsDetected} Hands Tracked", AppColors.primaryCyan),
                        _buildHealthRow("Inference Latency:",
                            "${telemetry.latencyMs.toStringAsFixed(1)} ms", AppColors.primaryCyan),
                        _buildHealthRow("Deployment Mode:",
                            "100% OFFLINE EDGE INFERENCE", AppColors.successEmerald),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  flex: 2,
                  child: GlassCard(
                    borderColor: AppColors.warningAmber.withValues(alpha: 0.4),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text("REALTIME ANOMALY ALERTS",
                                style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.textPrimary,
                                    letterSpacing: 1.1)),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: AppColors.warningAmber.withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                "${provider.alerts.length} ALERTS",
                                style: const TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.warningAmber),
                              ),
                            ),
                          ],
                        ),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        Expanded(
                          child: provider.alerts.isEmpty
                              ? const Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(Icons.shield_outlined,
                                          size: 36, color: AppColors.successEmerald),
                                      SizedBox(height: 8),
                                      Text("NO SEQUENCE VIOLATIONS DETECTED",
                                          style: TextStyle(
                                              color: AppColors.successEmerald,
                                              fontSize: 11,
                                              fontWeight: FontWeight.bold)),
                                      Text("FSM State Machine Nominal",
                                          style: TextStyle(
                                              color: AppColors.textMuted,
                                              fontSize: 10)),
                                    ],
                                  ),
                                )
                              : ListView.builder(
                                  itemCount: provider.alerts.length,
                                  itemBuilder: (context, index) {
                                    final alert = provider.alerts[index];
                                    return Container(
                                      margin: const EdgeInsets.only(bottom: 8),
                                      padding: const EdgeInsets.all(10),
                                      decoration: BoxDecoration(
                                        color: AppColors.background
                                            .withValues(alpha: 0.6),
                                        border: Border.all(
                                            color: AppColors.warningAmber
                                                .withValues(alpha: 0.5)),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Row(
                                        children: [
                                          const Icon(Icons.warning_amber,
                                              color: AppColors.warningAmber,
                                              size: 16),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              alert,
                                              style: const TextStyle(
                                                  fontSize: 11,
                                                  color: AppColors.textPrimary),
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
    );
  }

  Widget _buildGlassStatCard(
      String label, String value, IconData icon, Color neonColor) {
    return GlassCard.neon(
      neonColor: neonColor,
      padding: const EdgeInsets.all(12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: neonColor.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: neonColor, size: 22),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(label,
                    style: const TextStyle(
                        fontSize: 10,
                        color: AppColors.textMuted,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.8)),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: neonColor),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHealthRow(String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label,
              style:
                  const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
          Row(
            children: [
              Icon(Icons.circle, size: 6, color: color),
              const SizedBox(width: 6),
              Text(value,
                  style: TextStyle(
                      fontSize: 12, fontWeight: FontWeight.bold, color: color)),
            ],
          ),
        ],
      ),
    );
  }
}
