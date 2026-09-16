import 'package:flutter/material.dart';
import '../screens/dashboard_screen.dart';
import '../screens/live_monitoring_screen.dart';
import '../screens/experiment_selector_screen.dart';
import '../screens/data_collection_screen.dart';
import '../screens/session_history_screen.dart';
import '../screens/reports_screen.dart';
import '../screens/settings_screen.dart';

class AppRoutes {
  static const String dashboard = '/dashboard';
  static const String live = '/live';
  static const String experiments = '/experiments';
  static const String dataCollection = '/data_collection';
  static const String history = '/history';
  static const String reports = '/reports';
  static const String settings = '/settings';

  static final Map<String, String> tabToRoute = {
    'dashboard': dashboard,
    'live': live,
    'experiments': experiments,
    'data_collection': dataCollection,
    'history': history,
    'reports': reports,
    'settings': settings,
  };

  static final Map<String, String> routeToTab = {
    dashboard: 'dashboard',
    live: 'live',
    experiments: 'experiments',
    dataCollection: 'data_collection',
    history: 'history',
    reports: 'reports',
    settings: 'settings',
  };

  static Route<dynamic> generateRoute(RouteSettings routeSettings) {
    Widget page;
    switch (routeSettings.name) {
      case dashboard:
        page = const DashboardScreen();
        break;
      case live:
        page = const LiveMonitoringScreen();
        break;
      case experiments:
        page = const ExperimentSelectorScreen();
        break;
      case dataCollection:
        page = const DataCollectionScreen();
        break;
      case history:
        page = const SessionHistoryScreen();
        break;
      case reports:
        page = const ReportsScreen();
        break;
      case settings:
        page = const SettingsScreen();
        break;
      default:
        page = const DashboardScreen();
    }

    return PageRouteBuilder(
      settings: routeSettings,
      pageBuilder: (_, __, ___) => page,
      transitionsBuilder: (_, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: animation,
          child: child,
        );
      },
      transitionDuration: const Duration(milliseconds: 150),
    );
  }
}
