import 'package:flutter/material.dart';
import '../models/session_model.dart';
import '../services/database_service.dart';
import '../theme/app_theme.dart';

class SessionHistoryScreen extends StatefulWidget {
  const SessionHistoryScreen({super.key});

  @override
  State<SessionHistoryScreen> createState() => _SessionHistoryScreenState();
}

class _SessionHistoryScreenState extends State<SessionHistoryScreen> {
  final DatabaseService _dbService = DatabaseService();
  List<SessionRecord> _sessions = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  void _loadHistory() async {
    final list = await _dbService.getAllSessions();
    if (list.isEmpty) {
      // Mock initial demo session records if DB empty
      list.addAll([
        SessionRecord(
          sessionId: "EXP_1726159200",
          experimentName: "Two-Box Sorting",
          timestamp: "2026-09-12 22:15:00",
          durationSeconds: 45.2,
          totalSteps: 5,
          completedSteps: 5,
          skippedSteps: 0,
          wrongActions: 0,
          wrongObjects: 0,
          timeouts: 0,
          averageConfidence: 0.948,
          averageFps: 28.2,
          averageLatencyMs: 52.0,
          finalStatus: "PASSED",
        ),
        SessionRecord(
          sessionId: "EXP_1726155600",
          experimentName: "Two-Box Sorting",
          timestamp: "2026-09-12 21:00:00",
          durationSeconds: 62.0,
          totalSteps: 5,
          completedSteps: 4,
          skippedSteps: 1,
          wrongActions: 0,
          wrongObjects: 0,
          timeouts: 0,
          averageConfidence: 0.912,
          averageFps: 27.5,
          averageLatencyMs: 58.4,
          finalStatus: "COMPLETED_WITH_WARNINGS",
        ),
      ]);
    }
    setState(() {
      _sessions = list;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("SESSION HISTORY & LOCAL LOGS", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const Text("Historical payload experiment execution sessions stored in local SQLite database", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
          const SizedBox(height: 20),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _sessions.length,
                    itemBuilder: (context, idx) {
                      final s = _sessions[idx];
                      final bool isPassed = s.finalStatus == "PASSED";
                      return Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.cardBackground,
                          border: Border.all(color: AppColors.cardBorder),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text("${s.experimentName} [${s.sessionId}]", style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                                const SizedBox(height: 4),
                                Text("Timestamp: ${s.timestamp} | Duration: ${s.durationSeconds}s | Steps: ${s.completedSteps}/${s.totalSteps}", style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                              ],
                            ),
                            Row(
                              children: [
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    Text("Confidence: ${(s.averageConfidence * 100).toStringAsFixed(1)}%", style: const TextStyle(fontSize: 12, color: AppColors.primaryCyan, fontWeight: FontWeight.bold)),
                                    Text("Avg FPS: ${s.averageFps} | Latency: ${s.averageLatencyMs}ms", style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                                  ],
                                ),
                                const SizedBox(width: 16),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: (isPassed ? AppColors.successEmerald : AppColors.warningAmber).withOpacity(0.2),
                                    border: Border.all(color: isPassed ? AppColors.successEmerald : AppColors.warningAmber),
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: Text(s.finalStatus, style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: isPassed ? AppColors.successEmerald : AppColors.warningAmber)),
                                ),
                              ],
                            ),
                          ],
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
