"""Elden Ring Mohgwyn Palace rune farming helper.

The automation cycle intentionally preserves the original key order and sleep
durations. Refactors should keep RUNE_FARM_SEQUENCE behavior-compatible.
"""

from __future__ import annotations

import sys
import threading
import time
from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Protocol, Union


HOTKEY = "<cmd>+n"
IDLE_POLL_INTERVAL_SECONDS = 0.1
TRAY_ICON_SIZE = 64


class KeyboardController(Protocol):
    def press(self, key: object) -> None:
        ...

    def release(self, key: object) -> None:
        ...


@dataclass(frozen=True)
class KeyAction:
    action: str
    key: str


@dataclass(frozen=True)
class SleepAction:
    seconds: float


RuneAction = Union[KeyAction, SleepAction]


RUNE_FARM_SEQUENCE: tuple[RuneAction, ...] = (
    # Eat the golden fowl foot / horn tender from the first item slot.
    KeyAction("press", "r"),
    SleepAction(3),
    KeyAction("release", "r"),
    # Move into position.
    KeyAction("press", "w"),
    SleepAction(3),
    KeyAction("release", "w"),
    KeyAction("press", "a"),
    SleepAction(0.8),
    KeyAction("release", "a"),
    KeyAction("press", "w"),
    SleepAction(2.25),
    KeyAction("release", "w"),
    # Wave of Gold.
    KeyAction("press", "ctrl"),
    SleepAction(0.1),
    KeyAction("release", "ctrl"),
    SleepAction(2.5),
    # Fast travel back to the grace.
    KeyAction("press", "g"),
    SleepAction(0.1),
    KeyAction("release", "g"),
    SleepAction(0.8),
    KeyAction("press", "f"),
    SleepAction(0.1),
    KeyAction("release", "f"),
    SleepAction(0.1),
    KeyAction("press", "e"),
    SleepAction(0.1),
    KeyAction("release", "e"),
    SleepAction(2.5),
    KeyAction("press", "e"),
    SleepAction(0.1),
    KeyAction("release", "e"),
    # Loading screen.
    SleepAction(7),
)


def resolve_key(key_name: str, keyboard_module: Optional[object] = None) -> object:
    """Resolve abstract key names to pynput keys when needed."""
    if key_name == "ctrl":
        if keyboard_module is None:
            from pynput import keyboard as keyboard_module

        return keyboard_module.Key.ctrl
    return key_name


def run_rune_cycle(
    controller: KeyboardController,
    sleep: Callable[[float], None] = time.sleep,
    sequence: Iterable[RuneAction] = RUNE_FARM_SEQUENCE,
    keyboard_module: Optional[object] = None,
) -> None:
    """Run one complete rune farming cycle."""
    for action in sequence:
        if isinstance(action, SleepAction):
            sleep(action.seconds)
            continue

        key = resolve_key(action.key, keyboard_module)
        if action.action == "press":
            controller.press(key)
        elif action.action == "release":
            controller.release(key)
        else:
            raise ValueError(f"Unsupported key action: {action.action}")


class RuneMakerApp:
    def __init__(self, controller: KeyboardController, sleep: Callable[[float], None] = time.sleep):
        self._controller = controller
        self._sleep = sleep
        self._running = False
        self._lock = threading.Lock()
        self._stop_requested = threading.Event()

    def toggle_running(self) -> None:
        with self._lock:
            self._running = not self._running
            print("Started" if self._running else "Stopped", flush=True)

    def stop(self) -> None:
        with self._lock:
            self._running = False
        self._stop_requested.set()

    def is_running(self) -> bool:
        with self._lock:
            return self._running

    def wait_for_stop(self, timeout: float) -> bool:
        return self._stop_requested.wait(timeout)

    def run_worker(self) -> None:
        while not self._stop_requested.is_set():
            if self.is_running():
                run_rune_cycle(self._controller, self._sleep)
            else:
                self._stop_requested.wait(IDLE_POLL_INTERVAL_SECONDS)


def create_tray_image():
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (TRAY_ICON_SIZE, TRAY_ICON_SIZE), "#141414")
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 54, 54), outline="#d6b25e", width=3)
    draw.text((22, 22), "ER", fill="#d6b25e")
    return image


def setup_tray_icon(app: RuneMakerApp):
    import pystray

    def on_toggle(icon, item):
        app.toggle_running()

    def on_exit(icon, item):
        app.stop()
        icon.stop()

    icon = pystray.Icon(
        "EldenRingRuneMaker",
        create_tray_image(),
        menu=pystray.Menu(
            pystray.MenuItem("Start / Stop", on_toggle),
            pystray.MenuItem("Exit", on_exit),
        ),
    )
    return icon


def run_hotkey_listener(app: RuneMakerApp) -> None:
    from pynput import keyboard

    with keyboard.GlobalHotKeys({HOTKEY: app.toggle_running}) as listener:
        while not app.wait_for_stop(IDLE_POLL_INTERVAL_SECONDS):
            pass
        listener.stop()


def main() -> int:
    try:
        from pynput import keyboard
    except ImportError as exc:
        print(f"Missing dependency: {exc.name}. Install dependencies with `pip install -r requirements.txt`.")
        return 1

    app = RuneMakerApp(keyboard.Controller())
    worker = threading.Thread(target=app.run_worker, name="rune-worker", daemon=True)
    worker.start()

    tray_thread: Optional[threading.Thread] = None
    try:
        tray_icon = setup_tray_icon(app)
        tray_thread = threading.Thread(target=tray_icon.run, name="tray-icon", daemon=True)
        tray_thread.start()
    except ImportError as exc:
        print(f"Tray icon disabled, missing dependency: {exc.name}.")

    print("Press Win+N to start/stop the loop", flush=True)
    try:
        run_hotkey_listener(app)
    except KeyboardInterrupt:
        app.stop()
    finally:
        app.stop()
        worker.join(timeout=1)
        if tray_thread is not None:
            tray_thread.join(timeout=1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
