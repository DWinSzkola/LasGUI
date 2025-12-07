import customtkinter as ctk
from views import (
    create_settings_page_ui,
    create_settings_buttons
)
from handlers import (
    handle_save_settings,
    handle_reset_settings
)


class SettingsPage(ctk.CTkToplevel):
    """Settings window with configurable parameters"""
    
    def __init__(self, parent, settings_callback, current_settings):
        super().__init__(parent)
        
        self.settings = current_settings.copy() if current_settings else {}
        self.settingsWidget = {}
        self.settings_callback = settings_callback
        
        # Configure window properties first
        self.title("Settings")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Set the settings window to be on top of the main window
        self.transient(parent)  # Make it a transient window (child of parent)
        
        # Create UI using views module (includes "Hello Settings" text)
        main_frame, self.output_format, button_frame = create_settings_page_ui(
            self, settings_callback, current_settings, self.settingsWidget, self.settings
        )
        
        # Create buttons using views module
        create_settings_buttons(
            button_frame,
            self.save_settings,
            self.reset_settings,
            self.destroy
        )
        
        # Load default settings
        self.reset_settings()
        
        # Center and show the window
        self.center_window()
        self.update_idletasks()  # Process all pending events
        self.lift()  # Bring to the front
        self.focus_force()  # Force focus on the window
        self.grab_set()  # Make sure the user can't interact with the parent window while this is open
        self.update()  # Update to ensure window is displayed
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def save_settings(self):
        """Save current settings"""
        handle_save_settings(self)
    
    def reset_settings(self):
        """Reset all settings to default values"""
        handle_reset_settings(self)

