#!/bin/bash
# Script to run GUI in Docker with proper X11 setup for macOS

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - setting up X11 forwarding..."
    
    # Check if XQuartz is running
    if ! pgrep -x "Xquartz" > /dev/null; then
        echo "⚠️  XQuartz is not running. Starting XQuartz..."
        open -a XQuartz
        echo "⏳ Waiting for XQuartz to start (5 seconds)..."
        sleep 5
    fi
    
    # Get the IP address of the host
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
    
    if [ -z "$IP" ]; then
        IP="127.0.0.1"
    fi
    
    # Allow X11 connections
    xhost + $IP 2>/dev/null || xhost + 127.0.0.1
    
    # Set DISPLAY for Docker
    export DISPLAY=$IP:0
    
    echo "✅ X11 forwarding configured: DISPLAY=$DISPLAY"
    echo "🚀 Starting GUI container..."
    
    # Run docker-compose with the GUI service
    docker-compose up gui
else
    # Linux - should work with default setup
    echo "Detected Linux - using default X11 setup..."
    export DISPLAY=${DISPLAY:-:0}
    docker-compose up gui
fi

