/**
 * Documents service for handling PDF uploads and history operations.
 */

import { API_BASE_URL, handleResponse } from './api-client';
import type { SummaryResponse, HistoryItem } from './types';

/**
 * Upload a PDF file and generate AI summary.
 */
export async function uploadPDF(file: File): Promise<SummaryResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  return handleResponse<SummaryResponse>(response);
}

/**
 * Get the last 5 processed documents.
 */
export async function getHistory(): Promise<HistoryItem[]> {
  const response = await fetch(`${API_BASE_URL}/history`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<HistoryItem[]>(response);
}

/**
 * Delete a document by ID.
 */
export async function deleteDocument(docId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/history/${docId}`, {
    method: 'DELETE',
  });

  // handleResponse will handle 204 and errors properly
  await handleResponse<void>(response);
}
