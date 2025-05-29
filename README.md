# Wikimedia OCR Application

This application processes PDF documents using Tesseract OCR engine and provides a web interface for document processing.

## Project Structure
```
wikimedia-ocr/
├── backend/           # Python FastAPI backend
├── frontend/         # React TypeScript frontend
└── README.md
```

## Prerequisites
- Python 3.8+
- Node.js 16+
- Tesseract OCR
- npm or yarn

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Team Member Responsibilities

### Team Member 1 (PDF Processing & OCR)
- PDF page splitting
- OCR processing using Tesseract
- Initial text extraction

### Team Member 2 (Text Processing & Storage)
- Text file management
- Appending processed text
- Final output formatting

## API Documentation
The API documentation will be available at `http://localhost:8000/docs` when the backend server is running. 