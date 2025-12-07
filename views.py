import customtkinter as ctk
from typing import Dict, Any


def create_settings_page_ui(parent, settings_callback, current_settings, settings_widget_ref, settings_ref):
    """Create the settings page UI components"""
    # Hello Settings text
    hello_label = ctk.CTkLabel(
        parent,
        text="Hello Settings",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#4A9EFF"
    )
    hello_label.pack(pady=(20, 10))
    
    # Main frame
    main_frame = ctk.CTkFrame(parent)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
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
    create_setting_widget(
        scroll_frame, 
        "Points to render in % (Huge impact on render speed!):", 
        "points_to_render",     
        current_settings["points_to_render"],
        settings_widget_ref,
        min_value=10.0,
        max_value=100.0,
        step=1.0,
        
    )
    
    
    
    # Output format setting
    output_frame = ctk.CTkFrame(scroll_frame)
    output_frame.pack(fill="x", pady=10)
    
    ctk.CTkLabel(
        output_frame, 
        text="Output Format:",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(anchor="w", padx=10, pady=(10, 5))
    
    output_format = ctk.CTkComboBox(
        output_frame,
        values=[".las", ".txt", ".csv"],
        width=200,
    )
    output_format.set(current_settings["output_format"])
    output_format.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Checkbox settings
    
    
    # Buttons frame
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(fill="x", pady=(10, 10))
    
    return main_frame, output_format, button_frame


def create_setting_widget(parent, label_text, key, default_value, settings_widget_ref,
                         min_value=0, max_value=100, step=1):
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="x", pady=10, padx=10)

    # ustaw wartość startową
    settings_widget_ref[key] = default_value

    label = ctk.CTkLabel(
        frame,
        text=label_text,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    label.pack(anchor="w", padx=10, pady=(10, 5))

    value_frame = ctk.CTkFrame(frame)
    value_frame.pack(fill="x", padx=10, pady=(0, 10))

    value_label = ctk.CTkLabel(
        value_frame,
        text=f"{default_value}",
        font=ctk.CTkFont(size=12),
        width=100
    )
    value_label.pack(side="right", padx=10)

    def onChange(value):
        value_label.configure(text=f"{value:.2f}" if step < 1 else f"{int(value)}")
        settings_widget_ref[key] = float(value)

    slider = ctk.CTkSlider(
        value_frame,
        from_=min_value,
        to=max_value,
        number_of_steps=int((max_value - min_value) / step),
        command=onChange
    )

    slider.set(default_value)
    slider.pack(side="left", fill="x", expand=True, padx=10)


def create_settings_buttons(button_frame, save_command, reset_command, cancel_command):
    """Create settings page buttons"""
    # Save button
    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Save Settings",
        command=save_command,
        width=150,
        height=40,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    save_btn.pack(side="left", padx=10)
    
    # Reset button
    reset_btn = ctk.CTkButton(
        button_frame,
        text="🔄 Reset to Default",
        command=reset_command,
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
        command=cancel_command,
        width=150,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="red",
        hover_color="darkred"
    )
    cancel_btn.pack(side="right", padx=10)


def create_main_app_header(parent):
    """Create the main application header"""
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
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
    
    return header_frame


def create_file_selection_section(parent, browse_input_command, browse_output_command):
    """Create file selection section with input and output file selectors"""
    file_section = ctk.CTkFrame(parent)
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
    
    input_file_label = ctk.CTkLabel(
        input_file_frame,
        text="No file selected",
        font=ctk.CTkFont(size=12),
        text_color="gray",
        anchor="w"
    )
    input_file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    browse_input_btn = ctk.CTkButton(
        input_file_frame,
        text="Browse",
        command=browse_input_command,
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
    
    output_file_label = ctk.CTkLabel(
        output_file_frame,
        text="Output will be saved here",
        font=ctk.CTkFont(size=12),
        text_color="gray",
        anchor="w"
    )
    output_file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    browse_output_btn = ctk.CTkButton(
        output_file_frame,
        text="Choose Location",
        command=browse_output_command,
        width=120,
        height=35,
        font=ctk.CTkFont(size=13, weight="bold")
    )
    browse_output_btn.pack(side="right")
    
    return input_file_label, output_file_label


def create_action_buttons(parent, process_command, settings_command, clear_command):
    """Create action buttons section"""
    button_section = ctk.CTkFrame(parent, fg_color="transparent")
    button_section.pack(fill="x", pady=30, padx=20)
    
    # Process button
    process_btn = ctk.CTkButton(
        button_section,
        text="⚡ Process File",
        command=process_command,
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
        command=settings_command,
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
        command=clear_command,
        width=200,
        height=50,
        font=ctk.CTkFont(size=18, weight="bold"),
        fg_color="#8b2d2d",
        hover_color="#5c1f1f"
    )
    clear_btn.pack(side="right", padx=10)
    
    return button_section


def create_status_section(parent):
    """Create status section with status label and progress bar"""
    status_frame = ctk.CTkFrame(parent)
    status_frame.pack(fill="x", pady=20, padx=20)
    
    status_title = ctk.CTkLabel(
        status_frame,
        text="📊 Status:",
        font=ctk.CTkFont(size=14, weight="bold")
    )
    status_title.pack(anchor="w", padx=15, pady=(15, 5))
    
    status_label = ctk.CTkLabel(
        status_frame,
        text="Ready to process files",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    )
    status_label.pack(anchor="w", padx=15, pady=(0, 15))
    
    # Progress bar (initially hidden)
    progress_bar = ctk.CTkProgressBar(status_frame)
    progress_bar.pack(fill="x", padx=15, pady=(0, 15))
    progress_bar.pack_forget()
    
    return status_label, progress_bar

