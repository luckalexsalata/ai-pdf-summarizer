'use client';

import { useState } from 'react';
import { uploadPDF, SummaryResponse } from '@/services';

interface FileUploadProps {
  onUploadSuccess?: () => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<SummaryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/pdf') {
        setError('Please select a PDF file');
        return;
      }
      setFile(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const response = await uploadPDF(file);
      setResult(response);
      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (err: any) {
      setError(err.message || 'Error uploading file');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
      <h2 className="text-2xl font-semibold mb-4 text-black dark:text-zinc-50">
        Upload PDF
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label 
            htmlFor="file" 
            className="block text-sm font-medium mb-2 text-zinc-700 dark:text-zinc-300"
          >
            Select PDF file (max 50MB)
          </label>
          <input
            id="file"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={uploading}
            className="block w-full text-sm text-zinc-600 dark:text-zinc-400
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-zinc-900 file:text-zinc-50 dark:file:bg-zinc-100 dark:file:text-zinc-900
              hover:file:bg-zinc-800 dark:hover:file:bg-zinc-200
              disabled:opacity-50 disabled:cursor-not-allowed
              cursor-pointer"
          />
        </div>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!file || uploading}
          className="w-full bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 py-2 px-4 rounded-full hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:bg-zinc-400 dark:disabled:bg-zinc-600 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {uploading ? 'Uploading...' : 'Upload and generate summary'}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded">
          <h3 className="font-semibold text-green-800 dark:text-green-300 mb-2">
            Summary for {result.filename}
          </h3>
          <p className="text-green-700 dark:text-green-400 whitespace-pre-wrap">
            {result.summary}
          </p>
          <p className="text-sm text-green-600 dark:text-green-500 mt-2">
            Uploaded: {new Date(result.uploaded_at).toLocaleString('en-US')}
          </p>
        </div>
      )}
    </div>
  );
}
