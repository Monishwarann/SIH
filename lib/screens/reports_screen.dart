import 'package:flutter/material.dart';
import '../models/session_model.dart';
import '../services/report_service.dart';
import '../theme/app_theme.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  final ReportService _reportService = ReportService();
  String _message = '';

  final SessionRecord _activeSession = SessionRecord(
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
  );

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("EXPERIMENT REPORTS & EXPORT STUDIO", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const Text("Generate and export offline session reports in PDF, CSV, and JSON formats", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
          const SizedBox(height: 20),

          if (_message.isNotEmpty)
            Container(
              margin: const EdgeInsets.only(bottom: 16),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.primaryCyanGlow,
                border: Border.all(color: AppColors.primaryCyan),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Row(
                children: [
                  const Icon(Icons.check_circle, color: AppColors.primaryCyan, size: 18),
                  const SizedBox(width: 8),
                  Expanded(child: Text(_message, style: const TextStyle(fontSize: 12, color: AppColors.textPrimary))),
                ],
              ),
            ),

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
                Text("REPORT SUMMARY: ${_activeSession.experimentName} [${_activeSession.sessionId}]", style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const Divider(height: 20, color: AppColors.cardBorder),
                const SizedBox(height: 10),
                _buildRow("Session Timestamp:", _activeSession.timestamp),
                _buildRow("Total Session Duration:", "${_activeSession.durationSeconds} seconds"),
                _buildRow("Total Protocol Steps:", "${_activeSession.totalSteps}"),
                _buildRow("Completed Steps:", "${_activeSession.completedSteps}"),
                _buildRow("Skipped Steps Count:", "${_activeSession.skippedSteps}"),
                _buildRow("Wrong Sequence Actions:", "${_activeSession.wrongActions}"),
                _buildRow("Average Activity Confidence:", "${(_activeSession.averageConfidence * 100).toStringAsFixed(1)}%"),
                _buildRow("Average Pipeline Latency:", "${_activeSession.averageLatencyMs} ms"),
                _buildRow("Validation Status:", _activeSession.finalStatus),
                const SizedBox(height: 20),
                Row(
                  children: [
                    ElevatedButton.icon(
                      onPressed: () async {
                        final path = await _reportService.exportToPdf(_activeSession);
                        setState(() => _message = "Exported PDF Report to: $path");
                      },
                      icon: const Icon(Icons.picture_as_pdf, size: 16),
                      label: const Text("EXPORT PDF"),
                      style: ElevatedButton.styleFrom(backgroundColor: AppColors.errorRed, foregroundColor: Colors.white),
                    ),
                    const SizedBox(width: 12),
                    ElevatedButton.icon(
                      onPressed: () async {
                        final path = await _reportService.exportToCsv(_activeSession);
                        setState(() => _message = "Exported CSV Data to: $path");
                      },
                      icon: const Icon(Icons.table_chart, size: 16),
                      label: const Text("EXPORT CSV"),
                      style: ElevatedButton.styleFrom(backgroundColor: AppColors.successEmerald, foregroundColor: Colors.white),
                    ),
                    const SizedBox(width: 12),
                    ElevatedButton.icon(
                      onPressed: () async {
                        final path = await _reportService.exportToJson(_activeSession);
                        setState(() => _message = "Exported JSON Log to: $path");
                      },
                      icon: const Icon(Icons.code, size: 16),
                      label: const Text("EXPORT JSON"),
                      style: ElevatedButton.styleFrom(backgroundColor: AppColors.primaryCyan, foregroundColor: Colors.black),
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

  Widget _buildRow(String label, String val) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
          Text(val, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
        ],
      ),
    );
  }
}
