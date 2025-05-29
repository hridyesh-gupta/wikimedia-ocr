from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from pdf2image import convert_from_path
import os
from typing import List
import tempfile
from PIL import Image
import json
import sys

app = FastAPI(title="Wikimedia OCR API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_tesseract_path():
    # Common Tesseract installation paths
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        '/usr/bin/tesseract',  # Linux
        '/usr/local/bin/tesseract'  # macOS
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise Exception("Tesseract not found. Please install Tesseract OCR and ensure it's in your PATH.")

def get_poppler_path():
    # Common Poppler installation paths for Windows
    possible_paths = [
        r'C:\Program Files\poppler-24.08.0\Library\bin',
        r'C:\Program Files\poppler-24.02.0\Library\bin',
        r'C:\Program Files (x86)\poppler-24.02.0\Library\bin',
        r'C:\poppler-24.02.0\Library\bin',
        # Add more paths if needed
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If not found in common paths, check if it's in system PATH
    if sys.platform.startswith('win'):
        for path in os.environ['PATH'].split(';'):
            if 'poppler' in path.lower():
                return path
    
    raise Exception("Poppler not found. Please install Poppler and ensure it's in your PATH.")

try:
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()
except Exception as e:
    print(f"Warning: {str(e)}")

@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name

        # Get Poppler path
        poppler_path = get_poppler_path()

        # Convert PDF to images
        try:
            images = convert_from_path(temp_pdf_path, poppler_path=poppler_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to convert PDF to images. Make sure Poppler is installed correctly. Error: {str(e)}"
            )
        
        # Process each page
        processed_pages = []
        for i, image in enumerate(images):
            # Perform OCR on the image
            text = pytesseract.image_to_string(image)
            processed_pages.append({
                "page_number": i + 1,
                "text": text
            })

        # Clean up the temporary PDF file
        os.unlink(temp_pdf_path)

        return {
            "status": "success",
            "message": "PDF processed successfully",
            "pages": processed_pages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 