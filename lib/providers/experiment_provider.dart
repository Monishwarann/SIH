import 'package:flutter/foundation.dart';
import '../models/experiment_model.dart';

class ExperimentProvider with ChangeNotifier {
  ExperimentProtocol _selectedProtocol = ExperimentProtocol(
    experimentId: "EXP_001",
    name: "Two-Box Sorting",
    description: "On-board BAS two-box sample sorting protocol.",
    steps: [
      ExperimentStep(id: 1, name: "Approach Container", action: "APPROACH_OBJECT", targetObject: "container", timeoutSeconds: 30),
      ExperimentStep(id: 2, name: "Identify Red Box", action: "IDENTIFY_OBJECT", targetObject: "red_box", timeoutSeconds: 25),
      ExperimentStep(id: 3, name: "Pick Sample", action: "PICK_OBJECT", targetObject: "red_box", timeoutSeconds: 20),
      ExperimentStep(id: 4, name: "Move Sample", action: "MOVE_OBJECT", targetObject: "target_area", timeoutSeconds: 25),
      ExperimentStep(id: 5, name: "Place Sample", action: "PLACE_OBJECT", targetObject: "target_area", timeoutSeconds: 20),
    ],
  );

  ExperimentProtocol get selectedProtocol => _selectedProtocol;

  void selectProtocol(ExperimentProtocol protocol) {
    _selectedProtocol = protocol;
    notifyListeners();
  }
}
