from enum import Enum
from threading import Thread
import tkinter as tk
from queue import Empty, Queue

import screeninfo

CHECK_QUEUE_INTERVAL_MS = 100

POPUP_MONITOR_SIZE_RATIO = 0.8
FOREGROUND_COLOR = "#990011"
BACKGROUND_COLOR = "#fcf6f5"


def _get_primary_monitor_resolution() -> tuple[int, int]:
    monitors = screeninfo.get_monitors()

    if not monitors:
        return -1, -1

    for monitor in monitors:
        if monitor.is_primary:
            return monitor.width, monitor.height


class Popup(tk.Toplevel):
    def __init__(self, master: tk.Tk, text: str, width: int, height: int, x: int, y: int, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(
            self,
            text=text,
            font=("Helvetica", 24),
            wraplength=width * 0.9,
            bg=self["bg"],
            fg=FOREGROUND_COLOR
        )
        label.place(relx=0.5, rely=0.5, anchor="center")


class Operation(Enum):
    DESTROY_POPUP = 0
    CREATE_POPUP = 1


class GUIThread(Thread):
    def __init__(self, queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = queue
        self.popup = None

    def run(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after_idle(self.check_queue)
        self.root.mainloop()

    def create_unclosable_popup(self, text: str) -> None:
        if self.popup is not None:
            self.destroy_popup()

        monitor_width, monitor_height = _get_primary_monitor_resolution()
        width = int(monitor_width * POPUP_MONITOR_SIZE_RATIO)
        height = int(monitor_height * POPUP_MONITOR_SIZE_RATIO)
        x = monitor_width // 2 - width // 2
        y = monitor_height // 2 - height // 2

        self.popup = Popup(self.root, text, width, height, x, y, bg=BACKGROUND_COLOR)

        self.popup.overrideredirect(True)
        self.popup.attributes('-topmost', True)

    def destroy_popup(self) -> None:
        self.popup = self.popup.destroy()

    def process_operation(self, operation: str, *args, **kwargs):
        match operation:
            case Operation.CREATE_POPUP:
                self.create_unclosable_popup(*args, **kwargs)
            case Operation.DESTROY_POPUP:
                self.destroy_popup()
            case _:
                raise Exception("An unknown message was sent in the message queue")

    def check_queue(self):
        try:
            operation, args, kwargs = self.queue.get_nowait()
            self.process_operation(operation, *args, **kwargs)
        except Empty:
            pass

        self.root.after(CHECK_QUEUE_INTERVAL_MS, self.check_queue)
