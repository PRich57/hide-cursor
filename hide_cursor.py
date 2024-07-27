import ctypes
import logging
import threading
import time
from ctypes import wintypes


# Constants
OCR_NORMAL = 32512
SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load required DLLs
user32 = ctypes.windll.user32

# Function prototypes
user32.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
user32.SetSystemCursor.argtypes = [ctypes.c_void_p, ctypes.c_uint]
user32.SetSystemCursor.restype = ctypes.c_bool
user32.CopyIcon.argtypes = [ctypes.c_void_p]
user32.CopyIcon.restype = ctypes.c_void_p
user32.LoadCursorW.argtypes = [ctypes.c_void_p, ctypes.c_int]
user32.LoadCursorW.restype = ctypes.c_void_p
user32.SystemParametersInfoW.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
user32.SystemParametersInfoW.restype = ctypes.c_bool


def get_cursor_pos() -> tuple[int, int]:
    """
    Get the current position of the cursor.

    Returns:
        A tuple containing the x and y coordinates of the cursor.
    """
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def create_invisible_cursor() -> ctypes.c_void_p:
    """
    Create an invisible cursor.

    Returns:
        A handle to the created invisible cursor.
    """
    and_mask = (ctypes.c_ubyte * 4)(0xFF, 0xFF, 0xFF, 0xFF)
    xor_mask = (ctypes.c_ubyte * 4)(0, 0, 0, 0)
    return user32.CreateCursor(None, 0, 0, 1, 1, and_mask, xor_mask)


original_cursor = None


def hide_cursor() -> None:
    """
    Hide the cursor by replacing it with an invisible one.
    """
    global original_cursor
    invisible_cursor = create_invisible_cursor()
    original_cursor = user32.CopyIcon(user32.LoadCursorW(None, OCR_NORMAL))
    if user32.SetSystemCursor(invisible_cursor, OCR_NORMAL):
        logger.debug("Cursor hidden")
    else:
        logger.error("Failed to hide cursor")


def show_cursor() -> None:
    """
    Restore the original cursor.
    """
    global original_cursor
    if original_cursor:
        if user32.SetSystemCursor(original_cursor, OCR_NORMAL):
            logger.debug("Cursor restored")
            # Force a cursor update across all monitors
            user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        else:
            logger.error("Failed to restore cursor")
    else:
        logger.error("No original cursor to restore")


def hide_cursor_after_timeout(timeout: int = 3) -> None:
    """
    Hide the cursor after a specified timeout of inactivity.

    Args:
        timeout: Number of seconds of inactivity before hiding the cursor.
    """
    last_pos = get_cursor_pos()
    last_move_time = time.time()
    cursor_hidden = False

    logger.debug("Starting cursor hide thread")

    while True:
        time.sleep(0.1)
        current_pos = get_cursor_pos()

        if current_pos != last_pos:
            last_pos = current_pos
            last_move_time = time.time()
            if cursor_hidden:
                show_cursor()
                cursor_hidden = False
            logger.debug(f"Cursor moved to {current_pos}")
        elif not cursor_hidden and time.time() - last_move_time > timeout:
            hide_cursor()
            cursor_hidden = True


def main() -> None:
    """
    Main function to start the cursor hiding utility.

    This function sets up a daemon thread to handle cursor hiding and runs
    indefinitely until interrupted by the user.
    """
    cursor_thread = threading.Thread(target=hide_cursor_after_timeout, daemon=True)
    cursor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.debug("Script terminated by user")
    finally:
        # Ensure cursor is shown when the script exits
        show_cursor()
        logger.debug("Cursor shown on exit")


if __name__ == "__main__":
    main()