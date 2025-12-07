import customtkinter as ctk
import tkinter.filedialog as filedialog
import os
from typing import Dict, Any
import json

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class SettingsPage(ctk.CTkToplevel):
    """Settings window with configurable parameters"""
    
    def __init__(self, parent, settings_callback, current_settings):
        super().__init__(parent)
        self.settings = current_settings
        self.settingsWidget = {}
        self.lift()
        self.settings_callback = settings_callback
        
        
        self.title("Settings")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Set the settings window to be on top of the main window
        self.transient(parent)  # Make it a transient window (child of parent)
        self.grab_set()  # Make sure the user can't interact with the parent window while this is open

        # Center the window
        self.center_window()
        
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="⚙️ Settings", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(10, 30))
        
        # Scrollable frame for settings
        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Example settings - based on your project parameters
        self.create_setting_widget(
            scroll_frame, 
            "Points to render in % (Huge impact on render speed!):", 
            "points_to_render",
            10.0,
            min_value=10.0,
            max_value=100.0,
            step=1.0
        )
        
        self.create_setting_widget(
            scroll_frame,
            "Template 2",
            "Do wypelnienia 2",
            0.97,
            min_value=0.0,
            max_value=1.0,
            step=0.01
        )
        
        self.create_setting_widget(
            scroll_frame,
            "Template 3",
            "Do wypelnienia 3",
            0.2,
            min_value=0.01,
            max_value=10.0,
            step=0.01
        )
        
        
        
        # Output format setting
        output_frame = ctk.CTkFrame(scroll_frame)
        output_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            output_frame, 
            text="Output Format:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.output_format = ctk.CTkComboBox(
            output_frame,
            values=[".las", ".txt", ".csv"],
            width=200,
            
        )
        self.output_format.set(current_settings["output_format"])
        self.output_format.pack(anchor="w", padx=10, pady=(0, 10))
        
        
        
        
        # Checkbox settings
        self.create_checkbox_setting(
            scroll_frame,
            "Enable Verbose Logging",
            "verbose_logging",
            False
        )
        
        self.create_checkbox_setting(
            scroll_frame,
            "Save Intermediate Results",
            "save_intermediate",
            True
        )
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 10))
        
        # Save button
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(side="left", padx=10)
        
        # Reset button
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Default",
            command=self.reset_settings,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="gray",
            hover_color="darkgray"
        )
        reset_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=self.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="red",
            hover_color="darkred"
        )
        cancel_btn.pack(side="right", padx=10)
        
        # Load default settings
        self.reset_settings()
        self.lift()  # Bring to the front
        self.focus()  # Focus the window
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    
    def create_setting_widget(self, parent, label_text, key, default_value, 
                             min_value=0, max_value=100, step=1):
        """Create a setting widget with label and slider"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10, padx=10)
        
        # Label
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Value display and slider frame
        value_frame = ctk.CTkFrame(frame)
        value_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Value label
        value_label = ctk.CTkLabel(
            value_frame,
            text=f"{default_value}",
            font=ctk.CTkFont(size=12),
            width=100
        )
        value_label.pack(side="right", padx=10)
        
        # Slider
        slider = ctk.CTkSlider(
            value_frame,
            from_=min_value,
            to=max_value,
            number_of_steps=int((max_value - min_value) / step),
            command=lambda v: value_label.configure(text=f"{v:.2f}" if step < 1 else f"{int(v)}")
        )
        slider.set(default_value)
        slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Store references
        self.settingsWidget[key] = {
            "value": default_value,
            "slider": slider,
            "label": value_label
        }
    
    def create_checkbox_setting(self, parent, label_text, key, default_value):
        """Create a checkbox setting"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10, padx=10)
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=14)
        )
        checkbox.pack(anchor="w", padx=10, pady=10)
        
        if default_value:
            checkbox.select()
        
        self.settings[key] = {
            "value": default_value,
            "checkbox": checkbox
        }
    
    def save_settings(self):
        """Save current settings"""
        
        
        for key, widget_data in self.settings.items():
            if key == "output_format":
                self.settings[key] = self.output_format.get()
            elif key == "points_to_render":
                self.settings[key] = self.settingsWidget["points_to_render"]["value"]
            elif "checkbox" in widget_data:
                self.settings[key] = widget_data["checkbox"].get()
        print(self.settings)
        # Call callback with settings
        if self.settings_callback:
            self.settings_callback(self.settings)
        
        # Show success message
        success_label = ctk.CTkLabel(
            self,
            text="✅ Settings saved successfully!",
            font=ctk.CTkFont(size=12),
            fg_color="green",
            corner_radius=5
        )
        success_label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2000, success_label.destroy)
    
    def reset_settings(self):
        """Reset all settings to default values"""
        defaults = {
            "PROCENT_INTENSYWNOSCI_FILTRACJI": 2.0,
            "TOLERANCJA_PIONOWOSCI": 0.97,
            "DBSCAN_EPS": 0.2,
            "MIN_PUNKTY_GRUPY": 300,
            "TOLERANCJA_ODLEGLOSCI_RANSAC": 0.1,
            "MIN_INLIERS_PROCENT": 0.5,
            "verbose_logging": False,
            "save_intermediate": True
        }
        
        for key, default_value in defaults.items():
            if key in self.settings:
                widget_data = self.settings[key]
                if "slider" in widget_data:
                    widget_data["slider"].set(default_value)
                    widget_data["label"].configure(
                        text=f"{default_value:.2f}" if isinstance(default_value, float) else f"{int(default_value)}"
                    )
                elif "checkbox" in widget_data:
                    if default_value:
                        widget_data["checkbox"].select()
                    else:
                        widget_data["checkbox"].deselect()


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
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 Modern File Processor",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Process your files with ease",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # File selection section
        file_section = ctk.CTkFrame(main_container)
        file_section.pack(fill="x", pady=20, padx=20)
        
        # Input file section
        input_frame = ctk.CTkFrame(file_section)
        input_frame.pack(fill="x", pady=15, padx=20)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="📁 Input File:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        input_file_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_file_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.input_file_label = ctk.CTkLabel(
            input_file_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.input_file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_input_btn = ctk.CTkButton(
            input_file_frame,
            text="Browse",
            command=self.browse_input_file,
            width=120,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        browse_input_btn.pack(side="right")
        
        # Output file section
        output_frame = ctk.CTkFrame(file_section)
        output_frame.pack(fill="x", pady=15, padx=20)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="💾 Output File:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        output_file_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_file_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.output_file_label = ctk.CTkLabel(
            output_file_frame,
            text="Output will be saved here",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.output_file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_output_btn = ctk.CTkButton(
            output_file_frame,
            text="Choose Location",
            command=self.browse_output_file,
            width=120,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        browse_output_btn.pack(side="right")
        
        # Action buttons section
        button_section = ctk.CTkFrame(main_container, fg_color="transparent")
        button_section.pack(fill="x", pady=30, padx=20)
        
        # Process button
        process_btn = ctk.CTkButton(
            button_section,
            text="⚡ Process File",
            command=self.process_file,
            width=200,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        process_btn.pack(side="left", padx=10)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            button_section,
            text="⚙️ Settings",
            command=self.open_settings,
            width=200,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#2d8659",
            hover_color="#1f5c3f"
        )
        settings_btn.pack(side="left", padx=10)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            button_section,
            text="🗑️ Clear",
            command=self.clear_files,
            width=200,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#8b2d2d",
            hover_color="#5c1f1f"
        )
        clear_btn.pack(side="right", padx=10)
        
        # Status section
        status_frame = ctk.CTkFrame(main_container)
        status_frame.pack(fill="x", pady=20, padx=20)
        
        status_title = ctk.CTkLabel(
            status_frame,
            text="📊 Status:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to process files",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 15))
        self.progress_bar.pack_forget()
    
    def browse_input_file(self):
        """Open file dialog to select input file"""
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All Files", "*.*"),
                ("LAS Files", "*.las"),
                ("Text Files", "*.txt"),
                ("CSV Files", "*.csv"),
                ("Python Files", "*.py")
            ]
        )
        
        if file_path:
            self.input_file_path = file_path
            filename = os.path.basename(file_path)
            self.input_file_label.configure(
                text=filename,
                text_color="white"
            )
            self.update_status(f"Input file selected: {filename}")
    
    def browse_output_file(self):
        """Open file dialog to select output file location"""
        file_path = filedialog.asksaveasfilename(
            title="Save Output File As",
            defaultextension=".las",
            filetypes=[
                ("LAS Files", "*.las"),
                ("Text Files", "*.txt"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.output_file_path = file_path
            filename = os.path.basename(file_path)
            self.output_file_label.configure(
                text=filename,
                text_color="white"
            )
            self.update_status(f"Output location set: {filename}")
    
    def open_settings(self):
        """Open settings window"""
        settings_window = SettingsPage(self, self.on_settings_saved, self.current_settings)
        settings_window.focus()
    
    def on_settings_saved(self, settings):
        """Callback when settings are saved"""
        self.current_settings = settings
        self.update_status("Settings saved successfully!")
    
    def process_file(self):
        """Process the input file"""
        if not self.input_file_path:
            self.update_status("❌ Please select an input file first!", error=True)
            return
        
        if not self.output_file_path:
            self.update_status("❌ Please select an output file location first!", error=True)
            return
        
        if not os.path.exists(self.input_file_path):
            self.update_status("❌ Input file does not exist!", error=True)
            return
        
        # Show progress bar
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 15))
        self.progress_bar.set(0)
        
        self.update_status("Processing file...")
        
        # Simulate processing (replace with actual processing logic)
        self.after(100, self.simulate_processing)
    
    def simulate_processing(self):
        """Simulate file processing with progress updates"""
        # This is a simulation - replace with your actual processing logic
        steps = 10
        for i in range(steps + 1):
            progress = i / steps
            self.progress_bar.set(progress)
            self.update()
            self.after(200)  # Simulate work
        
        # Here you would call your actual processing function
        # For example: process_las_file(self.input_file_path, self.output_file_path, self.current_settings)
        
        try:
            # Example: Copy file as a placeholder (replace with actual processing)
            import shutil
            shutil.copy2(self.input_file_path, self.output_file_path)
            
            self.progress_bar.pack_forget()
            self.update_status(f"✅ File processed successfully! Saved to: {os.path.basename(self.output_file_path)}")
        except Exception as e:
            self.progress_bar.pack_forget()
            self.update_status(f"❌ Error processing file: {str(e)}", error=True)
    
    def clear_files(self):
        """Clear selected files"""
        self.input_file_path = None
        self.output_file_path = None
        self.input_file_label.configure(text="No file selected", text_color="gray")
        self.output_file_label.configure(text="Output will be saved here", text_color="gray")
        self.update_status("Files cleared")
    
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

