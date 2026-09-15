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
    this.onTap,
  });

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
        AppColors.cardBackground.withOpacity(0.75);

    Widget content = ClipRRect(
      borderRadius: BorderRadius.circular(widget.borderRadius),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          width: widget.width,
          height: widget.height,
          padding: widget.padding ?? const EdgeInsets.all(16),
          margin: widget.margin,
          decoration: BoxDecoration(
            color: effectiveBgColor,
            borderRadius: BorderRadius.circular(widget.borderRadius),
            border: Border.all(
              color: effectiveBorderColor,
              width: _isHovered ? 1.5 : 1.0,
            ),
            boxShadow: [
              if (_isHovered)
                BoxShadow(
                  color: (widget.borderColor ?? AppColors.primaryCyan)
                      .withOpacity(0.2),
                  blurRadius: 16,
                  spreadRadius: 1,
                )
              else
                BoxShadow(
                  color: Colors.black.withOpacity(0.3),
                  blurRadius: 8,
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
