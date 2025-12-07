import customtkinter as ctk
import os
from typing import Dict, Any
import json
from views import (
    create_main_app_header,
    create_file_selection_section,
    create_action_buttons,
    create_status_section
)
from handlers import (
    handle_browse_input_file,
    handle_browse_output_file,
    handle_process_file,
    handle_clear_files,
    handle_open_settings
)
from settings_view import SettingsPage

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class ModernGUIApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Modern File Processor")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Current settings
        self.current_settings = {
            "output_format": ".las",
            "points_to_render": 10.0
        }
        
        # Input and output file paths
        self.input_file_path = None
        self.output_file_path = None
        
        # Create UI
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header using views module
        create_main_app_header(main_container)
        
        # Create file selection section using views module
        self.input_file_label, self.output_file_label = create_file_selection_section(
            main_container,
            lambda: handle_browse_input_file(self),
            lambda: handle_browse_output_file(self)
        )
        
        # Create action buttons using views module
        create_action_buttons(
            main_container,
            lambda: handle_process_file(self),
            lambda: handle_open_settings(self),
            lambda: handle_clear_files(self)
        )
        
        # Create status section using views module
        self.status_label, self.progress_bar = create_status_section(main_container)
    
    def on_settings_saved(self, settings):
        """Callback when settings are saved"""
        self.current_settings = settings
        self.update_status("Settings saved successfully!")
    
    def update_status(self, message, error=False):
        """Update status label"""
        color = "red" if error else ("green" if "✅" in message else "gray")
        self.status_label.configure(text=message, text_color=color)


def main():
    """Main entry point"""
    app = ModernGUIApp()
    app.mainloop()


if __name__ == "__main__":
    main()

