import 'dart:convert';
import 'dart:io';
import 'package:csv/csv.dart';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import '../models/session_model.dart';

class ReportService {
  Future<String> exportToJson(SessionRecord session) async {
    final docsDir = await getApplicationDocumentsDirectory();
    final file = File('${docsDir.path}/${session.sessionId}_report.json');
    await file.writeAsString(jsonEncode(session.toMap()));
    return file.path;
  }

  Future<String> exportToCsv(SessionRecord session) async {
    final docsDir = await getApplicationDocumentsDirectory();
    final file = File('${docsDir.path}/${session.sessionId}_report.csv');

    List<List<dynamic>> rows = [
      ["Metric", "Value"],
      ["Session ID", session.sessionId],
      ["Experiment", session.experimentName],
      ["Timestamp", session.timestamp],
      ["Duration (s)", session.durationSeconds],
      ["Total Steps", session.totalSteps],
      ["Completed Steps", session.completedSteps],
      ["Skipped Steps", session.skippedSteps],
      ["Wrong Actions", session.wrongActions],
      ["Timeouts", session.timeouts],
      ["Average Confidence (%)", (session.averageConfidence * 100).toStringAsFixed(1)],
      ["Average FPS", session.averageFps],
      ["Average Latency (ms)", session.averageLatencyMs],
      ["Final Status", session.finalStatus],
    ];

    String csvData = const ListToCsvConverter().convert(rows);
    await file.writeAsString(csvData);
    return file.path;
  }

  Future<String> exportToPdf(SessionRecord session) async {
    final pdf = pw.Document();

    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text("ASTRA-HAR :: EXPERIMENT VALIDATION REPORT", style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold)),
              pw.Divider(),
              pw.SizedBox(height: 10),
              pw.Text("Session ID: ${session.sessionId}"),
              pw.Text("Experiment: ${session.experimentName}"),
              pw.Text("Date: ${session.timestamp}"),
              pw.Text("Duration: ${session.durationSeconds} s"),
              pw.Text("Status: ${session.finalStatus}"),
              pw.SizedBox(height: 15),
              pw.Text("PERFORMANCE METRICS", style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
              pw.Bullet(text: "Total Steps: ${session.totalSteps}"),
              pw.Bullet(text: "Completed Steps: ${session.completedSteps}"),
              pw.Bullet(text: "Skipped Steps: ${session.skippedSteps}"),
              pw.Bullet(text: "Wrong Actions: ${session.wrongActions}"),
              pw.Bullet(text: "Timeouts: ${session.timeouts}"),
              pw.Bullet(text: "Average Confidence: ${(session.averageConfidence * 100).toStringAsFixed(1)}%"),
              pw.Bullet(text: "Average FPS: ${session.averageFps}"),
              pw.Bullet(text: "Average Latency: ${session.averageLatencyMs} ms"),
            ],
          );
        },
      ),
    );

    final docsDir = await getApplicationDocumentsDirectory();
    final file = File('${docsDir.path}/${session.sessionId}_report.pdf');
    await file.writeAsBytes(await pdf.save());
    return file.path;
  }
}
