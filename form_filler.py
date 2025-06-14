# form_filler.py
# This script automates filling web forms using coordinates and CSV data.
#
# Installation for pyautogui (if not installed):
# pip install pyautogui
#
# On Linux, you might also need to install scrot for screenshots (used by pyautogui internally sometimes)
# and xclip or xsel for copy/paste functionality:
# sudo apt-get install scrot python3-tk python3-dev
# sudo apt-get install xclip # or xsel

import csv
import argparse
import time
import os

try:
    import pyautogui
except ImportError:
    print("Error: pyautogui library is not installed.")
    print("Please install it by running: pip install pyautogui")
    print("On Linux, you may also need: sudo apt-get install scrot python3-tk python3-dev xclip")
    exit(1)

def parse_coordinates(coords_filepath: str) -> tuple[dict, list]:
    """
    Parses a coordinates file (e.g., coords.txt) into a dictionary
    and a list of names in their original order.

    Args:
        coords_filepath: Path to the coordinates file.
                         Each line should be in the format: name:X,Y

    Returns:
        A tuple containing:
        - coordinates_map: A dictionary mapping names to (X, Y) integer tuples.
                           Example: {'username_field': (150, 300), 'submit_button': (200, 400)}
        - ordered_coord_names: A list of names in the order they appeared in the file.
                               Example: ['username_field', 'submit_button']

    Raises:
        FileNotFoundError: If the coordinates file does not exist.
    """
    if not os.path.exists(coords_filepath):
        raise FileNotFoundError(f"Error: Coordinates file not found at '{coords_filepath}'")

    coordinates_map = {}
    ordered_coord_names = []
    try:
        with open(coords_filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines or comments
                    continue
                parts = line.split(':', 1)
                if len(parts) != 2:
                    print(f"Warning: Skipping malformed line {line_num} in '{coords_filepath}': '{line}' - missing ':' separator.")
                    continue
                name = parts[0].strip()
                coords_str = parts[1].strip()
                try:
                    x_str, y_str = coords_str.split(',')
                    x = int(x_str.strip())
                    y = int(y_str.strip())
                    coordinates_map[name] = (x, y)
                    ordered_coord_names.append(name)
                except ValueError:
                    print(f"Warning: Skipping malformed coordinate format on line {line_num} in '{coords_filepath}': '{line}'")
    except Exception as e:
        print(f"Error reading or parsing coordinates file '{coords_filepath}': {e}")
        # Potentially re-raise or return empty dict/list depending on desired strictness
        return {}, [] # Return empty map and list on error
    return coordinates_map, ordered_coord_names

def read_csv_data(csv_filepath: str) -> list:
    """
    Reads data from a CSV file into a list of dictionaries.

    Args:
        csv_filepath: Path to the CSV file.
                      The first row is assumed to be headers.

    Returns:
        A list of dictionaries, where each dictionary represents a row
        (header: value).

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    if not os.path.exists(csv_filepath):
        raise FileNotFoundError(f"Error: CSV file not found at '{csv_filepath}'")

    data_rows = []
    try:
        with open(csv_filepath, mode='r', encoding='utf-8-sig') as csvfile: # utf-8-sig handles BOM
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                data_rows.append(row)
    except Exception as e:
        print(f"Error reading CSV file '{csv_filepath}': {e}")
        return [] # Return empty list on error
    return data_rows

def main():
    """
    Main function to parse arguments, load data, and run GUI automation.
    """
    parser = argparse.ArgumentParser(description="Automate form filling using mouse coordinates and CSV data.")
    parser.add_argument("csv_file", help="Path to the input CSV file (required).")
    parser.add_argument("--coords_file", default="coords.txt",
                        help="Path to the coordinates file (default: coords.txt).")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Delay in seconds between pyautogui actions (default: 0.5).")

    args = parser.parse_args()

    try:
        print(f"Loading coordinates from: {args.coords_file}")
        coordinates_map, ordered_coord_names = parse_coordinates(args.coords_file)
        if not coordinates_map or not ordered_coord_names:
            print(f"No coordinates loaded from '{args.coords_file}' or file is empty/invalid. Exiting.")
            return

        print(f"Loading CSV data from: {args.csv_file}")
        form_data_rows = read_csv_data(args.csv_file)
        if not form_data_rows:
            print(f"No data loaded from CSV file '{args.csv_file}' or file is empty. Exiting.")
            return

    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e: # Catch any other unexpected errors during setup
        print(f"An unexpected error occurred during setup: {e}")
        return

    # --- GUI Automation ---
    print("\nStarting GUI automation process...")
    print("IMPORTANT: Please do not move the mouse or use the keyboard during automation!")
    print("You have 3 seconds to switch to the target window...")
    time.sleep(3) # Give user time to switch to the target window


    # Define csv_headers here if needed for some initial checks,
    # but the primary logic will use 'action_name in row'
    # csv_headers = list(form_data_rows[0].keys()) # Example if needed elsewhere

    for i, row in enumerate(form_data_rows):
        print(f"\nProcessing row {i+1}/{len(form_data_rows)}: {row}")
        try:
            for action_name in ordered_coord_names:
                if action_name not in coordinates_map:
                    print(f"  Warning: Action '{action_name}' from ordered list not in coordinates_map. Skipping.")
                    continue

                x, y = coordinates_map[action_name]

                # Check if action_name corresponds to a data field in the current CSV row
                if action_name in row:
                    value = row[action_name] # Direct access as 'action_name in row' is true
                    print(f"    Performing data entry for '{action_name}' at ({x},{y}) with value '{value}'")
                    pyautogui.moveTo(x, y, duration=0.2)
                    pyautogui.click()
                    time.sleep(args.delay / 2) # Short sleep after click before typing
                    pyautogui.typewrite(str(value), interval=0.05)
                    print(f"    Typed '{value}' into field '{action_name}'.")
                    time.sleep(args.delay) # General delay after typing a field
                else:
                    # This is a click-only action
                    print(f"    Performing click-only action '{action_name}' at ({x},{y}).")
                    pyautogui.moveTo(x, y, duration=0.2)
                    pyautogui.click()
                    print(f"    Clicked '{action_name}'.")
                    time.sleep(1) # 1-second delay specifically for click-only actions

            print(f"  All actions for row {i+1} completed.")
            time.sleep(args.delay * 2) # Longer delay after all actions for a row are complete


        except pyautogui.FailSafeException:
            print("\nFAIL-SAFE TRIGGERED! PyAutoGUI mouse movement to a corner of the screen was detected.")
            print("Automation stopped to prevent unintended actions.")
            return
        except Exception as e:
            print(f"An error occurred during PyAutoGUI actions for row {i+1}: {e}")
            print("Skipping to the next row if possible, or stopping if critical.")
            # Depending on the error, you might want to 'continue' or 'return'
            # For now, let's stop on any pyautogui error to be safe
            return


    print("\nAutomation complete for all rows.")

if __name__ == "__main__":
    main()
