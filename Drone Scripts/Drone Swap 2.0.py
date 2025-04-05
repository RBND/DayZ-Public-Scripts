import tkinter as tk
from tkinter import ttk, filedialog
from pynput import keyboard, mouse
import threading
import time
import os
import json


class MouseAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Swap Tool 2.0")
        self.root.geometry("325x300")

        # Make window always on top
        self.root.attributes("-topmost", True)

        # Coordinates variables
        self.pickup1_coords = None
        self.pickup2_coords = None
        self.pickup3_coords = None
        self.dropoff_coords = None

        # Default keybindings
        self.keybindings = {
            "pickup1": keyboard.Key.f1,
            "pickup2": keyboard.Key.f2,
            "pickup3": keyboard.Key.f3,
            "reset": keyboard.Key.f5
        }

        # Key mapping for display purposes
        self.key_display_names = {
            str(keyboard.Key.f1): "F1",
            str(keyboard.Key.f2): "F2",
            str(keyboard.Key.f3): "F3",
            str(keyboard.Key.f4): "F4",
            str(keyboard.Key.f5): "F5",
            str(keyboard.Key.f6): "F6",
            str(keyboard.Key.f7): "F7",
            str(keyboard.Key.f8): "F8",
            str(keyboard.Key.f9): "F9",
            str(keyboard.Key.f10): "F10",
            str(keyboard.Key.f11): "F11",
            str(keyboard.Key.f12): "F12"
        }

        # State variables
        self.waiting_for_pickup = False
        self.waiting_for_dropoff = False
        self.current_pickup_key = None
        self.is_configured = False
        self.waiting_for_keybind = False
        self.current_keybind_target = None

        # Load settings if they exist
        self.settings_file = "mouse_automation_settings.json"
        self.load_settings()

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create content frame (will be on top of background)
        self.content_frame = tk.Frame(self.main_frame, bg='white', bd=0, relief=tk.GROOVE)
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Main tab
        self.main_tab = tk.Frame(self.notebook, bg='grey')
        self.notebook.add(self.main_tab, text="Main")

        # Settings tab
        self.settings_tab = tk.Frame(self.notebook, bg='grey')
        self.notebook.add(self.settings_tab, text="Settings")

        # About tab
        self.about_tab = tk.Frame(self.notebook, bg='grey')
        self.notebook.add(self.about_tab, text="About")

        # Create UI elements for main tab
        self.status_label = tk.Label(self.main_tab,
                                     text=f"DRONE SWAPPER 2.0",
                                     font=("Arial", 12), bg='grey')
        self.status_label.pack(pady=20)

        self.pickup1_label = tk.Label(self.main_tab,
                                      text=f"Swap Drone 1 ({self.get_key_display_name('pickup1')}): Not set",
                                      font=("Arial", 10), bg='grey')
        self.pickup1_label.pack(pady=1)

        self.pickup2_label = tk.Label(self.main_tab,
                                      text=f"Swap Drone 2 ({self.get_key_display_name('pickup2')}): Not set",
                                      font=("Arial", 10), bg='grey')
        self.pickup2_label.pack(pady=1)

        self.pickup3_label = tk.Label(self.main_tab,
                                      text=f"Swap Drone 3 ({self.get_key_display_name('pickup3')}): Not set",
                                      font=("Arial", 10), bg='grey')
        self.pickup3_label.pack(pady=1)

        self.dropoff_label = tk.Label(self.main_tab, text="Dropoff: Not set", font=("Arial", 10), bg='grey')
        self.dropoff_label.pack(pady=1)

        self.instruction_label = tk.Label(self.main_tab, text=self.get_instruction_text(),
                                          font=("Arial", 10), justify=tk.LEFT, bg='grey')
        self.instruction_label.pack(pady=5)

        # Create UI elements for settings tab
        self.settings_frame = tk.Frame(self.settings_tab, bg='grey')
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Keybinding settings
        tk.Label(self.settings_frame, text="Custom Keybindings", font=("Arial", 12, "bold"), bg='grey').grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              sticky="w",
                                                                                                              pady=(
                                                                                                              0, 10))

        # Pickup 1 keybinding
        tk.Label(self.settings_frame, text="Drone 1 Swap Key:", bg='grey').grid(row=1, column=0, sticky="w", pady=5)
        self.pickup1_btn = tk.Button(self.settings_frame,
                                     text=self.get_key_display_name('pickup1'),
                                     command=lambda: self.start_keybind_listen('pickup1'))
        self.pickup1_btn.grid(row=1, column=1, sticky="w", padx=10)

        # Pickup 2 keybinding
        tk.Label(self.settings_frame, text="Drone 2 Swap Key:", bg='grey').grid(row=2, column=0, sticky="w", pady=5)
        self.pickup2_btn = tk.Button(self.settings_frame,
                                     text=self.get_key_display_name('pickup2'),
                                     command=lambda: self.start_keybind_listen('pickup2'))
        self.pickup2_btn.grid(row=2, column=1, sticky="w", padx=10)

        # Pickup 3 keybinding
        tk.Label(self.settings_frame, text="Drone 3 Swap Key:", bg='grey').grid(row=3, column=0, sticky="w", pady=5)
        self.pickup3_btn = tk.Button(self.settings_frame,
                                     text=self.get_key_display_name('pickup3'),
                                     command=lambda: self.start_keybind_listen('pickup3'))
        self.pickup3_btn.grid(row=3, column=1, sticky="w", padx=10)

        # Reset keybinding
        tk.Label(self.settings_frame, text="Reset Coordinates:", bg='grey').grid(row=4, column=0, sticky="w", pady=5)
        self.reset_btn = tk.Button(self.settings_frame,
                                   text=self.get_key_display_name('reset'),
                                   command=lambda: self.start_keybind_listen('reset'))
        self.reset_btn.grid(row=4, column=1, sticky="w", padx=10)

        # Save settings button
        self.save_btn = tk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_btn.grid(row=7, column=0, columnspan=2, pady=20)

        #Create UI Elements for About Tab
        self.status_label = tk.Label(self.about_tab,
                                    text=f"ROBOTS NEVER DIE",
                                    font=("Arial", 12), bg='grey')
        self.status_label.pack(pady=20)

        self.about_label = tk.Label(self.about_tab, text=self.get_about_text(),
                                          font=("Arial", 10), justify=tk.CENTER, bg='grey')
        self.about_label.pack(pady=5)

    def get_about_text(self):
        return (f"This drone swapper tool was\n"
                f"created by RBND for friends.\n"
                f"If you're not a friend\n"
                f"go fuck yourself.\n"
                f")

        # Setup keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Setup mouse listener (will be activated when needed)
        self.mouse_listener = None

    def get_key_display_name(self, binding_name):
        key = self.keybindings.get(binding_name)
        if key:
            return self.key_display_names.get(str(key), str(key))
        return "Not Set"

    def get_instruction_text(self):
        return (f"Instructions:\n"
                f"1. Press {self.get_key_display_name('pickup1')}, {self.get_key_display_name('pickup2')}, or {self.get_key_display_name('pickup3')} to configure pickup points\n"
                f"2. Click to set the corresponding pickup point\n"
                f"3. Click to set dropoff point (shared for all)\n"
                f"4. Press the same key again to perform the action\n"
                f"5. Press {self.get_key_display_name('reset')} to reset all coordinates")

    def choose_background(self):
        pass  # Background selection is removed.

    def set_default_background(self):
        pass  # Background setup is removed.

    def start_keybind_listen(self, target):
        # Stop any existing keybind listening
        if self.waiting_for_keybind:
            return

        self.waiting_for_keybind = True
        self.current_keybind_target = target

        # Update button text
        button = getattr(self, f"{target}_btn")
        button.config(text="Press any F key...")

        # Create a separate listener for this
        self.keybind_listener = keyboard.Listener(on_press=self.on_keybind_press)
        self.keybind_listener.start()

    def on_keybind_press(self, key):
        # Only accept F keys for keybindings
        if not self.waiting_for_keybind or not hasattr(key, 'name') or not key.name.startswith('f'):
            return

        # Get the button for the current target
        button = getattr(self, f"{self.current_keybind_target}_btn")

        # Update keybinding
        self.keybindings[self.current_keybind_target] = key
        button.config(text=self.key_display_names.get(str(key), str(key)))

        # Update labels
        if self.current_keybind_target == 'pickup1':
            self.pickup1_label.config(text=f"Pickup 1 ({self.get_key_display_name('pickup1')}): " +
                                           (
                                               "Not set" if self.pickup1_coords is None else f"{self.pickup1_coords[0]}, {self.pickup1_coords[1]}"))
        elif self.current_keybind_target == 'pickup2':
            self.pickup2_label.config(text=f"Pickup 2 ({self.get_key_display_name('pickup2')}): " +
                                           (
                                               "Not set" if self.pickup2_coords is None else f"{self.pickup2_coords[0]}, {self.pickup2_coords[1]}"))
        elif self.current_keybind_target == 'pickup3':
            self.pickup3_label.config(text=f"Pickup 3 ({self.get_key_display_name('pickup3')}): " +
                                           (
                                               "Not set" if self.pickup3_coords is None else f"{self.pickup3_coords[0]}, {self.pickup3_coords[1]}"))

        # Update instructions
        self.instruction_label.config(text=self.get_instruction_text())

        # Reset state
        self.waiting_for_keybind = False
        self.current_keybind_target = None

        # Stop the listener
        self.keybind_listener.stop()
        return False

    def save_settings(self):
        settings = {
            "keybindings": {k: str(v) for k, v in self.keybindings.items()},
            "bg_image_path": getattr(self, 'bg_image_path', None)
        }

        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            tk.messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def load_settings(self):
        if not os.path.exists(self.settings_file):
            return

        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)

            # Load keybindings
            if "keybindings" in settings:
                for k, v in settings["keybindings"].items():
                    # Convert string representation back to Key object
                    for key_obj in keyboard.Key:
                        if str(key_obj) == v:
                            self.keybindings[k] = key_obj

            # Load background image path
            if "bg_image_path" in settings and settings["bg_image_path"]:
                self.bg_image_path = settings["bg_image_path"]
                if os.path.exists(self.bg_image_path):
                    image = Image.open(self.bg_image_path)
                    image = image.resize((600, 500), Image.LANCZOS)
                    self.bg_image = ImageTk.PhotoImage(image)
                    if hasattr(self, 'bg_label'):
                        self.bg_label.configure(image=self.bg_image)
        except Exception as e:
            print(f"Failed to load settings: {str(e)}")

    def on_key_press(self, key):
        # Check if we're waiting for a keybind
        if self.waiting_for_keybind:
            return

        # Check which action to perform based on the pressed key
        for action, bound_key in self.keybindings.items():
            if key == bound_key:
                if action == 'pickup1':
                    if self.pickup1_coords is None or self.dropoff_coords is None:
                        self.start_configuration("pickup1")
                    else:
                        self.perform_action("pickup1")
                elif action == 'pickup2':
                    if self.pickup2_coords is None or self.dropoff_coords is None:
                        self.start_configuration("pickup2")
                    else:
                        self.perform_action("pickup2")
                elif action == 'pickup3':
                    if self.pickup3_coords is None or self.dropoff_coords is None:
                        self.start_configuration("pickup3")
                    else:
                        self.perform_action("pickup3")
                elif action == 'reset':
                    self.reset_coordinates()

    def reset_coordinates(self):
        # Reset all coordinates and state
        self.pickup1_coords = None
        self.pickup2_coords = None
        self.pickup3_coords = None
        self.dropoff_coords = None
        self.waiting_for_pickup = False
        self.waiting_for_dropoff = False
        self.current_pickup_key = None
        self.is_configured = False

        # Update UI
        self.pickup1_label.config(text=f"Pickup 1 ({self.get_key_display_name('pickup1')}): Not set")
        self.pickup2_label.config(text=f"Pickup 2 ({self.get_key_display_name('pickup2')}): Not set")
        self.pickup3_label.config(text=f"Pickup 3 ({self.get_key_display_name('pickup3')}): Not set")
        self.dropoff_label.config(text="Dropoff: Not set")
        self.status_label.config(text="Coordinates reset. Press a pickup key to configure")

        # Stop mouse listener if active
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()

    def start_configuration(self, key):
        self.current_pickup_key = key

        # If dropoff is already set, we only need to configure the pickup point
        if self.dropoff_coords is not None:
            self.status_label.config(text=f"Click to set {key} pickup point")
            self.waiting_for_pickup = True
            self.waiting_for_dropoff = False
        else:
            self.status_label.config(text=f"Click to set {key} pickup point")
            self.waiting_for_pickup = True
            self.waiting_for_dropoff = False

        # Start mouse listener
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()

        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            if self.waiting_for_pickup:
                # Store pickup coordinates based on which key was pressed
                if self.current_pickup_key == "pickup1":
                    self.pickup1_coords = (x, y)
                    self.pickup1_label.config(text=f"Pickup 1 ({self.get_key_display_name('pickup1')}): {x}, {y}")
                elif self.current_pickup_key == "pickup2":
                    self.pickup2_coords = (x, y)
                    self.pickup2_label.config(text=f"Pickup 2 ({self.get_key_display_name('pickup2')}): {x}, {y}")
                elif self.current_pickup_key == "pickup3":
                    self.pickup3_coords = (x, y)
                    self.pickup3_label.config(text=f"Pickup 3 ({self.get_key_display_name('pickup3')}): {x}, {y}")

                # If dropoff is already set, we're done configuring
                if self.dropoff_coords is not None:
                    self.status_label.config(
                        text=f"Configuration complete. Press {self.get_key_display_name(self.current_pickup_key)} to perform action.")
                    self.waiting_for_pickup = False
                    self.mouse_listener.stop()
                    return False
                else:
                    self.status_label.config(text="Click to set dropoff point")
                    self.waiting_for_pickup = False
                    self.waiting_for_dropoff = True
                    return True  # Continue listening

            elif self.waiting_for_dropoff:
                self.dropoff_coords = (x, y)
                self.dropoff_label.config(text=f"Dropoff: {x}, {y}")
                self.status_label.config(
                    text=f"Configuration complete. Press {self.get_key_display_name(self.current_pickup_key)} to perform action.")
                self.waiting_for_dropoff = False
                self.mouse_listener.stop()
                return False  # Stop listening

    def perform_action(self, key):
        # Get the appropriate pickup coordinates based on which key was pressed
        pickup_coords = None
        if key == "pickup1" and self.pickup1_coords is not None:
            pickup_coords = self.pickup1_coords
            display_key = self.get_key_display_name('pickup1')
        elif key == "pickup2" and self.pickup2_coords is not None:
            pickup_coords = self.pickup2_coords
            display_key = self.get_key_display_name('pickup2')
        elif key == "pickup3" and self.pickup3_coords is not None:
            pickup_coords = self.pickup3_coords
            display_key = self.get_key_display_name('pickup3')

        # Make sure we have both pickup and dropoff coordinates
        if pickup_coords is None or self.dropoff_coords is None:
            self.status_label.config(text=f"Error: {key} pickup or dropoff not configured")
            return

        self.status_label.config(text=f"Performing {display_key} action...")

        # Run the mouse action in a separate thread to avoid freezing the UI
        threading.Thread(
            target=lambda: self._execute_mouse_action(pickup_coords, self.dropoff_coords, display_key)).start()

    def _execute_mouse_action(self, pickup, dropoff, key_display):
        mouse_controller = mouse.Controller()

        # Move to pickup position
        mouse_controller.position = pickup
        time.sleep(0.2)  # Small delay

        # Click and hold
        mouse_controller.press(mouse.Button.left)
        time.sleep(0.2)  # Small delay

        # Move to dropoff position
        mouse_controller.position = dropoff
        time.sleep(0.2)  # Small delay

        # Release
        mouse_controller.release(mouse.Button.left)

        # Update UI from the main thread
        self.root.after(0, lambda: self.status_label.config(
            text=f"{key_display} action completed. Press any configured key to repeat or configure."))


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseAutomationApp(root)
    root.mainloop()