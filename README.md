# Windows Cursor Hiding Utility

This project provides a Python utility for automatically hiding the Windows cursor after a period of inactivity and restoring it upon mouse movement. It's designed for scenarios where you want the cursor to disappear when not in use, such as during presentations or in kiosk-mode applications.

## Features

- Automatically hides the cursor after a configurable period of inactivity
- Restores the cursor immediately upon mouse movement
- Works across multiple monitors with different resolutions
- Includes a test module to verify functionality

## Requirements

- Windows operating system
- Python 3.9+
- Administrator privileges (required for system-wide cursor manipulation)

## Installation

1. Clone this repository or download the source files:
   ```
   git clone https://github.com/PRich57/windows-cursor-hiding-utility.git
   cd windows-cursor-hiding-utility
   ```

2. No additional dependencies are required beyond the Python standard library.

## Usage

#### Main Script

To use the cursor hiding utility:

1. Open a command prompt with administrator privileges.
2. Navigate to the project directory.
3. Run the script:
   ```
   python hide_cursor.py
   ```
4. The script will run in the background, hiding the cursor after 3 seconds of inactivity (default) and showing it again when you move the mouse.
5. To stop the script, press `ctrl+c` in the command prompt.

#### Test Module

To test the functionality of the cursor hiding utility:

1. Ensure both `hide_cursor.py` and `test_hide_cursor.py` are in the same directory.
2. Open a command prompt with administrator privileges.
3. Navigate to the project directory.
4. Run the test script:
   ```
   python test_hide_cursor.py
   ```
5. Follow the on-screen instructions to perform the test.
6. After the test, answer the questions to confirm if the cursor behaved as expected.

## Customization

You can modify the inactivity timeout in the `hide_cursor.py` script. Look for the `hide_cursor_after_timeout` function call in the `main` function and adjust the `timeout` parameter as needed.

## Troubleshooting

- If the cursor doesn't hide or show properly, ensure you're running the script with administrator privileges.
- On multi-monitor setups, make sure to test the functionality on all screens.
- If issues persist, check the log output for any error messages or unexpected behavior.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the Windows API through Python's ctypes library to manipulate the system cursor.
- Special thanks to the Python community for their invaluable resources and documentation.