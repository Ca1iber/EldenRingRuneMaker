import unittest

from ERScript import RUNE_FARM_SEQUENCE, KeyAction, SleepAction, run_rune_cycle


EXPECTED_SEQUENCE = (
    ("press", "r"),
    ("sleep", 3),
    ("release", "r"),
    ("press", "w"),
    ("sleep", 3),
    ("release", "w"),
    ("press", "a"),
    ("sleep", 0.8),
    ("release", "a"),
    ("press", "w"),
    ("sleep", 2.25),
    ("release", "w"),
    ("press", "ctrl"),
    ("sleep", 0.1),
    ("release", "ctrl"),
    ("sleep", 2.5),
    ("press", "g"),
    ("sleep", 0.1),
    ("release", "g"),
    ("sleep", 0.8),
    ("press", "f"),
    ("sleep", 0.1),
    ("release", "f"),
    ("sleep", 0.1),
    ("press", "e"),
    ("sleep", 0.1),
    ("release", "e"),
    ("sleep", 2.5),
    ("press", "e"),
    ("sleep", 0.1),
    ("release", "e"),
    ("sleep", 7),
)


class FakeController:
    def __init__(self):
        self.events = []

    def press(self, key):
        self.events.append(("press", key))

    def release(self, key):
        self.events.append(("release", key))


class FakeKeyboardModule:
    class Key:
        ctrl = "ctrl"


class RuneFarmSequenceTest(unittest.TestCase):
    def test_declared_sequence_matches_original_script_order_and_durations(self):
        actual = []
        for action in RUNE_FARM_SEQUENCE:
            if isinstance(action, SleepAction):
                actual.append(("sleep", action.seconds))
            elif isinstance(action, KeyAction):
                actual.append((action.action, action.key))

        self.assertEqual(EXPECTED_SEQUENCE, tuple(actual))

    def test_run_rune_cycle_executes_sequence(self):
        controller = FakeController()
        events = controller.events

        def fake_sleep(seconds):
            events.append(("sleep", seconds))

        run_rune_cycle(controller, fake_sleep, keyboard_module=FakeKeyboardModule)

        self.assertEqual(EXPECTED_SEQUENCE, tuple(events))


if __name__ == "__main__":
    unittest.main()
