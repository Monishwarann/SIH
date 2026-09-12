import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/realtime_provider.dart';
import 'theme/app_theme.dart';
import 'widgets/header_bar.dart';
import 'widgets/navigation_sidebar.dart';
import 'screens/dashboard_screen.dart';
import 'screens/live_monitoring_screen.dart';
import 'screens/experiment_selector_screen.dart';
import 'screens/data_collection_screen.dart';
import 'screens/session_history_screen.dart';
import 'screens/reports_screen.dart';
import 'screens/settings_screen.dart';

class AstraHarApp extends StatelessWidget {
  const AstraHarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ASTRA-HAR :: On-board BAS HAR Monitor (ISRO PS 26174)',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const MainShell(),
    );
  }
}

class MainShell extends StatelessWidget {
  const MainShell({super.key});

  @override
  Widget build(BuildContext context) {
    final activeTab = Provider.of<RealtimeProvider>(context).activeTab;

    Widget renderContent() {
      switch (activeTab) {
        case 'dashboard':
          return const DashboardScreen();
        case 'live':
          return const LiveMonitoringScreen();
        case 'experiments':
          return const ExperimentSelectorScreen();
        case 'data_collection':
          return const DataCollectionScreen();
        case 'history':
          return const SessionHistoryScreen();
        case 'reports':
          return const ReportsScreen();
        case 'settings':
          return const SettingsScreen();
        default:
          return const DashboardScreen();
      }
    }

    return Scaffold(
      appBar: const HeaderBar(),
      body: Row(
        children: [
          const NavigationSidebar(),
          Expanded(child: renderContent()),
        ],
      ),
    );
  }
}
