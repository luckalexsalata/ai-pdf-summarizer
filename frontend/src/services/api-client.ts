/**
 * Base API client with common utilities for handling HTTP requests.
 */

const API_BASE_URL = '/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  // 204 No Content has no body - handle first
  if (response.status === 204) {
    return undefined as T;
  }
  
  if (!response.ok) {
    let errorMessage = response.statusText;
    try {
      const text = await response.text();
      if (text) {
        const errorData = JSON.parse(text);
        errorMessage = errorData.detail || errorData.message || errorMessage;
      }
    } catch {
      // If unable to parse JSON, use status text
    }
    throw new Error(errorMessage);
  }
  
  // Check if response has content
  const contentType = response.headers.get('content-type');
  if (!contentType || !contentType.includes('application/json')) {
    return undefined as T;
  }
  
  const text = await response.text();
  if (!text || text.trim() === '') {
    return undefined as T;
  }
  
  try {
    return JSON.parse(text) as T;
  } catch (error) {
    // If JSON parsing fails, return undefined
    return undefined as T;
  }
}

export { API_BASE_URL, handleResponse };
