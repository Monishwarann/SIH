import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/app_theme.dart';

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
      color: AppColors.cardBackground,
      child: Column(
        children: [
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
              children: [
                const Padding(
                  padding: EdgeInsets.only(left: 12, bottom: 12),
                  child: Text(
                    "PAYLOAD OPERATIONS",
                    style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppColors.textMuted, letterSpacing: 1.2),
                  ),
                ),
                ...menuItems.map((item) {
                  final String id = item['id'] as String;
                  final String label = item['label'] as String;
                  final IconData icon = item['icon'] as IconData;
                  final bool isActive = activeTab == id;

                  return Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: InkWell(
                      onTap: () => provider.setActiveTab(id),
                      borderRadius: BorderRadius.circular(6),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                        decoration: BoxDecoration(
                          color: isActive ? AppColors.primaryCyanGlow : Colors.transparent,
                          border: Border.all(
                            color: isActive ? AppColors.primaryCyan : Colors.transparent,
                            width: 1,
                          ),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Row(
                          children: [
                            Icon(icon, size: 18, color: isActive ? AppColors.primaryCyan : AppColors.textSecondary),
                            const SizedBox(width: 12),
                            Text(
                              label,
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                                color: isActive ? AppColors.primaryCyan : AppColors.textSecondary,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }).toList(),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: const BoxDecoration(
              border: Border(top: BorderSide(color: AppColors.cardBorder)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Target FPS:", style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                    Text("${provider.currentTelemetry.fps.toStringAsFixed(1)}", style: const TextStyle(fontSize: 11, color: AppColors.textPrimary)),
                  ],
                ),
                const SizedBox(height: 4),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Latency:", style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                    Text("${provider.currentTelemetry.latencyMs.toStringAsFixed(1)} ms", style: const TextStyle(fontSize: 11, color: AppColors.primaryCyan)),
                  ],
                ),
                const SizedBox(height: 4),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Inference:", style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                    const Text("100% Offline", style: TextStyle(fontSize: 11, color: AppColors.successEmerald)),
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
