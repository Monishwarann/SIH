import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/realtime_provider.dart';
import '../theme/app_theme.dart';

class HeaderBar extends StatelessWidget implements PreferredSizeWidget {
  const HeaderBar({super.key});

  @override
  Size get preferredSize => const Size.fromHeight(60);

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<RealtimeProvider>(context);
    final isConnected = provider.isWsConnected;

    return ClipRRect(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
        child: Container(
          height: 60,
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: BoxDecoration(
            color: AppColors.cardBackground.withValues(alpha: 0.8),
            border: Border(
              bottom: BorderSide(
                color: AppColors.cardBorder.withValues(alpha: 0.8),
              ),
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.primaryCyanGlow.withValues(alpha: 0.4),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: AppColors.primaryCyan.withValues(alpha: 0.6),
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primaryCyan.withValues(alpha: 0.25),
                          blurRadius: 10,
                        ),
                      ],
                    ),
                    child: const Icon(Icons.rocket_launch,
                        color: AppColors.primaryCyan, size: 20),
                  ),
                  const SizedBox(width: 12),
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text("ASTRA-HAR",
                          style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textPrimary,
                              letterSpacing: 1.1)),
                      Text("ISRO BAS EXPERIMENT HAR MONITOR (PS 26174)",
                          style: TextStyle(
                              fontSize: 9,
                              color: AppColors.textMuted,
                              letterSpacing: 0.8)),
                    ],
                  ),
                ],
              ),
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: isConnected
                          ? AppColors.successEmerald.withValues(alpha: 0.15)
                          : AppColors.errorRed.withValues(alpha: 0.15),
                      border: Border.all(
                        color: isConnected
                            ? AppColors.successEmerald
                            : AppColors.errorRed,
                      ),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: (isConnected
                                  ? AppColors.successEmerald
                                  : AppColors.errorRed)
                              .withValues(alpha: 0.2),
                          blurRadius: 8,
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.circle,
                            size: 8,
                            color: isConnected
                                ? AppColors.successEmerald
                                : AppColors.errorRed),
                        const SizedBox(width: 8),
                        Text(
                          isConnected ? "AI ENGINE ONLINE" : "AI ENGINE OFFLINE",
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: isConnected
                                ? AppColors.successEmerald
                                : AppColors.errorRed,
                            letterSpacing: 0.8,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 14),
                  ElevatedButton.icon(
                    onPressed: () {
                      if (provider.isExperimentRunning) {
                        provider.stopExperiment();
                      } else {
                        provider.startExperiment();
                      }
                    },
                    icon: Icon(
                        provider.isExperimentRunning ? Icons.stop : Icons.play_arrow,
                        size: 16),
                    label: Text(provider.isExperimentRunning
                        ? "STOP SESSION"
                        : "START EXPERIMENT"),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: provider.isExperimentRunning
                          ? AppColors.errorRed
                          : AppColors.primaryCyan,
                      foregroundColor: Colors.black,
                      elevation: 4,
                      shadowColor: (provider.isExperimentRunning
                              ? AppColors.errorRed
                              : AppColors.primaryCyan)
                          .withValues(alpha: 0.4),
                      textStyle: const TextStyle(
                          fontSize: 11, fontWeight: FontWeight.bold),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 10),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
