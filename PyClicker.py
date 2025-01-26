import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key, Listener
import threading
import time

# Initialize controllers
mouse = MouseController()
keyboard = KeyboardController()

# Variables to control the autoclicker state
running = threading.Event()
interval = 0.1  # Default interval in seconds
click_count = 0
start_time = None
custom_stop_key = None
custom_toggle_key = None

# Get list of all keyboard keys
key_options = ["None"] + sorted(list(Key.__members__.keys()) + [chr(i) for i in range(32, 127)])

# Functions for autoclicker functionality
def start_autoclicker(button, key):
    global click_count, start_time
    start_time = time.time()
    while running.is_set():
        if button:
            mouse.click(button)
            click_count += 1
        if key:
            keyboard.press(key)
            keyboard.release(key)
            click_count += 1
        time.sleep(interval)

def start(button=None, key=None):
    if not running.is_set():
        running.set()
        thread = threading.Thread(target=start_autoclicker, args=(button, key))
        thread.daemon = True
        thread.start()

def stop():
    global start_time
    if running.is_set():
        running.clear()
        start_time = None

def toggle_autoclicker():
    if running.is_set():
        stop()
    else:
        handle_start()

# Function to handle starting from the UI
def handle_start():
    selected_button = mouse_button_var.get()
    selected_key = key_var.get()

    button = None
    key = None

    if selected_button == "None":
        button = None
    elif selected_button == "Left":
        button = Button.left
    elif selected_button == "Right":
        button = Button.right
    elif selected_button == "Middle":
        button = Button.middle

    if selected_key == "None":
        key = None
    elif selected_key and selected_key in Key.__members__:
        key = Key[selected_key]
    elif selected_key and len(selected_key) == 1:
        key = selected_key

    # Calculate interval
    interval_value = interval_var.get()
    unit = interval_unit_var.get()
    global interval
    if unit == "Milliseconds":
        interval = interval_value / 1000
    elif unit == "Seconds":
        interval = interval_value
    elif unit == "Minutes":
        interval = interval_value * 60

    start(button, key)

# Listener for customizable keys
def on_press(key):
    global custom_stop_key, custom_toggle_key
    try:
        if key == custom_stop_key:
            root.destroy()
        elif key == custom_toggle_key:
            toggle_autoclicker()
    except AttributeError:
        pass

listener = Listener(on_press=on_press)
listener.start()

# Function to adjust UI scaling dynamically
def adjust_ui(event):
    width = root.winfo_width()
    height = root.winfo_height()

    scale_x = width / 800
    scale_y = height / 600

    for frame in [row1_frame, row2_frame, row3_frame, row4_frame]:
        for widget in frame.winfo_children():
            widget.config(font=("Arial", int(12 * scale_x)))

# GUI setup
root = tk.Tk()
root.title("Autoclicker")
root.geometry("1600x1200")
root.configure(bg="#007B83")
root.state("zoomed")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#007B83", foreground="white", font=("Gotham", 16))
style.configure("TButton", background="#005F6B", foreground="white", font=("Gotham", 16, "bold"), relief="raised")
style.configure("TCombobox", fieldbackground="white", background="#005F6B", font=("Gotham", 14))

# Row 1: Mouse button, key, and interval settings
row1_frame = tk.Frame(root, bg="#007B83")
row1_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

mouse_button_label = ttk.Label(row1_frame, text="Select Mouse Button:")
mouse_button_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

mouse_button_var = tk.StringVar(value="Left")
mouse_button_dropdown = ttk.Combobox(row1_frame, textvariable=mouse_button_var, state="readonly")
mouse_button_dropdown["values"] = ["None", "Left", "Right", "Middle"]
mouse_button_dropdown.grid(row=0, column=1, padx=20, pady=10, sticky="w")

key_label = ttk.Label(row1_frame, text="Select Key (Optional):")
key_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")

key_var = tk.StringVar(value="None")
key_dropdown = ttk.Combobox(row1_frame, textvariable=key_var, state="readonly")
key_dropdown["values"] = key_options
key_dropdown.grid(row=0, column=3, padx=20, pady=10, sticky="w")

# Row 2: Interval settings
row2_frame = tk.Frame(root, bg="#007B83")
row2_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

interval_label = ttk.Label(row2_frame, text="Set Interval:")
interval_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

interval_var = tk.DoubleVar(value=0.1)
interval_entry = ttk.Entry(row2_frame, textvariable=interval_var)
interval_entry.grid(row=0, column=1, padx=20, pady=10, sticky="w")

interval_unit_label = ttk.Label(row2_frame, text="Interval Unit:")
interval_unit_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")

interval_unit_var = tk.StringVar(value="Seconds")
interval_unit_dropdown = ttk.Combobox(row2_frame, textvariable=interval_unit_var, state="readonly")
interval_unit_dropdown["values"] = ["Milliseconds", "Seconds", "Minutes"]
interval_unit_dropdown.grid(row=0, column=3, padx=20, pady=10, sticky="w")

# Row 3: Stop and toggle key settings
row3_frame = tk.Frame(root, bg="#007B83")
row3_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

stop_key_label = ttk.Label(row3_frame, text="Set Stop Key:")
stop_key_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

stop_key_var = tk.StringVar()
stop_key_dropdown = ttk.Combobox(row3_frame, textvariable=stop_key_var, state="readonly")
stop_key_dropdown["values"] = key_options
stop_key_dropdown.grid(row=0, column=1, padx=20, pady=10, sticky="w")

def set_stop_key():
    global custom_stop_key
    key = stop_key_var.get()
    if key in Key.__members__:
        custom_stop_key = Key[key]
    elif len(key) == 1:
        custom_stop_key = key

set_stop_key_button = ttk.Button(row3_frame, text="Set Stop Key", command=set_stop_key)
set_stop_key_button.grid(row=0, column=2, padx=20, pady=10, sticky="w")

toggle_key_label = ttk.Label(row3_frame, text="Set Toggle Key:")
toggle_key_label.grid(row=0, column=3, padx=20, pady=10, sticky="w")

toggle_key_var = tk.StringVar()
toggle_key_dropdown = ttk.Combobox(row3_frame, textvariable=toggle_key_var, state="readonly")
toggle_key_dropdown["values"] = key_options
toggle_key_dropdown.grid(row=0, column=4, padx=20, pady=10, sticky="w")

def set_toggle_key():
    global custom_toggle_key
    key = toggle_key_var.get()
    if key in Key.__members__:
        custom_toggle_key = Key[key]
    elif len(key) == 1:
        custom_toggle_key = key

set_toggle_key_button = ttk.Button(row3_frame, text="Set Toggle Key", command=set_toggle_key)
set_toggle_key_button.grid(row=0, column=5, padx=20, pady=10, sticky="w")

# Row 4: Start, Stop, and Click Count
row4_frame = tk.Frame(root, bg="#007B83")
row4_frame.grid(row=3, column=0, columnspan=4, sticky="nsew")

start_button = ttk.Button(row4_frame, text="Start", command=handle_start)
start_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

stop_button = ttk.Button(row4_frame, text="Stop", command=stop)
stop_button.grid(row=0, column=1, padx=20, pady=10, sticky="w")

click_count_label = ttk.Label(row4_frame, text="Clicks: 0")
click_count_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")

def update_click_count():
    while True:
        elapsed_time = time.time() - start_time if start_time and running.is_set() else 0
        click_count_label.config(text=f"Clicks: {click_count} | Time: {elapsed_time:.2f} seconds")
        time.sleep(0.1)

threading.Thread(target=update_click_count, daemon=True).start()

# Run the application
root.mainloop()
