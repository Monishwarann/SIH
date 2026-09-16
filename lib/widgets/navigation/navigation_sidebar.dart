import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/realtime_provider.dart';
import '../../theme/app_theme.dart';
import '../../models/telemetry_model.dart';


class NavigationSidebar extends StatelessWidget {
  const NavigationSidebar({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final activeTab = provider.activeTab;

    final menuItems = [
      {'id': 'dashboard', 'label': 'Mission Control', 'icon': Icons.dashboard_outlined},
      {'id': 'live', 'label': 'Live Experiment', 'icon': Icons.videocam_outlined},
      {'id': 'experiments', 'label': 'Experiment Selector', 'icon': Icons.science_outlined},
      {'id': 'data_collection', 'label': 'Data Collection', 'icon': Icons.collections_bookmark_outlined},
      {'id': 'history', 'label': 'Session History', 'icon': Icons.history_outlined},
      {'id': 'reports', 'label': 'Reports & Exports', 'icon': Icons.assessment_outlined},
      {'id': 'settings', 'label': 'Settings', 'icon': Icons.settings_outlined},
    ];

    return Container(
      width: 240,
      margin: const EdgeInsets.all(8),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
          child: Container(
            decoration: BoxDecoration(
              color: AppColors.cardBackground.withValues(alpha: 0.75),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.cardBorder.withValues(alpha: 0.8)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.4),
                  blurRadius: 12,
                  offset: const Offset(2, 4),
                ),
              ],
            ),
            child: Column(
              children: [
                Expanded(
                  child: ListView(
                    padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 10),
                    children: [
                      const Padding(
                        padding: EdgeInsets.only(left: 10, bottom: 12),
                        child: Text(
                          "PAYLOAD OPERATIONS",
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: AppColors.textMuted,
                            letterSpacing: 1.2,
                          ),
                        ),
                      ),
                      ...menuItems.map((item) {
                        final String id = item['id'] as String;
                        final String label = item['label'] as String;
                        final IconData icon = item['icon'] as IconData;
                        final bool isActive = activeTab == id;

                        return Padding(
                          padding: const EdgeInsets.only(bottom: 6),
                          child: InkWell(
                            onTap: () => provider.setActiveTab(id),
                            borderRadius: BorderRadius.circular(8),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 11),
                              decoration: BoxDecoration(
                                color: isActive
                                    ? AppColors.primaryCyanGlow.withValues(alpha: 0.35)
                                    : Colors.transparent,
                                border: Border.all(
                                  color: isActive
                                      ? AppColors.primaryCyan
                                      : Colors.transparent,
                                  width: 1,
                                ),
                                borderRadius: BorderRadius.circular(8),
                                boxShadow: [
                                  if (isActive)
                                    BoxShadow(
                                      color: AppColors.primaryCyan.withValues(alpha: 0.2),
                                      blurRadius: 10,
                                    ),
                                ],
                              ),
                              child: Row(
                                children: [
                                  Icon(icon,
                                      size: 18,
                                      color: isActive
                                          ? AppColors.primaryCyan
                                          : AppColors.textSecondary),
                                  const SizedBox(width: 12),
                                  Text(
                                    label,
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight:
                                          isActive ? FontWeight.bold : FontWeight.normal,
                                      color: isActive
                                          ? AppColors.primaryCyan
                                          : AppColors.textSecondary,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      }),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: 0.25),
                    border: Border(top: BorderSide(color: AppColors.cardBorder.withValues(alpha: 0.6))),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text("Target FPS:",
                              style: TextStyle(fontSize: 10, color: AppColors.textMuted)),
                          Text(provider.currentTelemetry.formattedFps,
                              style: const TextStyle(
                                  fontSize: 10,
                                  color: AppColors.textPrimary,
                                  fontWeight: FontWeight.bold)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text("Latency:",
                              style: TextStyle(fontSize: 10, color: AppColors.textMuted)),
                          Text(provider.currentTelemetry.formattedLatency,
                              style: const TextStyle(
                                  fontSize: 10,
                                  color: AppColors.primaryCyan,
                                  fontWeight: FontWeight.bold)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text("Inference:",
                              style: TextStyle(fontSize: 10, color: AppColors.textMuted)),
                          const Text("100% Offline",
                              style: TextStyle(
                                  fontSize: 10,
                                  color: AppColors.successEmerald,
                                  fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
