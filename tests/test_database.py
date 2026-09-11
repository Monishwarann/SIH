import unittest
from backend.database.db_service import DBService, db_service

class TestDatabaseService(unittest.TestCase):

    def setUp(self):
        self.db = DBService()

    def test_db_info(self):
        info = self.db.get_db_info()
        self.assertIn("configured_engine", info)
        self.assertIn("active_engine", info)
        self.assertIn("status", info)

    def test_save_and_get_experiment(self):
        exp_data = {
            "id": "EXP_TEST_001",
            "name": "Test Experiment",
            "description": "PostgreSQL & SQLite integration test",
            "steps": [
                {"name": "Step 1", "activity": "REACH", "object": "red_box"}
            ]
        }
        self.db.save_experiment(exp_data)
        exps = self.db.get_experiments()
        self.assertTrue(any(e["id"] == "EXP_TEST_001" for e in exps))

    def test_session_logging(self):
        session_id = "SESS_TEST_999"
        self.db.log_session_start(session_id, "EXP_TEST_001", 5)
        self.db.log_step(session_id, 1, "Reach Red Box", 0.95, "COMPLETED", {"evidence": "test"})
        history = self.db.get_session_history()
        self.assertTrue(any(s["session_id"] == session_id for s in history))

if __name__ == "__main__":
    unittest.main()
