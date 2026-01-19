'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getHistory, HistoryItem } from '@/services';

export default function HistoryPreview() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      // Ignore errors in preview
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-black dark:text-zinc-50">
            Recent Documents
          </h2>
          <Link
            href="/history"
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            All →
          </Link>
        </div>
        <p className="text-zinc-600 dark:text-zinc-400">Loading...</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-black rounded-lg shadow-lg p-6 border border-zinc-200 dark:border-zinc-800">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-black dark:text-zinc-50">
          Recent Documents
        </h2>
        {history.length > 0 && (
          <Link
            href="/history"
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            All →
          </Link>
        )}
      </div>
      
      {history.length === 0 ? (
        <p className="text-zinc-600 dark:text-zinc-400">
          History is empty. Upload your first PDF file!
        </p>
      ) : (
        <div className="space-y-3">
          {history.map((item) => (
            <Link
              key={item.id}
              href="/history"
              className="block border border-zinc-200 dark:border-zinc-800 rounded-lg p-4 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition"
            >
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-semibold text-base text-black dark:text-zinc-50 truncate">
                  {item.filename}
                </h3>
                <span className="text-xs text-zinc-500 dark:text-zinc-400 ml-2 flex-shrink-0">
                  {item.file_size_mb.toFixed(2)} MB
                </span>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-300 line-clamp-2">
                {item.summary}
              </p>
              <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">
                {new Date(item.uploaded_at).toLocaleString('en-US')}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
