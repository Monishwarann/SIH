import 'dart:ui';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class GlassCard extends StatefulWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final double width;
  final double? height;
  final Color? borderColor;
  final Color? backgroundColor;
  final double borderRadius;
  final double blurSigma;
  final Gradient? gradient;
  final VoidCallback? onTap;

  const GlassCard({
    super.key,
    required this.child,
    this.padding,
    this.margin,
    this.width = double.infinity,
    this.height,
    this.borderColor,
    this.backgroundColor,
    this.borderRadius = 12.0,
    this.blurSigma = 12.0,
    this.gradient,
    this.onTap,
  });

  factory GlassCard.frosted({
    required Widget child,
    EdgeInsetsGeometry? padding,
    EdgeInsetsGeometry? margin,
    double width = double.infinity,
    double? height,
    double borderRadius = 12.0,
    VoidCallback? onTap,
  }) {
    return GlassCard(
      padding: padding,
      margin: margin,
      width: width,
      height: height,
      borderRadius: borderRadius,
      blurSigma: 16.0,
      backgroundColor: const Color(0x1A0F172A),
      borderColor: const Color(0x3300F0FF),
      onTap: onTap,
      child: child,
    );
  }

  factory GlassCard.neon({
    required Widget child,
    required Color neonColor,
    EdgeInsetsGeometry? padding,
    EdgeInsetsGeometry? margin,
    double width = double.infinity,
    double? height,
    double borderRadius = 12.0,
    VoidCallback? onTap,
  }) {
    return GlassCard(
      padding: padding,
      margin: margin,
      width: width,
      height: height,
      borderRadius: borderRadius,
      blurSigma: 14.0,
      backgroundColor: neonColor.withValues(alpha: 0.08),
      borderColor: neonColor.withValues(alpha: 0.6),
      onTap: onTap,
      child: child,
    );
  }

  factory GlassCard.gradient({
    required Widget child,
    required Gradient gradient,
    EdgeInsetsGeometry? padding,
    EdgeInsetsGeometry? margin,
    double width = double.infinity,
    double? height,
    double borderRadius = 12.0,
    VoidCallback? onTap,
  }) {
    return GlassCard(
      padding: padding,
      margin: margin,
      width: width,
      height: height,
      borderRadius: borderRadius,
      blurSigma: 14.0,
      gradient: gradient,
      borderColor: Colors.white.withValues(alpha: 0.2),
      onTap: onTap,
      child: child,
    );
  }

  @override
  State<GlassCard> createState() => _GlassCardState();
}

class _GlassCardState extends State<GlassCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    final effectiveBorderColor = widget.borderColor ??
        (_isHovered ? AppColors.primaryCyan : AppColors.cardBorder);
    final effectiveBgColor = widget.backgroundColor ??
        AppColors.cardBackground.withValues(alpha: 0.75);

    Widget content = ClipRRect(
      borderRadius: BorderRadius.circular(widget.borderRadius),
      child: BackdropFilter(
        filter: ImageFilter.blur(
            sigmaX: widget.blurSigma, sigmaY: widget.blurSigma),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          width: widget.width,
          height: widget.height,
          padding: widget.padding ?? const EdgeInsets.all(16),
          margin: widget.margin,
          decoration: BoxDecoration(
            color: widget.gradient == null ? effectiveBgColor : null,
            gradient: widget.gradient,
            borderRadius: BorderRadius.circular(widget.borderRadius),
            border: Border.all(
              color: effectiveBorderColor,
              width: _isHovered ? 1.5 : 1.0,
            ),
            boxShadow: [
              if (_isHovered)
                BoxShadow(
                  color: (widget.borderColor ?? AppColors.primaryCyan)
                      .withValues(alpha: 0.25),
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
          ),
          child: widget.child,
        ),
      ),
    );

    if (widget.onTap != null) {
      return MouseRegion(
        onEnter: (_) => setState(() => _isHovered = true),
        onExit: (_) => setState(() => _isHovered = false),
        cursor: SystemMouseCursors.click,
        child: GestureDetector(
          onTap: widget.onTap,
          child: content,
        ),
      );
    }

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: content,
    );
  }
}
