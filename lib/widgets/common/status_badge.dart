import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class StatusBadge extends StatelessWidget {
  final String label;
  final bool isSuccess;
  final IconData? icon;
  final Color? customColor;

  const StatusBadge({
    super.key,
    required this.label,
    required this.isSuccess,
    this.icon,
    this.customColor,
  });

  @override
  Widget build(BuildContext context) {
    final color = customColor ??
        (isSuccess ? AppColors.successEmerald : AppColors.errorRed);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        border: Border.all(color: color),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: color.withValues(alpha: 0.2),
            blurRadius: 8,
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon ?? Icons.circle,
            size: 8,
            color: color,
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.bold,
              color: color,
              letterSpacing: 0.8,
            ),
          ),
        ],
      ),
    );
  }
}
