"""
FastAPI server exposing Logic.py functions as REST API endpoints
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import tempfile
import shutil
from pathlib import Path
import Logic

app = FastAPI(
    title="LAS File Processing API",
    description="API for processing LAS files and other file operations",
    version="1.0.0"
)

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads and outputs directories if they don't exist
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "LAS File Processing API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/process-file")
async def process_file(
    file: UploadFile = File(...),
    output_format: str = Form(".las"),
    points_to_render: float = Form(10.0)
):
    """
    Process a file (LAS, CSV, TXT) with specified settings.
    
    - **file**: The input file to process
    - **output_format**: Output format (.las, .txt, .csv)
    - **points_to_render**: Percentage of points to render (10.0-100.0)
    """
    try:
        # Validate output format
        if output_format not in [".las", ".txt", ".csv"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid output_format. Must be .las, .txt, or .csv"
            )
        
        # Validate points_to_render
        if not 10.0 <= points_to_render <= 100.0:
            raise HTTPException(
                status_code=400,
                detail="points_to_render must be between 10.0 and 100.0"
            )
        
        # Save uploaded file temporarily
        input_path = UPLOAD_DIR / file.filename
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Generate output filename
        base_name = Path(file.filename).stem
        output_filename = f"{base_name}_processed{output_format}"
        output_path = OUTPUT_DIR / output_filename
        
        # Process the file
        settings = {
            "output_format": output_format,
            "points_to_render": points_to_render
        }
        
        success, message = Logic.process_file(
            str(input_path),
            str(output_path),
            settings
        )
        
        if not success:
            # Clean up input file
            if input_path.exists():
                input_path.unlink()
            raise HTTPException(status_code=500, detail=message)
        
        # Return the processed file
        if output_path.exists():
            return FileResponse(
                path=str(output_path),
                filename=output_filename,
                media_type="application/octet-stream"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Processing completed but output file not found"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Clean up input file after processing
        if 'input_path' in locals() and input_path.exists():
            try:
                input_path.unlink()
            except:
                pass


@app.post("/api/process-file-local")
async def process_file_local(
    input_path: str = Form(...),
    output_path: str = Form(...),
    output_format: str = Form(".las"),
    points_to_render: float = Form(10.0)
):
    """
    Process a file using local file paths (for server-side files).
    
    - **input_path**: Absolute path to input file on server
    - **output_path**: Absolute path where output should be saved
    - **output_format**: Output format (.las, .txt, .csv)
    - **points_to_render**: Percentage of points to render (10.0-100.0)
    """
    try:
        # Validate output format
        if output_format not in [".las", ".txt", ".csv"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid output_format. Must be .las, .txt, or .csv"
            )
        
        # Validate points_to_render
        if not 10.0 <= points_to_render <= 100.0:
            raise HTTPException(
                status_code=400,
                detail="points_to_render must be between 10.0 and 100.0"
            )
        
        # Process the file
        settings = {
            "output_format": output_format,
            "points_to_render": points_to_render
        }
        
        success, message = Logic.process_file(
            input_path,
            output_path,
            settings
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=message)
        
        return {
            "success": True,
            "message": message,
            "output_path": output_path
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/move-to-downloads")
async def move_to_downloads(file_path: str = Form(...)):
    """
    Move a file to the Downloads folder.
    
    - **file_path**: Absolute path to the file to move
    """
    try:
        success, message = Logic.move_to_downloads(file_path)
        
        if not success:
            raise HTTPException(status_code=500, detail=message)
        
        return {
            "success": True,
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

