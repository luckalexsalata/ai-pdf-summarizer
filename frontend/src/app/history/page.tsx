'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getHistory, deleteDocument, HistoryItem } from '@/services';

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await getHistory();
      setHistory(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Error loading history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (docId: string) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      setDeleting(docId);
      await deleteDocument(docId);
      // Refresh history after deletion
      await fetchHistory();
    } catch (err: any) {
      alert(err.message || 'Error deleting document');
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black font-sans">
      <main className="flex min-h-screen w-full max-w-4xl flex-col items-center justify-center py-16 px-8">
        <div className="w-full mb-6">
          <Link
            href="/"
            className="text-blue-600 dark:text-blue-400 hover:underline"
          >
            ← Back
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-center mb-8 text-black dark:text-zinc-50">
          Document History
        </h1>

        {loading ? (
          <div className="w-full bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
            <p className="text-zinc-600 dark:text-zinc-400">Loading...</p>
          </div>
        ) : error ? (
          <div className="w-full bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
              {error}
            </div>
          </div>
        ) : history.length === 0 ? (
          <div className="w-full bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
            <p className="text-zinc-600 dark:text-zinc-400 text-center">
              History is empty. Upload your first PDF file!
            </p>
          </div>
        ) : (
          <div className="w-full space-y-4">
            {history.map((item) => (
              <div
                key={item.id}
                className="bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-lg text-black dark:text-zinc-50">
                    {item.filename}
                  </h3>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-zinc-500 dark:text-zinc-400">
                      {item.file_size_mb.toFixed(2)} MB
                    </span>
                    <button
                      onClick={() => handleDelete(item.id)}
                      disabled={deleting === item.id}
                      className="px-3 py-1 text-sm bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded transition-colors"
                    >
                      {deleting === item.id ? 'Deleting...' : 'Delete'}
                    </button>
                  </div>
                </div>
                <p className="text-zinc-600 dark:text-zinc-300 mb-2 whitespace-pre-wrap">
                  {item.summary}
                </p>
                <p className="text-sm text-zinc-400 dark:text-zinc-500">
                  {new Date(item.uploaded_at).toLocaleString('en-US')}
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
