# Docker GUI Setup Guide

This guide explains how to run the LAS File Processing GUI application in a Docker container.

## Prerequisites

### For macOS:
1. Install **XQuartz** (X11 server for macOS):
   ```bash
   brew install --cask xquartz
   ```
2. Restart your Mac or log out and back in
3. Enable X11 forwarding:
   ```bash
   xhost +localhost
   # Or for more security:
   xhost + 127.0.0.1
   ```

### For Linux:
X11 should work out of the box. Just ensure your DISPLAY variable is set:
```bash
echo $DISPLAY
# Should show something like :0 or :1
```

## Running the GUI Application

### Option 1: Using the Helper Script (Recommended for macOS)

The easiest way to run the GUI on macOS:

```bash
./run-gui-docker.sh
```

This script will:
- Check if XQuartz is running and start it if needed
- Configure X11 forwarding automatically
- Set the correct DISPLAY variable
- Start the GUI container

### Option 2: Using Docker Compose Manually

1. **For macOS - Set up X11:**
   ```bash
   # Start XQuartz if not running
   open -a XQuartz
   
   # Get your IP address
   IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
   
   # Allow X11 connections
   xhost + $IP
   
   # Set DISPLAY
   export DISPLAY=$IP:0
   ```

2. **Run the GUI container:**
   ```bash
   docker-compose up gui
   ```

3. **For Linux:**
   ```bash
   export DISPLAY=:0
   xhost +local:docker
   docker-compose up gui
   ```

### Option 2: Using Docker directly

**For macOS:**
```bash
export DISPLAY=:0
xhost +localhost

docker build -f Dockerfile.gui -t las-gui .
docker run -it --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd):/app/data:ro \
  --network host \
  las-gui
```

**For Linux:**
```bash
xhost +local:docker

docker build -f Dockerfile.gui -t las-gui .
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd):/app/data:ro \
  --network host \
  las-gui
```

## Running Both API and GUI

To run both the API server and GUI application:

```bash
# Start both services
docker-compose up

# Or start them separately
docker-compose up api    # API server on port 8000
docker-compose up gui    # GUI application (connects to API automatically)
```

**Important:** The GUI application now communicates with the API service. When running in Docker, the GUI automatically connects to the API via the Docker network at `http://api:8000`. If running the GUI locally (not in Docker), it will connect to `http://localhost:8000` by default.

You can override the API URL by setting the `API_URL` environment variable:
```bash
export API_URL=http://your-api-host:8000
docker-compose up gui
```

## Troubleshooting

### GUI window doesn't appear

1. **Check X11 is running (macOS):**
   ```bash
   # Check if XQuartz is running
   ps aux | grep -i xquartz
   
   # If not, start it:
   open -a XQuartz
   ```

2. **Verify DISPLAY variable:**
   ```bash
   echo $DISPLAY
   # Should show :0 or localhost:0
   ```

3. **Check xhost permissions:**
   ```bash
   xhost
   # Should show localhost or 127.0.0.1 in the list
   ```

4. **View container logs:**
   ```bash
   docker-compose logs gui
   ```

### Permission denied errors

On Linux, you might need to:
```bash
xhost +local:docker
```

Or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# Then log out and back in
```

### Alternative: Use VNC (Headless GUI)

If X11 forwarding doesn't work, you can use VNC:

1. **Modify Dockerfile.gui** to include a VNC server
2. **Access via VNC client** on port 5900

For a VNC-based setup, you would need to:
- Install `tigervnc-standalone-server` in the Dockerfile
- Expose port 5900
- Connect using a VNC client

## File Access

The GUI container mounts:
- `./data:/app/user_data` - For input/output files (read-write)
- `.:/app/data` - Current directory (read-only)

Make sure to place your files in the `./data` directory or adjust the volume mounts in `docker-compose.yml`.

## Notes

- The GUI container uses `network_mode: host` for X11 forwarding
- The GUI app doesn't auto-restart (unlike the API) since it's user-controlled
- On macOS, you may need to allow XQuartz through your firewall

