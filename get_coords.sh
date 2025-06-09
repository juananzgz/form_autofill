#!/bin/bash

# Output file
OUTPUT_FILE="coords.txt"

# Welcome message and instructions
echo "Welcome to the Coordinate Generation Script!"
echo "This script will help you capture mouse coordinates for various points on your screen."
echo "Instructions:"
echo "1. Make sure you have 'xdotool' installed. If not, please install it (e.g., sudo apt-get install xdotool)."
echo "2. When prompted, enter a descriptive name for the coordinate (e.g., 'username_field', 'login_button')."
echo "3. After entering the name, you will have 5 seconds to position your mouse over the desired element."
echo "4. The script will then capture the mouse coordinates (X,Y)."
echo "5. Enter 'done' or 'exit' as the name when you are finished capturing coordinates."
echo "The coordinates will be saved to '$OUTPUT_FILE'."
echo ""

# Clear the output file if it already exists
> "$OUTPUT_FILE"
echo "Cleared existing '$OUTPUT_FILE'."
echo ""

# Loop to capture coordinates
while true; do
  read -p "Enter a name for the coordinate (or 'done' to finish): " coord_name

  # Check if the user wants to exit
  if [[ "$coord_name" == "done" || "$coord_name" == "exit" ]]; then
    break
  fi

  # Prompt user to position mouse and wait
  echo "Position your mouse over the '$coord_name' element. Capturing in 5 seconds..."
  sleep 5

  # Get mouse location using xdotool and parse X, Y
  MOUSE_INFO=$(xdotool getmouselocation --shell)
  X=$(echo "$MOUSE_INFO" | grep 'X=' | cut -d'=' -f2)
  Y=$(echo "$MOUSE_INFO" | grep 'Y=' | cut -d'=' -f2)

  # Check if X and Y were captured
  if [[ -z "$X" || -z "$Y" ]]; then
    echo "Error: Could not capture mouse coordinates. Make sure xdotool is working correctly."
    echo "If you are running this in a headless environment or via SSH without X forwarding, xdotool may not work."
    continue # Skip to the next iteration
  fi

  # Append to the output file
  echo "${coord_name}:${X},${Y}" >> "$OUTPUT_FILE"
  echo "Saved: ${coord_name} at X=${X}, Y=${Y} to '$OUTPUT_FILE'."
  echo ""
done

# Final message
echo ""
echo "Coordinate capturing complete."
echo "All coordinates have been saved to '$OUTPUT_FILE'."
echo "You can now use this file for your automation scripts."
