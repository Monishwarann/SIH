import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LiveWaveformGraph extends StatelessWidget {
  final List<double> dataPoints;
  final String title;
  final String unit;
  final Color lineColor;
  final double minValue;
  final double maxValue;

  const LiveWaveformGraph({
    super.key,
    required this.dataPoints,
    required this.title,
    required this.unit,
    this.lineColor = AppColors.primaryCyan,
    this.minValue = 0.0,
    this.maxValue = 60.0,
  });

  @override
  Widget build(BuildContext context) {
    final currentValue = dataPoints.isNotEmpty ? dataPoints.last : 0.0;

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.cardBackground.withOpacity(0.8),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title.toUpperCase(),
                style: const TextStyle(
                  color: AppColors.textSecondary,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.1,
                ),
              ),
              Text(
                '${currentValue.toStringAsFixed(1)} $unit',
                style: TextStyle(
                  color: lineColor,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: CustomPaint(
                size: Size.infinite,
                painter: _WaveformPainter(
                  dataPoints: dataPoints,
                  lineColor: lineColor,
                  minValue: minValue,
                  maxValue: maxValue,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _WaveformPainter extends CustomPainter {
  final List<double> dataPoints;
  final Color lineColor;
  final double minValue;
  final double maxValue;

  _WaveformPainter({
    required this.dataPoints,
    required this.lineColor,
    required this.minValue,
    required this.maxValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (dataPoints.isEmpty) return;

    final bgPaint = Paint()..color = const Color(0xFF050B14);
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), bgPaint);

    final gridPaint = Paint()
      ..color = AppColors.cardBorder.withOpacity(0.4)
      ..strokeWidth = 0.5;

    for (int i = 1; i < 4; i++) {
      final y = size.height * (i / 4);
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    final path = Path();
    final fillPath = Path();

    final stepX = size.width / (math_max(1, dataPoints.length - 1));
    final rangeY = (maxValue - minValue) <= 0 ? 1.0 : (maxValue - minValue);

    for (int i = 0; i < dataPoints.length; i++) {
      final val = dataPoints[i].clamp(minValue, maxValue);
      final normY = (val - minValue) / rangeY;
      final x = i * stepX;
      final y = size.height - (normY * size.height);

      if (i == 0) {
        path.moveTo(x, y);
        fillPath.moveTo(x, size.height);
        fillPath.lineTo(x, y);
      } else {
        path.lineTo(x, y);
        fillPath.lineTo(x, y);
      }
    }

    if (dataPoints.isNotEmpty) {
      fillPath.lineTo((dataPoints.length - 1) * stepX, size.height);
      fillPath.close();

      final fillGradient = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          lineColor.withOpacity(0.35),
          lineColor.withOpacity(0.0),
        ],
      );

      final fillPaint = Paint()
        ..shader = fillGradient.createShader(Rect.fromLTWH(0, 0, size.width, size.height));
      canvas.drawPath(fillPath, fillPaint);
    }

    final linePaint = Paint()
      ..color = lineColor
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    canvas.drawPath(path, linePaint);
  }

  double math_max(int a, int b) => (a > b ? a : b).toDouble();

  @override
  bool shouldRepaint(covariant _WaveformPainter oldDelegate) {
    return oldDelegate.dataPoints != dataPoints;
  }
}
