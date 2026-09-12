import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import '../models/session_model.dart';

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  Database? _db;

  Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDb();
    return _db!;
  }

  Future<Database> _initDb() async {
    if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
      sqfliteFfiInit();
      databaseFactory = databaseFactoryFfi;
    }

    final docsDir = await getApplicationDocumentsDirectory();
    final dbPath = join(docsDir.path, 'astra_har_sessions.db');

    return await openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE sessions (
            session_id TEXT PRIMARY KEY,
            experiment_name TEXT,
            timestamp TEXT,
            duration_seconds REAL,
            total_steps INTEGER,
            completed_steps INTEGER,
            skipped_steps INTEGER,
            wrong_actions INTEGER,
            wrong_objects INTEGER,
            timeouts INTEGER,
            average_confidence REAL,
            average_fps REAL,
            average_latency_ms REAL,
            final_status TEXT
          )
        ''');
      },
    );
  }

  Future<void> saveSession(SessionRecord session) async {
    try {
      final db = await database;
      await db.insert(
        'sessions',
        session.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    } catch (e) {
      debugPrint('[DatabaseService] Failed to save session: $e');
    }
  }

  Future<List<SessionRecord>> getAllSessions() async {
    try {
      final db = await database;
      final maps = await db.query('sessions', orderBy: 'timestamp DESC');
      return maps.map((m) => SessionRecord.fromJson(m)).toList();
    } catch (e) {
      debugPrint('[DatabaseService] Failed to fetch sessions: $e');
      return [];
    }
  }
}
