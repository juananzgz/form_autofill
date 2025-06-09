import time
import os

try:
    import pyautogui
except ImportError:
    print("Error: The 'pyautogui' library is not installed.")
    print("Please install it by running: pip install pyautogui")
    print("You may need to install other system dependencies for pyautogui to work.")
    print("Refer to pyautogui documentation: https://pyautogui.readthedocs.io/en/latest/install.html")
    exit()

def get_coordinates_script():
    """
    Interactively captures mouse coordinates for UI elements and saves them to coords.txt.
    """
    output_filename = "coords.txt"

    print("Welcome to the Python Coordinate Capturer!")
    print("This script will help you capture X,Y mouse coordinates for UI elements.")
    print(f"Coordinates will be saved to '{output_filename}'.")
    print("You will be prompted to enter a name for each coordinate.")
    print("After entering a name, you will have 5 seconds to position your mouse.")
    print("Type 'done' (and press Enter) when you have captured all coordinates.")
    print("-" * 30)

    # Check if coords.txt exists and ask if user wants to append or overwrite
    if os.path.exists(output_filename):
        while True:
            choice = input(
                f"'{output_filename}' already exists. Do you want to (o)verwrite it, (a)ppend to it, or (q)uit? [o/a/q]: "
            ).lower()
            if choice == 'o':
                # Overwrite by opening in 'w' mode later
                mode = 'w'
                print(f"'{output_filename}' will be overwritten.")
                break
            elif choice == 'a':
                mode = 'a' # Append mode
                print(f"New coordinates will be appended to '{output_filename}'.")
                break
            elif choice == 'q':
                print("Exiting script.")
                return
            else:
                print("Invalid choice. Please enter 'o', 'a', or 'q'.")
    else:
        mode = 'w' # Create new file

    try:
        with open(output_filename, mode) as f:
            if mode == 'a' and os.path.getsize(output_filename) > 0:
                f.write("\n") # Add a newline if appending to a non-empty file

            count = 0
            while True:
                count += 1
                prompt_message = f"Enter name for coordinate #{count} (or 'done' to finish): "
                name = input(prompt_message)

                if name.lower() == 'done':
                    break

                if not name:
                    print("Name cannot be empty. Please try again.")
                    count -= 1 # Decrement count as this entry was invalid
                    continue

                if ":" in name:
                    print("Name cannot contain ':'. Please use a different name.")
                    count -= 1
                    continue

                print(f"Position your mouse over '{name}' in the next 5 seconds...")
                for i in range(5, 0, -1):
                    print(f"{i}...", end="", flush=True)
                    time.sleep(1)
                    print("\r", end="", flush=True) # Carriage return to overwrite countdown

                try:
                    x, y = pyautogui.position()
                    f.write(f"{name}:{x},{y}\n")
                    print(f"SUCCESS! Saved: {name} -> ({x},{y})")
                except Exception as e:
                    print(f"Error getting mouse position: {e}")
                    print("Please ensure your environment allows pyautogui to control mouse/keyboard.")
                    print("If using Wayland on Linux, pyautogui might have issues. Try an X11 session.")
                    count -=1 # Decrement count as this entry failed
                    continue


    except IOError as e:
        print(f"Error: Could not write to file {output_filename}. Details: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


    print("-" * 30)
    print(f"Coordinate capturing complete. Data saved to '{output_filename}'.")

if __name__ == "__main__":
    get_coordinates_script()
