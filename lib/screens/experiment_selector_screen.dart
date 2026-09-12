import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/experiment_provider.dart';
import '../models/experiment_model.dart';
import '../theme/app_theme.dart';

class ExperimentSelectorScreen extends StatelessWidget {
  const ExperimentSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final expProvider = Provider.of<ExperimentProvider>(context);
    final selected = expProvider.selectedProtocol;

    final protocols = [
      ExperimentProtocol(
        experimentId: "EXP_001",
        name: "Two-Box Sorting Protocol",
        description: "On-board BAS two-box sample sorting protocol for microgravity payloads.",
        steps: [
          ExperimentStep(id: 1, name: "Approach Container", action: "APPROACH_OBJECT", targetObject: "container", timeoutSeconds: 30),
          ExperimentStep(id: 2, name: "Identify Red Box", action: "IDENTIFY_OBJECT", targetObject: "red_box", timeoutSeconds: 25),
          ExperimentStep(id: 3, name: "Pick Sample", action: "PICK_OBJECT", targetObject: "red_box", timeoutSeconds: 20),
          ExperimentStep(id: 4, name: "Move Sample", action: "MOVE_OBJECT", targetObject: "target_area", timeoutSeconds: 25),
          ExperimentStep(id: 5, name: "Place Sample", action: "PLACE_OBJECT", targetObject: "target_area", timeoutSeconds: 20),
        ],
      ),
      ExperimentProtocol(
        experimentId: "EXP_002",
        name: "Electronic Display Interaction",
        description: "BAS Display payload diagnostic and sensor calibration experiment protocol.",
        steps: [
          ExperimentStep(id: 1, name: "Approach Display", action: "APPROACH_OBJECT", targetObject: "display", timeoutSeconds: 20),
          ExperimentStep(id: 2, name: "Touch Screen", action: "TOUCH_DISPLAY", targetObject: "display", timeoutSeconds: 15),
          ExperimentStep(id: 3, name: "Press Switch", action: "PRESS_BUTTON", targetObject: "button", timeoutSeconds: 15),
          ExperimentStep(id: 4, name: "Inspect Diagnostic", action: "INSPECT_OBJECT", targetObject: "display", timeoutSeconds: 20),
        ],
      ),
    ];

    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("EXPERIMENT PROTOCOL SELECTOR", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const Text("Select or load JSON protocol configuration for on-board HAR sequence validation", style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
          const SizedBox(height: 20),
          Expanded(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  flex: 2,
                  child: ListView.builder(
                    itemCount: protocols.length,
                    itemBuilder: (context, idx) {
                      final p = protocols[idx];
                      final bool isSelected = p.experimentId == selected.experimentId;
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        color: isSelected ? AppColors.primaryCyanGlow : AppColors.cardBackground,
                        shape: RoundedRectangleBorder(
                          side: BorderSide(color: isSelected ? AppColors.primaryCyan : AppColors.cardBorder),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: ListTile(
                          title: Text(p.name, style: TextStyle(fontWeight: FontWeight.bold, color: isSelected ? AppColors.primaryCyan : AppColors.textPrimary)),
                          subtitle: Text(p.description, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                          trailing: Text("${p.steps.length} Steps", style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                          onTap: () => expProvider.selectProtocol(p),
                        ),
                      );
                    },
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                  flex: 3,
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
                        Text("PROTOCOL STEPS: ${selected.name.toUpperCase()}", style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                        const Divider(height: 20, color: AppColors.cardBorder),
                        Expanded(
                          child: ListView.builder(
                            itemCount: selected.steps.length,
                            itemBuilder: (context, sIdx) {
                              final step = selected.steps[sIdx];
                              return Container(
                                margin: const EdgeInsets.only(bottom: 8),
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: AppColors.background,
                                  border: Border.all(color: AppColors.cardBorder),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Row(
                                  children: [
                                    CircleAvatar(
                                      radius: 12,
                                      backgroundColor: AppColors.primaryCyanGlow,
                                      child: Text("${step.id}", style: const TextStyle(fontSize: 11, color: AppColors.primaryCyan, fontWeight: FontWeight.bold)),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(step.name, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                                          Text("Action: ${step.action} | Timeout: ${step.timeoutSeconds}s", style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            },
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
