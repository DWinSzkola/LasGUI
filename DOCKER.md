# Docker Setup Guide

This guide explains how to run the LAS File Processing API as a Docker container.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t las-processing-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/uploads:/app/uploads \
     -v $(pwd)/outputs:/app/outputs \
     --name las-api \
     las-processing-api
   ```

3. **View logs:**
   ```bash
   docker logs -f las-api
   ```

4. **Stop the container:**
   ```bash
   docker stop las-api
   docker rm las-api
   ```

## API Endpoints

Once the container is running, the API will be available at `http://localhost:8000`

### Available Endpoints:

- **GET /** - Root endpoint with API information
- **GET /health** - Health check endpoint
- **POST /api/process-file** - Process uploaded file
- **POST /api/process-file-local** - Process file using server-side paths
- **POST /api/move-to-downloads** - Move file to downloads folder

### API Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Example Usage

### Process a file via API:

```bash
curl -X POST "http://localhost:8000/api/process-file" \
  -F "file=@yourfile.las" \
  -F "output_format=.las" \
  -F "points_to_render=10.0" \
  --output processed_file.las
```

### Using Python requests:

```python
import requests

url = "http://localhost:8000/api/process-file"
files = {"file": open("input.las", "rb")}
data = {
    "output_format": ".las",
    "points_to_render": 10.0
}

response = requests.post(url, files=files, data=data)
with open("output.las", "wb") as f:
    f.write(response.content)
```

## Volumes

The Docker setup mounts two directories:
- `./uploads` - Temporary storage for uploaded files
- `./outputs` - Storage for processed output files

These directories persist data between container restarts.

## Environment Variables

You can customize the API behavior by setting environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  # Add more variables as needed
```

## Troubleshooting

### Container won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- View container logs: `docker-compose logs`

### Permission issues
- Ensure the `uploads` and `outputs` directories exist and are writable
- On Linux, you may need to adjust permissions: `chmod -R 777 uploads outputs`

### Build errors
- Ensure all dependencies in `requirements.txt` are valid
- Try rebuilding without cache: `docker-compose build --no-cache`

