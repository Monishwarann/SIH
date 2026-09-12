import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class DataCollectionScreen extends StatefulWidget {
  const DataCollectionScreen({super.key});

  @override
  State<DataCollectionScreen> createState() => _DataCollectionScreenState();
}

class _DataCollectionScreenState extends State<DataCollectionScreen> {
  bool _isRecording = false;
  String _selectedAction = 'PICK_OBJECT';
  String _sequenceType = 'correct';
  String _participantId = 'P01';

  final List<String> _actions = [
    'APPROACH_OBJECT', 'IDENTIFY_OBJECT', 'REACH_OBJECT', 'PICK_OBJECT',
    'HOLD_OBJECT', 'MOVE_OBJECT', 'PLACE_OBJECT', 'OPEN_CONTAINER',
    'CLOSE_CONTAINER', 'TOUCH_DISPLAY', 'PRESS_BUTTON', 'INSPECT_OBJECT'
  ];

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("DATASET COLLECTION STUDIO", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const Text("Record and label custom space experiment activity video samples locally into datasets/BAS/", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
          const SizedBox(height: 20),
          Expanded(
            child: Row(
              children: [
                Expanded(
                  flex: 3,
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.black,
                      border: Border.all(color: AppColors.cardBorder),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Stack(
                      children: [
                        Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(_isRecording ? Icons.fiber_manual_record : Icons.camera_alt_outlined, size: 56, color: _isRecording ? AppColors.errorRed : AppColors.textMuted),
                              const SizedBox(height: 12),
                              Text(_isRecording ? "RECORDING SAMPLE DATASET FEED..." : "CAMERA READY FOR RECORDING", style: TextStyle(color: _isRecording ? AppColors.errorRed : AppColors.primaryCyan, fontWeight: FontWeight.bold, fontSize: 14)),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                  flex: 2,
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      border: Border.all(color: AppColors.cardBorder),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("SAMPLE LABEL METADATA", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        const Text("Participant ID:", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                        const SizedBox(height: 4),
                        TextField(
                          decoration: InputDecoration(
                            hintText: "P01",
                            filled: true,
                            fillColor: AppColors.background,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                          ),
                          onChanged: (v) => _participantId = v,
                        ),
                        const SizedBox(height: 16),
                        const Text("Target BAS Action Class:", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                        const SizedBox(height: 4),
                        DropdownButtonFormField<String>(
                          value: _selectedAction,
                          dropdownColor: AppColors.cardBackground,
                          items: _actions.map((a) => DropdownMenuItem(value: a, child: Text(a, style: const TextStyle(fontSize: 12)))).toList(),
                          onChanged: (v) => setState(() => _selectedAction = v!),
                          decoration: InputDecoration(
                            filled: true,
                            fillColor: AppColors.background,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                          ),
                        ),
                        const SizedBox(height: 16),
                        const Text("Sequence Quality Type:", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                        const SizedBox(height: 4),
                        DropdownButtonFormField<String>(
                          value: _sequenceType,
                          dropdownColor: AppColors.cardBackground,
                          items: ['correct', 'skipped', 'wrong_order', 'wrong_object']
                              .map((t) => DropdownMenuItem(value: t, child: Text(t.toUpperCase(), style: const TextStyle(fontSize: 12))))
                              .toList(),
                          onChanged: (v) => setState(() => _sequenceType = v!),
                          decoration: InputDecoration(
                            filled: true,
                            fillColor: AppColors.background,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                          ),
                        ),
                        const Spacer(),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton.icon(
                            onPressed: () {
                              setState(() {
                                _isRecording = !_isRecording;
                              });
                            },
                            icon: Icon(_isRecording ? Icons.stop : Icons.fiber_manual_record, color: Colors.white),
                            label: Text(_isRecording ? "STOP & SAVE SAMPLE" : "START RECORDING SAMPLE"),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: _isRecording ? AppColors.errorRed : AppColors.successEmerald,
                              padding: const EdgeInsets.symmetric(vertical: 14),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
