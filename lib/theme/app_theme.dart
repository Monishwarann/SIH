import 'package:flutter/material.dart';

class AppColors {
  // Primary Palette
  static const Color background = Color(0xFF020617); // Slate 950
  static const Color surface = Color(0xFF0B132B); // Dark Navy Surface
  static const Color cardBackground = Color(0xFF0F172A); // Slate 900
  static const Color cardBorder = Color(0xFF1E293B); // Slate 800

  // Accents & Brand
  static const Color primaryCyan = Color(0xFF06B6D4); // Cyan 500
  static const Color primaryCyanGlow = Color(0x3306B6D4);
  static const Color secondaryBlue = Color(0xFF3B82F6); // Blue 500
  static const Color accentPurple = Color(0xFFA855F7); // Purple 500
  static const Color accentNeon = Color(0xFF00F0FF); // Neon Cyan

  // Status Colors
  static const Color successEmerald = Color(0xFF10B981); // Emerald 500
  static const Color warningAmber = Color(0xFFF59E0B); // Amber 500
  static const Color errorRed = Color(0xFFEF4444); // Red 500

  // Text Colors
  static const Color textPrimary = Color(0xFFF8FAFC); // Slate 50
  static const Color textSecondary = Color(0xFF94A3B8); // Slate 400
  static const Color textMuted = Color(0xFF64748B); // Slate 500
}

class AppTypography {
  static const TextStyle hudTitle = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
    letterSpacing: 1.2,
  );

  static const TextStyle sectionHeader = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.bold,
    color: AppColors.primaryCyan,
    letterSpacing: 1.0,
  );

  static const TextStyle body = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    color: AppColors.textSecondary,
  );

  static const TextStyle labelMuted = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.w600,
    color: AppColors.textMuted,
    letterSpacing: 0.8,
  );

  static const TextStyle badgeText = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.bold,
    letterSpacing: 0.8,
  );
}

class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 12.0;
  static const double lg = 16.0;
  static const double xl = 24.0;

  static const double radiusSm = 6.0;
  static const double radiusMd = 12.0;
  static const double radiusLg = 16.0;
}

class AppDecorations {
  static BoxDecoration glassBox({
    Color? backgroundColor,
    Color? borderColor,
    double borderRadius = AppSpacing.radiusMd,
    bool isHovered = false,
  }) {
    final border = borderColor ?? (isHovered ? AppColors.primaryCyan : AppColors.cardBorder);
    final bg = backgroundColor ?? AppColors.cardBackground.withValues(alpha: 0.75);

    return BoxDecoration(
      color: bg,
      borderRadius: BorderRadius.circular(borderRadius),
      border: Border.all(
        color: border,
        width: isHovered ? 1.5 : 1.0,
      ),
      boxShadow: [
        if (isHovered)
          BoxShadow(
            color: (borderColor ?? AppColors.primaryCyan).withValues(alpha: 0.25),
            blurRadius: 18,
            spreadRadius: 1,
          )
        else
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.35),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
      ],
    );
  }
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
          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.cardBackground,
        elevation: 0,
      ),
    );
  }
}

