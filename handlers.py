import customtkinter as ctk
import tkinter.filedialog as filedialog
import os
from typing import Dict, Any


def handle_browse_input_file(app_instance):
    """Handle input file browsing"""
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
        app_instance.input_file_path = file_path
        filename = os.path.basename(file_path)
        app_instance.input_file_label.configure(
            text=filename,
            text_color="white"
        )
        app_instance.update_status(f"Input file selected: {filename}")


def handle_browse_output_file(app_instance):
    """Handle output file location selection"""
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
        app_instance.output_file_path = file_path
        filename = os.path.basename(file_path)
        app_instance.output_file_label.configure(
            text=filename,
            text_color="white"
        )
        app_instance.update_status(f"Output location set: {filename}")


def handle_process_file(app_instance):
    """Handle file processing"""
    if not app_instance.input_file_path:
        app_instance.update_status("❌ Please select an input file first!", error=True)
        return
    
    if not app_instance.output_file_path:
        app_instance.update_status("❌ Please select an output file location first!", error=True)
        return
    
    if not os.path.exists(app_instance.input_file_path):
        app_instance.update_status("❌ Input file does not exist!", error=True)
        return
    
    # Show progress bar
    app_instance.progress_bar.pack(fill="x", padx=15, pady=(0, 15))
    app_instance.progress_bar.set(0)
    
    app_instance.update_status("Processing file...")
    
    # Simulate processing (replace with actual processing logic)
    app_instance.after(100, lambda: simulate_processing(app_instance))


def simulate_processing(app_instance):
    """Simulate file processing with progress updates"""
    # This is a simulation - replace with your actual processing logic
    steps = 10
    for i in range(steps + 1):
        progress = i / steps
        app_instance.progress_bar.set(progress)
        app_instance.update()
        app_instance.after(200)  # Simulate work
    
    # Here you would call your actual processing function
    # For example: process_las_file(app_instance.input_file_path, app_instance.output_file_path, app_instance.current_settings)
    
    try:
        # Example: Copy file as a placeholder (replace with actual processing)
        import shutil
        shutil.copy2(app_instance.input_file_path, app_instance.output_file_path)
        
        app_instance.progress_bar.pack_forget()
        app_instance.update_status(f"✅ File processed successfully! Saved to: {os.path.basename(app_instance.output_file_path)}")
    except Exception as e:
        app_instance.progress_bar.pack_forget()
        app_instance.update_status(f"❌ Error processing file: {str(e)}", error=True)


def handle_clear_files(app_instance):
    """Handle clearing selected files"""
    app_instance.input_file_path = None
    app_instance.output_file_path = None
    app_instance.input_file_label.configure(text="No file selected", text_color="gray")
    app_instance.output_file_label.configure(text="Output will be saved here", text_color="gray")
    app_instance.update_status("Files cleared")


def handle_open_settings(app_instance):
    """Handle opening settings window"""
    # Import here to avoid circular import
    from settings_view import SettingsPage
    settings_window = SettingsPage(app_instance, app_instance.on_settings_saved, app_instance.current_settings)
    settings_window.focus()


def handle_save_settings(settings_page_instance):
    """Handle saving settings"""
    for key, widget_data in settings_page_instance.settings.items():
        if key == "output_format":
            settings_page_instance.settings[key] = settings_page_instance.output_format.get()
        elif key == "points_to_render":
            settings_page_instance.settings[key] = settings_page_instance.settingsWidget["points_to_render"]
    
    print(settings_page_instance.settings)
    # Call callback with settings
    if settings_page_instance.settings_callback:
        settings_page_instance.settings_callback(settings_page_instance.settings)
    
    # Show success message
    success_label = ctk.CTkLabel(
        settings_page_instance,
        text="✅ Settings saved successfully!",
        font=ctk.CTkFont(size=12),
        fg_color="green",
        corner_radius=5
    )
    success_label.place(relx=0.5, rely=0.95, anchor="center")
    settings_page_instance.after(2000, success_label.destroy)


def handle_reset_settings(settings_page_instance):
    settings_page_instance.settings_callback({
            "output_format": ".las",
            "points_to_render": 10.0
        })
    
    
   
