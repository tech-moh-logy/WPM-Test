# Mohammed's COMMAND-LINE APPLICATION 
# 2024 MOHAMMED. All rights reserved. Unauthorized copying and pasting of the content of this application is prohibited. 
# This work is licensed under Attribution-NonCommercial-NoDerivatives 4.0 International

import curses
from curses import wrapper
import time
import random

# Function to display the start screen
def start_screen(stdscr):
    # stdscr stands for "standard screen."
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

# Function to display the target text, user input, and WPM
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Default to green for correct characters
        if char != correct_char:
            color = curses.color_pair(2)  # Red for incorrect characters

        stdscr.addstr(0, i, char, color)

# Function to load a random line of text from a file
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

# Function to perform the WPM test
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Exit if Escape key is pressed; ASCII values (27 = Escape key)
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            # Check if the pressed key corresponds to a backspace character
            # This includes the special key "KEY_BACKSPACE" and the ASCII values for backspace ('\b') and delete ("\x7f")
            # Note: The interpretation of these keys may vary across different operating systems.
            # On some systems, 'KEY_BACKSPACE' represents the backspace key, while '\b' and '\x7f' are ASCII values for backspace and delete.
            # Ensure compatibility by considering the key representations based on the target operating system.
            # If true, handle backspace functionality to remove the last typed character
            if len(current_text) > 0:
                current_text.pop()
              
        elif len(current_text) < len(target_text):
            # Prevents overlapping of current text
            current_text.append(key)

# Main function
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:  # Exit if Escape key is pressed
            break

# Run the main function using the curses wrapper
wrapper(main)
