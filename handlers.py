import customtkinter as ctk
import tkinter.filedialog as filedialog
import os
import requests
from typing import Dict, Any
import threading
import time


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

    if not app_instance.input_file_path:
        app_instance.update_status("❌ Please select an input file first!", error=True)
        return
    
    if not app_instance.output_file_path:
        app_instance.update_status("❌ Please select an output file location first!", error=True)
        return
    
    if not os.path.exists(app_instance.input_file_path):
        app_instance.update_status("❌ Input file does not exist!", error=True)
        return
    
    # Check API health before processing
    is_connected, message = check_api_health(app_instance.api_url)
    if not is_connected:
        app_instance.update_status(f"❌ {message}. Please ensure API is running.", error=True)
        update_api_status_indicator(app_instance)
        return
    
    # Show progress bar
    app_instance.progress_bar.pack(fill="x", padx=15, pady=(0, 15))
    app_instance.progress_bar.set(0)
    
    app_instance.update_status("Processing file...")
    
    # Simulate processing (replace with actual processing logic)
    app_instance.after(100, lambda: simulate_processing(app_instance))


def process_file_via_api(app_instance):
    """Process file via API with progress updates"""
    api_url = getattr(app_instance, 'api_url', 'http://localhost:8000')
    
    try:
        # Update progress bar
        app_instance.progress_bar.set(0.2)
        app_instance.update()
        
        # Read the input file
        with open(app_instance.input_file_path, 'rb') as f:
            files = {'file': (os.path.basename(app_instance.input_file_path), f, 'application/octet-stream')}
            
            # Prepare form data
            data = {
                'output_format': app_instance.current_settings.get('output_format', '.las'),
                'points_to_render': app_instance.current_settings.get('points_to_render', 10.0)
            }
            
            app_instance.progress_bar.set(0.5)
            app_instance.update()
            
            # Make API request
            response = requests.post(
                f'{api_url}/api/process-file',
                files=files,
                data=data,
                timeout=300  # 5 minute timeout for large files
            )
            
            app_instance.progress_bar.set(0.9)
            app_instance.update()
            
            if response.status_code == 200:
                # Save the processed file
                output_dir = os.path.dirname(app_instance.output_file_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                with open(app_instance.output_file_path, 'wb') as out_file:
                    out_file.write(response.content)
                
                app_instance.progress_bar.set(1.0)
                app_instance.update()
                app_instance.progress_bar.pack_forget()
                app_instance.update_status(f"✅ File processed successfully! Saved to: {os.path.basename(app_instance.output_file_path)}")
            else:
                error_msg = response.json().get('detail', f'API error: {response.status_code}')
                app_instance.progress_bar.pack_forget()
                app_instance.update_status(f"❌ {error_msg}", error=True)
                
    except requests.exceptions.ConnectionError:
        app_instance.progress_bar.pack_forget()
        app_instance.update_status("❌ Cannot connect to API server. Is it running?", error=True)
    except requests.exceptions.Timeout:
        app_instance.progress_bar.pack_forget()
        app_instance.update_status("❌ Request timed out. File may be too large.", error=True)
    except FileNotFoundError:
        app_instance.progress_bar.pack_forget()
        app_instance.update_status("❌ Input file not found!", error=True)
    except Exception as e:
        app_instance.progress_bar.pack_forget()
        app_instance.update_status(f"❌ Error processing file: {str(e)}", error=True)


def simulate_processing(app_instance):
    """Process file with progress updates (runs in background thread)"""
    # Run API call in a separate thread to avoid blocking UI
    thread = threading.Thread(target=process_file_via_api, args=(app_instance,))
    thread.daemon = True
    thread.start()


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


def check_api_health(api_url, timeout=2):
    """
    Check if API is available and healthy.
    Returns (is_connected, message)
    """
    try:
        response = requests.get(f'{api_url}/health', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                return True, "API connected"
            else:
                return False, "API unhealthy"
        else:
            return False, f"API error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "API not reachable"
    except requests.exceptions.Timeout:
        return False, "API timeout"
    except Exception as e:
        return False, f"Connection error: {str(e)}"


def update_api_status_indicator(app_instance):
    """Update the API connection status indicator"""
    is_connected, message = check_api_health(app_instance.api_url)
    
    if hasattr(app_instance, 'api_status_label'):
        if is_connected:
            app_instance.api_status_label.configure(
                text="🟢 API Connected",
                text_color="green"
            )
        else:
            app_instance.api_status_label.configure(
                text=f"🔴 {message}",
                text_color="red"
            )
    
    return is_connected


def start_api_health_monitor(app_instance, interval=5):
    """Start periodic API health monitoring"""
    def monitor():
        while True:
            update_api_status_indicator(app_instance)
            time.sleep(interval)
    
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    
    
   
