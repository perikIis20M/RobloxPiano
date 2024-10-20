import tkinter as tk
import time
import threading
import keyboard  # For keybinds
from pynput.keyboard import Controller
from tkinter import messagebox, filedialog

# Initialize keyboard controller for typing the music
keyboard_controller = Controller()

# Define initial typing speed and control flags
typing_speed = 0.1  # seconds (default)
is_playing = False
is_looping = False

# Function to press multiple keys at once (for handling combinations like [9yip])
def press_keys(keys):
    for key in keys:
        keyboard_controller.press(key)
    for key in keys:
        keyboard_controller.release(key)

# Function to play the music
def play_music(music_sheet):
    global is_playing
    while True:
        for segment in music_sheet.split():
            if not is_playing:
                break  # Stop playing if 'stop_music' is called
            # Handle bracketed sequences for multiple key presses (e.g., [9yip])
            if segment.startswith("[") and segment.endswith("]"):
                keys = segment[1:-1]  # Remove brackets
                press_keys(keys)
            else:
                # Split by special characters, but keep track of valid keys
                for char in segment:
                    if char:  # Ignore empty characters
                        try:
                            keyboard_controller.press(char)
                            keyboard_controller.release(char)
                        except ValueError:
                            print(f"Invalid key: {char}")  # Handle invalid keys
            time.sleep(typing_speed)  # Add delay between key presses
        if not is_looping:
            break  # Exit the loop if not looping

# Function to stop playing the music
def stop_music():
    global is_playing
    is_playing = False

# Function to handle the play button
def start_playing():
    global is_playing
    is_playing = True
    music_sheet = text_field.get("1.0", tk.END).strip()  # Get music from text box
    if music_sheet:
        threading.Thread(target=play_music, args=(music_sheet,)).start()  # Start playing in a new thread
    else:
        messagebox.showwarning("Input Error", "No music notes to play!")

# Function to update the typing speed when the slider is adjusted
def update_speed(value):
    global typing_speed
    typing_speed = float(value)  # Convert slider value to float

# Function to handle the keybinds for starting and stopping music
def check_keybinds():
    while True:
        # Play music with Ctrl + Shift + A
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('a'):
            play_button.invoke()  # Simulate play button press
        # Stop music with Ctrl + Shift + S
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('s'):
            stop_button.invoke()  # Simulate stop button press
        time.sleep(0.1)

# Function to toggle looping
def toggle_looping():
    global is_looping
    is_looping = not is_looping
    loop_button.config(relief=tk.SUNKEN if is_looping else tk.RAISED)

# Function to save music sheet to a file
def save_music_sheet():
    music_sheet = text_field.get("1.0", tk.END).strip()
    if music_sheet:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(music_sheet)
            messagebox.showinfo("Success", "Music sheet saved successfully!")
    else:
        messagebox.showwarning("Input Error", "No music notes to save!")

# Function to load music sheet from a file
def load_music_sheet():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            music_sheet = file.read()
            text_field.delete("1.0", tk.END)  # Clear current text
            text_field.insert(tk.END, music_sheet)  # Insert loaded music sheet

# Setting up the GUI
root = tk.Tk()
root.title("Music Player GUI")

# Text field to input or display music notes
text_field = tk.Text(root, height=10, width=50)
text_field.pack(pady=10)

# Play button
play_button = tk.Button(root, text="Play Music", command=start_playing)
play_button.pack(pady=5)

# Stop button
stop_button = tk.Button(root, text="Stop Music", command=stop_music)
stop_button.pack(pady=5)

# Loop button
loop_button = tk.Button(root, text="Toggle Looping", command=toggle_looping)
loop_button.pack(pady=5)

# Save button
save_button = tk.Button(root, text="Save Music Sheet", command=save_music_sheet)
save_button.pack(pady=5)

# Load button
load_button = tk.Button(root, text="Load Music Sheet", command=load_music_sheet)
load_button.pack(pady=5)

# Slider to adjust the typing speed (delay between notes)
speed_label = tk.Label(root, text="Adjust typing speed (seconds delay):")
speed_label.pack(pady=5)

speed_slider = tk.Scale(root, from_=0.05, to=1.0, resolution=0.05, orient=tk.HORIZONTAL, command=update_speed)
speed_slider.set(typing_speed)  # Set the initial speed
speed_slider.pack(pady=5)

# Instructions label
instruction_label = tk.Label(root, text="Press 'Ctrl + Shift + A' to play and 'Ctrl + Shift + S' to stop music.")
instruction_label.pack(pady=10)

# Credits label
credits_label = tk.Label(root, text="Credits: The Amazing Digital Circus - Main Theme")
credits_label.pack(pady=10)

# Start the keybind check in a separate thread
threading.Thread(target=check_keybinds, daemon=True).start()

# Start the GUI event loop
root.mainloop()
