import ctypes
import time
import threading
from ctypes import wintypes

# Constants
USER32 = ctypes.windll.user32
CURSOR_SHOWING = 0x00000001

# Function prototypes
GetCursorPos = USER32.GetCursorPos
ShowCursor = USER32.ShowCursor
GetCursorInfo = USER32.GetCursorInfo


class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('flags', ctypes.c_uint),
        ('hCursor', ctypes.c_void_p),
        ('ptScreenPos', ctypes.wintypes.POINT),
    ]


def get_cursor_pos() -> tuple[int, int]:
    """Get the current position of the cursor."""
    pt = wintypes.POINT()
    GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def show_cursor(show: bool) -> int:
    """Show or hide the cursor based on the 'show' parameter"""
    return ShowCursor(show)


def is_cursor_showing() -> bool:
    """Check if the cursor is currently visible."""
    ci = CURSORINFO()
    ci.cbSize = ctypes.sizeof(CURSORINFO)
    GetCursorInfo(ctypes.byref(ci))
    return bool(ci.flags & CURSOR_SHOWING)


def hide_cursor_after_timeout(timeout: int = 3) -> None:
    """Hide the cursor after a specified timeout of inactivity."""
    last_pos = get_cursor_pos()
    cursor_hidden = False
    last_move_time = time.time()

    while True:
        time.sleep(0.1)
        current_pos = get_cursor_pos()

        if current_pos != last_pos:
            if cursor_hidden:
                show_cursor(True)
                cursor_hidden = False
            last_pos = current_pos
            last_move_time = time.time()

        elif not cursor_hidden and time.time() - last_move_time > timeout:
            show_cursor(False)
            cursor_hidden = True


def main() -> None:
    """Main function to start the cursor hiding utility."""
    cursor_thread = threading.Thread(target=hide_cursor_after_timeout, daemon=True)
    cursor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()