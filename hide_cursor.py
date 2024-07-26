import ctypes
import ctypes.wintypes
import time
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants and structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# Load required DLLs
user32 = ctypes.windll.user32

# Function prototypes
user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.SetSystemCursor.argtypes = [ctypes.c_void_p, ctypes.c_uint]

# Constants
OCR_NORMAL = 32512
SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

def get_cursor_pos():
    """Get the current position of the cursor."""
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return (pt.x, pt.y)

def create_invisible_cursor():
    """Create an invisible cursor."""
    # Create a 1x1 pixel black cursor
    cursor = user32.CreateCursor(None, 0, 0, 1, 1, bytes([0]), bytes([0]))
    return cursor

def set_system_cursor(cursor, cursor_id=OCR_NORMAL):
    """Set the system cursor to the specified cursor."""
    user32.SetSystemCursor(cursor, cursor_id)

def restore_system_cursors():
    """Restore the system cursors to their default appearance."""
    user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

def hide_cursor_after_timeout(timeout=3):
    """Hide the cursor after a specified timeout of inactivity."""
    last_pos = get_cursor_pos()
    last_move_time = time.time()
    cursor_hidden = False
    invisible_cursor = create_invisible_cursor()

    logging.debug("Starting cursor hide thread")

    while True:
        time.sleep(0.1)
        current_pos = get_cursor_pos()

        if current_pos != last_pos:
            if cursor_hidden:
                restore_system_cursors()
                logging.debug("Cursor shown")
                cursor_hidden = False
            last_pos = current_pos
            last_move_time = time.time()
            logging.debug(f"Cursor moved to {current_pos}")
        elif not cursor_hidden and time.time() - last_move_time > timeout:
            set_system_cursor(invisible_cursor)
            logging.debug("Cursor hidden")
            cursor_hidden = True

def main():
    """Main function to start the cursor hiding utility."""
    cursor_thread = threading.Thread(target=hide_cursor_after_timeout, daemon=True)
    cursor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.debug("Script terminated by user")
    finally:
        restore_system_cursors()
        logging.debug("System cursors restored")

if __name__ == "__main__":
    main()