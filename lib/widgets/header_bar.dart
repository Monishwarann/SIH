import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/app_theme.dart';

class HeaderBar extends StatelessWidget implements PreferredSizeWidget {
  const HeaderBar({super.key});

  @override
  Size get preferredSize => const Size.fromHeight(56);

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final isConnected = provider.isWsConnected;

    return Container(
      height: 56,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: const BoxDecoration(
        color: AppColors.cardBackground,
        border: Border(bottom: BorderSide(color: AppColors.cardBorder)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: AppColors.primaryCyanGlow,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Icon(Icons.rocket_launch, color: AppColors.primaryCyan, size: 20),
              ),
              const SizedBox(width: 12),
              Column(
                mainAxisAlignment: ColorScheme.dark().surface == AppColors.cardBackground ? MainAxisAlignment.center : MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text("ASTRA-HAR", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                  Text("ISRO BAS EXPERIMENT HAR MONITOR (PS 26174)", style: TextStyle(fontSize: 9, color: AppColors.textMuted, letterSpacing: 0.8)),
                ],
              ),
            ],
          ),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: isConnected ? const Color(0x2210B981) : const Color(0x22EF4444),
                  border: Border.all(color: isConnected ? AppColors.successEmerald : AppColors.errorRed),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  children: [
                    Icon(Icons.circle, size: 8, color: isConnected ? AppColors.successEmerald : AppColors.errorRed),
                    const SizedBox(width: 6),
                    Text(
                      isConnected ? "AI ENGINE ONLINE" : "AI ENGINE OFFLINE",
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        color: isConnected ? AppColors.successEmerald : AppColors.errorRed,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              ElevatedButton.icon(
                onPressed: () {
                  if (provider.isExperimentRunning) {
                    provider.stopExperiment();
                  } else {
                    provider.startExperiment();
                  }
                },
                icon: Icon(provider.isExperimentRunning ? Icons.stop : Icons.play_arrow, size: 16),
                label: Text(provider.isExperimentRunning ? "STOP SESSION" : "START EXPERIMENT"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: provider.isExperimentRunning ? AppColors.errorRed : AppColors.primaryCyan,
                  foregroundColor: Colors.black,
                  textStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
