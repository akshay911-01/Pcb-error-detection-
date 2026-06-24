import type { PredictResponse } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const uploadImage = async (file: File): Promise<PredictResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorMessage = 'Failed to process image';
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (_) {
      // Ignored
    }
    throw new Error(errorMessage);
  }

  return await response.json();
};

export const downloadReport = async (): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/report`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error('Failed to generate report');
  }

  // Handle PDF file download
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `pcb_report_${new Date().toISOString().split('T')[0]}.pdf`;
  document.body.appendChild(a);
  a.click();
  
  // Clean up
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};
