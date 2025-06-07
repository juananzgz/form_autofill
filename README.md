# Form Filler Bot

This project consists of two main components:
1.  A Linux shell script (`get_coords.sh`) to capture screen coordinates for form fields and buttons.
2.  A Python application (`form_filler.py`) that reads data from a CSV file and uses the captured coordinates to automatically fill and submit web forms or other GUI applications.

## Features

-   **Coordinate Capturing:** Interactively capture X,Y coordinates for any element on your screen.
-   **CSV Data Input:** Reads data from a CSV file, with the first row expected to be headers.
-   **Automated Form Filling:** Uses `pyautogui` to simulate mouse movements, clicks, and typing.
-   **Configurable Delays:** Allows adjustment of delays between actions to suit different system speeds and application responsiveness.
-   **Command-line Interface:** Both scripts are run from the command line.

## Prerequisites

-   **Linux Environment:** The `get_coords.sh` script is designed for Linux.
-   **xdotool:** Required by `get_coords.sh` for capturing mouse coordinates.
    -   Installation (Debian/Ubuntu): `sudo apt update && sudo apt install xdotool`
-   **Python 3:** Required to run `form_filler.py`.
-   **pip (Python package installer):** Usually comes with Python 3.
-   **Python Libraries:**
    -   `pyautogui`: For GUI automation.
    -   The `csv` module used is part of the Python standard library.

    Install Python libraries using pip:
    ```bash
    pip install pyautogui
    ```
    *(Note: `pyautogui` might have other system-level dependencies depending on your Linux distribution for interacting with the display server, e.g., `scrot`, `python3-tk`, `python3-dev`. The `form_filler.py` script will mention these if an `ImportError` for `pyautogui` occurs. If `pyautogui` fails during execution, check its documentation for specific OS dependencies like those needed for X11/Wayland.)*

## Setup and Usage

### 1. Capture Coordinates (`get_coords.sh`)

This script helps you create a `coords.txt` file. Each entry in this file defines a named screen position (X,Y coordinate). These names and coordinates drive the automation:

-   **For Data Entry:** If a name you define in `coords.txt` **matches a header in your CSV file**, the script will type the corresponding data from the CSV into the field at these coordinates.
-   **For Click-Only Actions:** If a name in `coords.txt` **does not match any header in your CSV file**, the script will simply perform a click at these coordinates.
-   **Order Matters:** The sequence of these click-only actions is determined by their order in `coords.txt`. Data entry fields are processed first (matching CSV header order), followed by all click-only actions in their defined sequence.

a.  **Make the script executable:**
    ```bash
    chmod +x get_coords.sh
    ```

b.  **Run the script:**
    ```bash
    ./get_coords.sh
    ```

c.  **Follow the on-screen prompts:**
    -   The script will ask you to enter a name for each coordinate (e.g., `username`, `email_field`, `submit_button`).
    -   After entering a name, you will have 5 seconds to move your mouse cursor to the desired location on the screen.
    -   The script will capture the X and Y coordinates and save them with the name you provided to `coords.txt`.
    -   Enter `done` when you have captured all necessary coordinates.

    **Example `coords.txt`:**
    ```
    username:850,350       # Matches CSV header 'username', will type data
    password:850,400       # Matches CSV header 'password', will type data
    terms_checkbox:800,450 # Does not match any CSV header, will be clicked
    login_button:900,520   # Does not match any CSV header, will be clicked after 'terms_checkbox'
    ```
    **Important:**
    - Names intended for data entry **must exactly match** the corresponding headers in your CSV file.
    - Names for click-only actions can be anything descriptive.
    - The order of click-only actions in this file dictates their execution order.

### 2. Prepare Your CSV Data File

Create a CSV file (e.g., `data.csv`) where:
-   The first row contains headers, and fields **must be separated by semicolons (;)**. These headers **must match the names** you assigned to the coordinates in `coords.txt` (e.g., if you used `firstname` in `coords.txt`, your CSV should have a `firstname` column).
-   Subsequent rows contain the data to be filled into the form, also using semicolons as delimiters.
-   *Note: The semicolon delimiter is used to avoid conflicts with data that might contain commas (e.g., decimal numbers in some European formats or free text fields).*

**Example `data.csv`:**
```csv
firstname;lastname;email
John;Doe;john.doe@example.com
Jane;Smith;jane.smith@example.com
```

### 3. Run the Form Filler (`form_filler.py`)

This Python script reads your `coords.txt` and your CSV file, then automates the form filling process.

a.  **Open the target application/web page** that you want to fill.

b.  **Run the script from your terminal:**
    ```bash
    python3 form_filler.py your_data.csv
    ```
    -   Replace `your_data.csv` with the path to your CSV file.
    -   You can also use optional arguments like `--coords-file` and `--delay`.

c.  **Switch to the target application window quickly!** The script has a short delay (3 seconds by default after starting) before it begins controlling your mouse and keyboard.

**Command-line Arguments for `form_filler.py`:**
-   `csv_file`: (Required) Path to your CSV data file.
-   `--coords-file COORDS_FILE` or `--coords_file COORDS_FILE`: (Optional) Path to your coordinates file. Defaults to `coords.txt` in the same directory.
-   `--delay DELAY`: (Optional) General delay in seconds between most GUI actions. Default is `0.5`.

**Example Usage:**
```bash
python3 form_filler.py data.csv --coords-file my_custom_coords.txt --delay 0.7
```
*(Note: The script `form_filler.py` uses `argparse`, which typically allows both `-` and `_` in argument names, e.g. `--coords-file` and `--coords_file` should both work.)*

## How It Works

1.  `get_coords.sh` uses `xdotool getmouselocation --shell` to find out where your mouse is pointing after a timed delay. It stores these named coordinates in the order you define them.
2.  `form_filler.py` parses the coordinate file (e.g., `coords.txt`) and the CSV data file. It identifies which coordinate names from `coords.txt` match headers in the CSV file.
3.  For each row in the CSV:
    -   **Data Entry:** The script iterates through the CSV headers. If a CSV header matches a name defined in `coords.txt`, it moves the mouse to the corresponding (X,Y) position, clicks, and types the data from the current CSV row's cell for that header. The `--delay` argument applies after each typing action.
    -   **Click-Only Actions:** After processing all CSV headers for the current row, the script then processes any "click-only" actions. These are coordinates defined in `coords.txt` whose names *did not* match any CSV header. These actions are performed in the sequence they appeared in `coords.txt`.
        -   A **1-second hardcoded delay** occurs *between each* of these sequential click-only actions. This is independent of the `--delay` argument.
    -   The general `--delay` is applied once more after all actions (typing and clicking) for the current row are complete, before moving to the next row.

## Troubleshooting

-   **Incorrect Coordinates:** If the mouse isn't clicking the right places, re-run `get_coords.sh` carefully. Ensure your application window doesn't move or resize between capturing coordinates and running the filler.
-   **`pyautogui` Issues:**
    -   **FailSafeException:** If `pyautogui` throws a `FailSafeException`, it means you moved your mouse to a corner of the screen (usually top-left) as a security measure to stop the script. The script is designed to catch this and exit gracefully.
    -   **Permissions/Display Server:** On some Linux systems, `pyautogui` might need additional permissions or specific configurations to control the mouse and keyboard. This is especially true under Wayland (try running in an X11 session if issues persist). Refer to `pyautogui` documentation and the installation notes in `form_filler.py`.
    -   **Module Not Found:** Ensure `pyautogui` is installed in the Python environment you are using. (`pip install pyautogui`).
-   **Timing Issues:** If the script is too fast or too slow for your target application, adjust the `--delay` option in `form_filler.py`. Some applications need more time to process inputs or load new sections.
-   **Window Focus:** Ensure the target application window is active and focused before `form_filler.py` starts its automation sequence. The script includes a brief pause at the beginning for this. If the wrong window is active, the script will interact with that window instead.
-   **`xdotool` not found/not working:** Ensure `xdotool` is installed correctly and working from your terminal. If `get_coords.sh` reports errors capturing coordinates, this is the likely cause.

## License
This project is licensed under the MIT License. You can create a `LICENSE` file and paste the MIT License text into it if you wish.
(A basic MIT License template can be found at https://opensource.org/licenses/MIT)
