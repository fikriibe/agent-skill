import unittest
import os
import shutil
import json
import sys

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
import team_manager

class TestTeamManager(unittest.TestCase):
    def setUp(self):
        # Override team dir function for testing to avoid touching real teams/
        self.original_get_team_dir = team_manager.get_team_dir
        team_manager.get_team_dir = lambda name: os.path.join("test_teams", name)
        os.makedirs("test_teams", exist_ok=True)

    def tearDown(self):
        # Restore and clean up
        team_manager.get_team_dir = self.original_get_team_dir
        if os.path.exists("test_teams"):
            shutil.rmtree("test_teams")

    def test_init_team(self):
        team_manager.init_team("test_feature", ["fe", "be"])
        team_dir = os.path.join("test_teams", "test_feature")
        
        # Check config exists
        self.assertTrue(os.path.exists(os.path.join(team_dir, "config.json")))
        
        # Check inboxes
        self.assertTrue(os.path.exists(os.path.join(team_dir, "inboxes", "fe")))
        self.assertTrue(os.path.exists(os.path.join(team_dir, "inboxes", "be")))
        
        # Check config data
        config = team_manager.load_team_config("test_feature")
        self.assertEqual(config["team_name"], "test_feature")
        self.assertEqual(config["phase"], "PLANNING")
        self.assertEqual(config["required_roles"], ["fe", "be"])

    def test_approve_phases(self):
        team_manager.init_team("test_feature", ["fe", "be"])
        
        # Approve to DEV
        team_manager.approve_phase("test_feature")
        config = team_manager.load_team_config("test_feature")
        self.assertEqual(config["phase"], "DEV")
        self.assertEqual(config["active_agents"], ["fe", "be"])
        
        # Check inbox message
        fe_mailbox = os.path.join("test_teams", "test_feature", "inboxes", "fe", "mailbox.md")
        with open(fe_mailbox, "r") as f:
            content = f.read()
        self.assertIn("Phase Started: DEVELOPMENT", content)

if __name__ == "__main__":
    unittest.main()
