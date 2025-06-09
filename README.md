# Form Filler Bot

This project consists of two main components:

1.  A Linux shell script (`get_coords.sh`) or Python app (`get_coords_py.py`) to capture screen coordinates for form fields and buttons.

2.  A Python application (`form_filler.py`) that reads data from a CSV file and uses the captured coordinates to automatically fill and submit web forms or other GUI applications.

## Features


-   **Coordinate Capturing:** Interactively capture X,Y coordinates using Python (`get_coords_py.py`) or a shell script on Linux (`get_coords.sh`).
-   **CSV Data Input:** Reads data from a CSV file (semicolon-delimited), with the first row expected to be headers.
-   **Automated Form Filling:** Uses `pyautogui` to simulate mouse movements, clicks, and typing.
-   **Configurable Delays:** Allows adjustment of delays between actions to suit different system speeds and application responsiveness.
-   **Command-line Interface:** All scripts are run from the command line.
-   **Cross-Platform (Python components):** `get_coords_py.py` and `form_filler.py` are written in Python and should work on Windows, macOS, and Linux, provided Python and `pyautogui` are set up correctly.

## Prerequisites

**Core Requirements (for `get_coords_py.py` and `form_filler.py`):**
-   **Python 3:**
    -   **Windows:** Download from `https://www.python.org/downloads/`. Ensure "Add Python to PATH" is checked during installation.
    -   **Linux/macOS:** Python 3 is often pre-installed. If not, use your system's package manager (e.g., `sudo apt install python3` on Debian/Ubuntu, or `brew install python` on macOS).
-   **pip (Python package installer):** Usually comes with Python 3. If not, search for "install pip" for your OS.
-   **`pyautogui` Python library:** For GUI automation. Install via pip:
    ```bash
    pip install pyautogui
    ```
    *   **Important Note for `pyautogui`:** This library may have additional system dependencies for interacting with the display server, especially on Linux (e.g., `scrot`, `python3-tk`, `python3-dev`, `xclip`/`xsel`). If `pyautogui` import fails or doesn't work correctly (e.g., mouse control issues), please consult its official installation guide for your OS: `https://pyautogui.readthedocs.io/en/latest/install.html`

**For Linux-Specific Shell Script (`get_coords.sh` only):**
-   **Linux Environment.**
-   **xdotool:** Required by `get_coords.sh` for capturing mouse coordinates.
    -   Installation (Debian/Ubuntu): `sudo apt update && sudo apt install xdotool`

## Setup and General Usage Workflow

The general workflow involves two main steps:
1.  **Capture Coordinates:** Use one of the provided scripts to get the X,Y positions of UI elements.
2.  **Automate Filling:** Use `form_filler.py` with your captured coordinates and CSV data.

### 1. Capture Coordinates

You have two options for capturing coordinates. The Python-based script is recommended for cross-platform compatibility.

**a. Using `get_coords_py.py` (Recommended for Windows, macOS, Linux)**

This Python script interactively captures mouse coordinates and saves them to `coords.txt`.

-   **Run the script:**
    ```bash
    # Ensure Python is installed and in your PATH
    python get_coords_py.py
    ```
    (On some systems, you might need to use `python3` explicitly: `python3 get_coords_py.py`)

-   **Follow on-screen prompts:**
    -   It will ask if you want to overwrite or append to an existing `coords.txt`.
    -   Enter a name for each coordinate (e.g., `username_field`, `submit_button`). This name will be used in `coords.txt`.
    -   After entering a name, you'll have a 5-second countdown to position your mouse over the target UI element.
    -   The script uses `pyautogui.position()` to get the coordinates.
    -   Type `done` when finished.

**b. Linux-Specific: Using `get_coords.sh`**

This shell script is an alternative for Linux users who have `xdotool` installed.

-   **Make the script executable (if you haven't already):**
    ```bash
    chmod +x get_coords.sh
    ```
-   **Run the script:**
    ```bash
    ./get_coords.sh
    ```
-   **Follow on-screen prompts:**
    -   Enter a name for each coordinate.
    -   After entering a name, you will have 5 seconds to move your mouse cursor to the desired location.
    -   The script uses `xdotool` to capture coordinates.
    -   Enter `done` when finished.

**`coords.txt` File Details:**

Both scripts generate a `coords.txt` file (or append to it). This file acts as an **ordered script of actions** to be performed by `form_filler.py` for each row in your CSV file.

-   **For Data Entry:** If a name you define in `coords.txt` **matches a header in your CSV file**, the script will type the corresponding data from the CSV into the field at these coordinates.
-   **For Click-Only Actions:** If a name in `coords.txt` **does not match any header in your CSV file**, the script will simply perform a click at these coordinates.
-   **Order is Paramount:** The `coords.txt` file now defines an **exact script of operations** to be performed for each row in your CSV file. Actions (typing or clicking) are executed in the precise order they appear in `coords.txt`.

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

    email_field:100,200     # If 'email_field' is in CSV for the current row, types data. Else, clicks.
    company_name:100,250  # If 'company_name' is in CSV for the current row, types data. Else, clicks.
    next_step_button:50,300 # Likely not a CSV header, so this will usually be a click.
    age_field:100,350       # If 'age_field' is in CSV for the current row, types data. Else, clicks.
    final_submit:100,400    # Likely not a CSV header, so this will usually be a click.
    ```
    **Key points for `coords.txt`:**
    - For each entry in `coords.txt`, its `action_name` is checked against the keys/headers of the current CSV row.
    - If `action_name` matches a CSV header, the script types the data from that CSV field at the (X,Y) position.
    - If `action_name` does not match any CSV header for the current row, the script performs a click at (X,Y).
    - This process is repeated sequentially for every entry in `coords.txt`, for each row in the CSV. The order in `coords.txt` is strictly followed.


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

    # For Windows (assuming Python is in PATH)
    python form_filler.py your_data.csv

    # For Linux/macOS (use python3 if python is Python 2)
    python3 form_filler.py your_data.csv
    # Or if python is already Python 3:
    # python form_filler.py your_data.csv

    ```
    -   Replace `your_data.csv` with the path to your CSV file.
    -   You can also use optional arguments like `--coords-file` and `--delay`.

c.  **Switch to the target application window quickly!** The script has a short delay (3 seconds by default after starting) before it begins controlling your mouse and keyboard.

**Command-line Arguments for `form_filler.py`:**
-   `csv_file`: (Required) Path to your CSV data file.

-   `--coords-file COORDS_FILE` (or `--coords_file`): (Optional) Path to your coordinates file. Defaults to `coords.txt`.
-   `--delay DELAY`: (Optional) General delay in seconds between most GUI actions. Default is `0.5`.

**Example Usage (cross-platform):**
```bash
python form_filler.py data.csv --coords-file my_custom_coords.txt --delay 0.7
```
*(Note: `argparse` typically allows both `-` and `_` in argument names, e.g. `--coords-file` and `--coords_file`.)*

## How It Works

1.  **Coordinate Scripting (using `get_coords_py.py` or `get_coords.sh`):**
    -   You create `coords.txt`. This file acts as an **ordered script of actions**. Each line defines a named coordinate (`action_name:X,Y`). The sequence of these lines is critical.

2.  **Python Automation (`form_filler.py`):**
    -   The script loads `coords.txt` (preserving the order of `action_name` entries) and the input CSV file (semicolon-delimited).
    -   It then iterates through each **row** of your CSV data. For each CSV row, it performs the following sequence of operations:
        -   It iterates through each `action_name` from your loaded `coords.txt` **in the exact order they were defined**.
        -   For the current `action_name` and its corresponding (X,Y) coordinates:
            -   **Check against current CSV row's data:** The script checks if `action_name` exists as a key (header) in the dictionary representing the current CSV row.
            -   **If `action_name` IS a key in the current CSV row (Data Entry Action):**
                1.  The mouse moves to the (X,Y) coordinate.
                2.  A click is performed.
                3.  A brief pause occurs (`args.delay / 2`).
                4.  The script types the value associated with `action_name` from the current CSV row (e.g., `row[action_name]`).
                5.  A configurable delay (`args.delay`) occurs after completing the typing for this field.
            -   **If `action_name` IS NOT a key in the current CSV row (Click-Only Action):**
                1.  The mouse moves to the (X,Y) coordinate.
                2.  A click is performed.
                3.  A **fixed 1-second delay** occurs immediately after this click. This delay is not affected by the `--delay` argument.
        -   This entire sequence (iterating through all `action_name` entries from `coords.txt` and performing the corresponding action) is completed for the current CSV row before the script proceeds to the next row in the CSV file.

3.  **Delays Summary (controlled by `form_filler.py`):**
    -   **Before Typing (Data Entry):** `args.delay / 2`.
    -   **After Typing (Data Entry):** `args.delay`.
    -   **After Click-Only Action:** Fixed 1-second delay.
    -   **End of each CSV Row Processing:** After all actions defined in `coords.txt` are performed for a single CSV row, a longer delay of `args.delay * 2` occurs. This is intended to give the UI time to react (e.g., process submissions, load new pages) before the next row's automation begins.


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
