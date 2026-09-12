import 'package:flutter/material.dart';

class AppColors {
  static const Color background = Color(0xFF020617); // Slate 950
  static const Color cardBackground = Color(0xFF0F172A); // Slate 900
  static const Color cardBorder = Color(0xFF1E293B); // Slate 800
  
  static const Color primaryCyan = Color(0xFF06B6D4); // Cyan 500
  static const Color primaryCyanGlow = Color(0x3306B6D4);
  
  static const Color successEmerald = Color(0xFF10B981); // Emerald 500
  static const Color warningAmber = Color(0xFFF59E0B); // Amber 500
  static const Color errorRed = Color(0xFFEF4444); // Red 500
  static const Color accentPurple = Color(0xFFA855F7); // Purple 500

  static const Color textPrimary = Color(0xFFF8FAFC); // Slate 50
  static const Color textSecondary = Color(0xFF94A3B8); // Slate 400
  static const Color textMuted = Color(0xFF64748B); // Slate 500
}

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData.dark().copyWith(
      scaffoldBackgroundColor: AppColors.background,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primaryCyan,
        surface: AppColors.cardBackground,
        error: AppColors.errorRed,
      ),
      cardTheme: CardThemeData(
        color: AppColors.cardBackground,
        shape: RoundedRectangleBorder(
          side: const BorderSide(color: AppColors.cardBorder, width: 1),
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.cardBackground,
        elevation: 0,
      ),
    );
  }
}
