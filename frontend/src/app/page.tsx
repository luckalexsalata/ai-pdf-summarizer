'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import HistoryPreview from '@/components/HistoryPreview';

export default function Home() {
  const [refreshHistory, setRefreshHistory] = useState(0);

  const handleUploadSuccess = () => {
    setRefreshHistory((prev) => prev + 1);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black font-sans">
      <main className="flex min-h-screen w-full max-w-4xl flex-col items-center justify-center py-16 px-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-black dark:text-zinc-50">
          PDF Summary AI
        </h1>
        
        <div className="w-full space-y-8">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
          <HistoryPreview key={refreshHistory} />
        </div>
      </main>
    </div>
  );
}
