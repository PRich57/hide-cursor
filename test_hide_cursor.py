import time
import logging
from hide_cursor import hide_cursor, show_cursor, get_cursor_pos

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_cursor_toggle() -> None:
    """
    Test the cursor hiding and showing functionality.
    """
    logger.info("Starting cursor visibility test")
    
    initial_pos = get_cursor_pos()
    logger.info(f"Initial cursor position: {initial_pos}")
    
    logger.info("Hiding cursor")
    hide_cursor()
    logger.info("Cursor should be hidden now. Is it? (Move your mouse to check)")
    time.sleep(3)
    
    logger.info("Showing cursor")
    show_cursor()
    logger.info("Cursor should be visible now. Is it?")
    
    final_pos = get_cursor_pos()
    logger.info(f"Final cursor position: {final_pos}")


def main() -> None:
    """
    Main function to run the cursor hiding test.
    """
    print("This script will test hiding the cursor for 3 seconds, then show it again.")
    print("Press Enter to start the test...")
    input()
    
    try:
        test_cursor_toggle()
    except Exception as e:
        logger.error(f"An error occurred during the test: {e}")
    
    print("\nTest complete. Please answer the following questions:")
    print("1. Did the cursor disappear for about 3 seconds?")
    print("2. Did the cursor reappear after that?")
    print("3. Check the logged cursor positions. Did they change?")
    print("   (If they changed, it confirms that get_cursor_pos() is working)")


if __name__ == "__main__":
    main()