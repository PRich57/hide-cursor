import ctypes
import time

user32 = ctypes.windll.user32

def toggle_cursor():
    user32.ShowCursor(False)
    print("Cursor should be hidden now. Is it?")
    time.sleep(3)
    user32.ShowCursor(True)
    print("Cursor should be visible now. Is it?")

if __name__ == "__main__":
    print("This script will hide the cursor for 3 seconds, then show it again.")
    print("Press Enter to start the test...")
    input()
    toggle_cursor()
    print("Test complete. Did the cursor hide and then reappear?")