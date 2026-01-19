/**
 * Type definitions for API responses and entities.
 */

export interface SummaryResponse {
  filename: string;
  summary: string;
  uploaded_at: string;
}

export interface HistoryItem {
  id: string;
  filename: string;
  summary: string;
  uploaded_at: string;
  file_size_mb: number;
}
