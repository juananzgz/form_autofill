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
    email_field:100,200     # If 'email_field' is in CSV, types data. Else, clicks.
    company_name:100,250  # If 'company_name' is in CSV, types data. Else, clicks.
    next_step_button:50,300 # Likely not in CSV, so this will be a click.
    age_field:100,350       # If 'age_field' is in CSV, types data. Else, clicks.
    final_submit:100,400    # Likely not in CSV, so this will be a click.
    ```
    **Important:**
    - For each entry in `coords.txt`, its `name` is checked against the headers of the current CSV row.
    - If the `name` matches a CSV header, the script types the data from that CSV field.
    - If the `name` does not match any CSV header for the current row, the script performs a click.
    - This process is repeated sequentially for every entry in `coords.txt`.

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

1.  **Coordinate Scripting (`get_coords.sh` & `coords.txt`):**
    -   `get_coords.sh` helps you create `coords.txt`.
    -   `coords.txt` acts as an **ordered script of actions**. Each line defines a named coordinate (`action_name:X,Y`). The sequence of these lines is critical.

2.  **Python Automation (`form_filler.py`):**
    -   The script loads `coords.txt` (preserving the order of actions) and the input CSV file.
    -   It then iterates through each **row** of your CSV data. For each CSV row, it performs the following:
        -   It iterates through each `action_name` in your `coords.txt` **in the exact order defined**.
        -   For the current `action_name` and its (X,Y) coordinates:
            -   **Check against CSV row:** The script checks if `action_name` exists as a key/header in the current CSV row's data.
            -   **If `action_name` IS in the CSV row (Data Entry):**
                1.  The mouse moves to (X,Y) and clicks.
                2.  A brief pause occurs (`args.delay / 2`).
                3.  The script types the value from `row[action_name]`.
                4.  A configurable delay (`args.delay`) occurs after typing this field.
            -   **If `action_name` IS NOT in the CSV row (Click-Only Action):**
                1.  The mouse moves to (X,Y) and clicks.
                2.  A **fixed 1-second delay** occurs immediately after this click.
        -   This sequence (iterate through `coords.txt` entries, perform action) is completed for all actions defined in `coords.txt` before the script moves to the next row in the CSV file.

3.  **Delays Summary:**
    -   **Typing Action:** `args.delay / 2` (before typing) + `args.delay` (after typing).
    -   **Click-Only Action:** Fixed 1-second delay after the click.
    -   **End of CSV Row:** After all actions from `coords.txt` are performed for a CSV row, a longer delay of `args.delay * 2` occurs before processing the next CSV row. This gives time for the UI to update (e.g., page loads).

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
