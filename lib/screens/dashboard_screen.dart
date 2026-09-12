import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/app_theme.dart';

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
                  Text("MISSION CONTROL DASHBOARD", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                  Text("Real-Time Autonomous Space Payload HAR System Overview", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                ],
              ),
              ElevatedButton.icon(
                onPressed: () => provider.setActiveTab('live'),
                icon: const Icon(Icons.videocam, size: 16),
                label: const Text("OPEN LIVE MONITORING"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryCyan,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Status Cards Grid
          GridView.count(
            crossAxisCount: 4,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            shrinkWrap: true,
            childAspectRatio: 2.2,
            children: [
              _buildStatCard("ACTIVE EXPERIMENT", telemetry.experiment, Icons.science, AppColors.primaryCyan),
              _buildStatCard("CURRENT ACTIVITY", telemetry.activity, Icons.directions_run, AppColors.successEmerald),
              _buildStatCard("SEQUENCE STEP", "${telemetry.currentStep} / ${telemetry.totalSteps}", Icons.format_list_numbered, AppColors.accentPurple),
              _buildStatCard("CONFIDENCE", "${(telemetry.confidence * 100).toStringAsFixed(1)}%", Icons.verified, AppColors.warningAmber),
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
                        const Text("SYSTEM HEALTH & TELEMETRY METRICS", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        const SizedBox(height: 10),
                        _buildHealthRow("Camera Pipeline:", "ONLINE (1280x720 @ 30 FPS)", AppColors.successEmerald),
                        _buildHealthRow("3D HAR Model:", "ACTIVE (models/bas_har.keras)", AppColors.successEmerald),
                        _buildHealthRow("Object Detector:", "ONLINE (models/object_detector.onnx)", AppColors.successEmerald),
                        _buildHealthRow("Pose Skeleton:", "TRACKING ACTIVE", AppColors.successEmerald),
                        _buildHealthRow("Hand Tracker:", "${telemetry.handsDetected} Hands Tracked", AppColors.primaryCyan),
                        _buildHealthRow("Inference Latency:", "${telemetry.latencyMs.toStringAsFixed(1)} ms", AppColors.primaryCyan),
                        _buildHealthRow("Deployment Mode:", "100% OFFLINE EDGE INFERENCE", AppColors.successEmerald),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  flex: 2,
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
                        const Text("RECENT ALERTS & SEQUENCE EVENTS", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        Expanded(
                          child: provider.alerts.isEmpty
                              ? const Center(child: Text("No sequence errors or warnings logged.", style: TextStyle(color: AppColors.textMuted, fontSize: 12)))
                              : ListView.builder(
                                  itemCount: provider.alerts.length,
                                  itemBuilder: (context, index) {
                                    return Padding(
                                      padding: const EdgeInsets.only(bottom: 8),
                                      child: Row(
                                        children: [
                                          const Icon(Icons.warning_amber, size: 16, color: AppColors.warningAmber),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              provider.alerts[index],
                                              style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
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

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        border: Border.all(color: AppColors.cardBorder),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppColors.textMuted, letterSpacing: 1.0)),
              Icon(icon, size: 16, color: color),
            ],
          ),
          Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color), overflow: TextOverflow.ellipsis),
        ],
      ),
    );
  }

  Widget _buildHealthRow(String label, String status, Color statusColor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
          Text(status, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: statusColor)),
        ],
      ),
    );
  }
}
