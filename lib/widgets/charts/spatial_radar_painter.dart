import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../models/telemetry_model.dart';
import '../../theme/app_theme.dart';

class SpatialRadarWidget extends StatefulWidget {
  final TelemetryData telemetry;

  const SpatialRadarWidget({
    super.key,
    required this.telemetry,
  });

  @override
  State<SpatialRadarWidget> createState() => _SpatialRadarWidgetState();
}

class _SpatialRadarWidgetState extends State<SpatialRadarWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _sweepController;

  @override
  void initState() {
    super.initState();
    _sweepController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 4),
    )..repeat();
  }

  @override
  void dispose() {
    _sweepController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _sweepController,
      builder: (context, child) {
        return CustomPaint(
          size: Size.infinite,
          painter: SpatialRadarPainter(
            telemetry: widget.telemetry,
            sweepAngle: _sweepController.value * 2 * math.pi,
          ),
        );
      },
    );
  }
}

class SpatialRadarPainter extends CustomPainter {
  final TelemetryData telemetry;
  final double sweepAngle;

  SpatialRadarPainter({
    required this.telemetry,
    required this.sweepAngle,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = math.min(size.width, size.height) / 2 - 16;

    if (maxRadius <= 0) return;

    final bgPaint = Paint()..color = const Color(0xFF030712);
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), bgPaint);

    // 1. Draw Concentric Sonar Rings
    final ringPaint = Paint()
      ..color = AppColors.primaryCyan.withValues(alpha: 0.18)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    final ringDashPaint = Paint()
      ..color = AppColors.primaryCyan.withValues(alpha: 0.08)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    for (int i = 1; i <= 4; i++) {
      final r = maxRadius * (i / 4);
      canvas.drawCircle(center, r, ringPaint);
    }

    // 2. Draw Crosshairs & Axis Grid
    final axisPaint = Paint()
      ..color = AppColors.primaryCyan.withValues(alpha: 0.25)
      ..strokeWidth = 1.0;

    canvas.drawLine(
        Offset(center.dx - maxRadius, center.dy),
        Offset(center.dx + maxRadius, center.dy),
        axisPaint);
    canvas.drawLine(
        Offset(center.dx, center.dy - maxRadius),
        Offset(center.dx, center.dy + maxRadius),
        axisPaint);

    // Diagonal lines
    for (var angle in [math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4]) {
      final dx = center.dx + maxRadius * math.cos(angle);
      final dy = center.dy + maxRadius * math.sin(angle);
      canvas.drawLine(center, Offset(dx, dy), ringDashPaint);
    }

    // 3. Draw Rotating Radar Sweep Shader Line
    final sweepPaint = Paint()
      ..shader = SweepGradient(
        center: Alignment.center,
        startAngle: 0.0,
        endAngle: math.pi / 2,
        colors: [
          AppColors.primaryCyan.withValues(alpha: 0.4),
          AppColors.primaryCyan.withValues(alpha: 0.0),
        ],
        stops: const [0.0, 1.0],
        transform: GradientRotation(sweepAngle),
      ).createShader(Rect.fromCircle(center: center, radius: maxRadius));

    canvas.drawCircle(center, maxRadius, sweepPaint);

    final sweepLineEnd = Offset(
      center.dx + maxRadius * math.cos(sweepAngle),
      center.dy + maxRadius * math.sin(sweepAngle),
    );
    final sweepLinePaint = Paint()
      ..color = AppColors.primaryCyan
      ..strokeWidth = 1.5;
    canvas.drawLine(center, sweepLineEnd, sweepLinePaint);

    // 4. Draw Detected Payload Objects
    for (int i = 0; i < telemetry.objects.length; i++) {
      final obj = telemetry.objects[i];
      final normX = (obj.x / 640.0) * 2 - 1;
      final normY = (obj.y / 480.0) * 2 - 1;

      final posX = center.dx + normX * (maxRadius * 0.7);
      final posY = center.dy + normY * (maxRadius * 0.7);
      final objOffset = Offset(posX, posY);

      final isAlert = telemetry.status != 'CORRECT';
      final dotColor = isAlert ? AppColors.warningAmber : AppColors.successEmerald;

      // Glow circle
      final glowPaint = Paint()
        ..color = dotColor.withValues(alpha: 0.3)
        ..style = PaintingStyle.fill;
      canvas.drawCircle(objOffset, 12, glowPaint);

      final dotPaint = Paint()..color = dotColor;
      canvas.drawCircle(objOffset, 5, dotPaint);

      // Connecting line from center to object
      final linePaint = Paint()
        ..color = dotColor.withValues(alpha: 0.4)
        ..strokeWidth = 1.0;
      canvas.drawLine(center, objOffset, linePaint);

      // Label text
      final textSpan = TextSpan(
        text: '${obj.name} (${(obj.confidence * 100).toInt()}%)',
        style: const TextStyle(
          color: AppColors.textPrimary,
          fontSize: 9,
          fontWeight: FontWeight.bold,
        ),
      );
      final textPainter = TextPainter(
        text: textSpan,
        textDirection: TextDirection.ltr,
      );
      textPainter.layout();
      textPainter.paint(canvas, Offset(posX + 8, posY - 6));
    }

    // 5. Draw Hand Landmark Points & Astronaut Position
    if (telemetry.handsDetected > 0) {
      final handPaint = Paint()..color = AppColors.primaryCyan;
      final handGlow = Paint()
        ..color = AppColors.primaryCyan.withValues(alpha: 0.35);

      final hand1 = Offset(center.dx - 24, center.dy + 18);
      final hand2 = Offset(center.dx + 28, center.dy + 12);

      canvas.drawCircle(hand1, 8, handGlow);
      canvas.drawCircle(hand1, 4, handPaint);

      if (telemetry.handsDetected > 1) {
        canvas.drawCircle(hand2, 8, handGlow);
        canvas.drawCircle(hand2, 4, handPaint);
      }
    }

    // 6. Cardinal Compass Directions Text
    const compassStyle = TextStyle(
      color: AppColors.primaryCyan,
      fontSize: 10,
      fontWeight: FontWeight.bold,
    );
    _drawText(canvas, "N", Offset(center.dx - 4, center.dy - maxRadius + 4), compassStyle);
    _drawText(canvas, "S", Offset(center.dx - 4, center.dy + maxRadius - 14), compassStyle);
    _drawText(canvas, "W", Offset(center.dx - maxRadius + 4, center.dy - 6), compassStyle);
    _drawText(canvas, "E", Offset(center.dx + maxRadius - 12, center.dy - 6), compassStyle);
  }

  void _drawText(Canvas canvas, String text, Offset offset, TextStyle style) {
    final textPainter = TextPainter(
      text: TextSpan(text: text, style: style),
      textDirection: TextDirection.ltr,
    );
    textPainter.layout();
    textPainter.paint(canvas, offset);
  }

  @override
  bool shouldRepaint(covariant SpatialRadarPainter oldDelegate) {
    return oldDelegate.sweepAngle != sweepAngle ||
        oldDelegate.telemetry != telemetry;
  }
}
