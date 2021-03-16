import unittest
from unittest import TestCase
from command_processor import Processor

class TestCommandProccessor(TestCase):
    
    def setUp(self):
        self.cmd_proc_instance = Processor()

    def test_if_methods_are_dispatched_correctly(self):
        self.assertEqual(
            self.cmd_proc_instance._Processor__dispatch_command(
                "cmd start_game"
            )["dispatched_method"].__name__,
            "start_game"
        )
        # check if it can handler errors properly
        self.assertEqual(
            self.cmd_proc_instance._Processor__dispatch_command("cmd _werosdf_")["error"],
            True
        )

if __name__ == "__main__": unittest.main()