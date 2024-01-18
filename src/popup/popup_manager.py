from queue import Queue

from .gui import GUIThread, Operation


class PopupManager:
    def __init__(self) -> None:
        self.queue = Queue(1)
        self.popup_exists = False

        td_gui = GUIThread(self.queue, daemon=True)
        td_gui.start()

    def create_unclosable(self, text: str) -> None:
        self.queue.put((Operation.CREATE_POPUP, tuple(), {"text": text}))
        self.popup_exists = True

    def destroy_popup(self) -> None:
        self.queue.put((Operation.DESTROY_POPUP, tuple(), dict()))
        self.popup_exists = False
