import React, { useState } from 'react';
import './App.css';

interface ProcessedPage {
  page_number: number;
  text: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<ProcessedPage[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setProcessing(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/process-pdf', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process PDF');
      }

      const data = await response.json();
      setResult(data.pages);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Wikimedia OCR Application</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <div className="upload-section">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={processing}
            />
            <button type="submit" disabled={!file || processing}>
              {processing ? 'Processing...' : 'Process PDF'}
            </button>
          </div>
        </form>

        {error && <div className="error">{error}</div>}

        {result.length > 0 && (
          <div className="results">
            <h2>Processed Pages</h2>
            {result.map((page) => (
              <div key={page.page_number} className="page-result">
                <h3>Page {page.page_number}</h3>
                <pre>{page.text}</pre>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
