import type {
  SessionResponse,
  DocumentUploadResponse,
  DocumentListResponse,
  AnalysisResponse,
  AnalysisStatusResponse,
  MarketDataResponse,
} from '../types';

const BASE = '';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    ...options,
    headers: {
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || body.message || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  createSession: () => request<SessionResponse>('/api/v1/sessions', { method: 'POST' }),

  uploadDocument: async (sessionId: string, file: File): Promise<DocumentUploadResponse> => {
    const form = new FormData();
    form.append('file', file);
    return request<DocumentUploadResponse>(`/api/v1/sessions/${sessionId}/documents`, {
      method: 'POST',
      body: form,
    });
  },

  listDocuments: (sessionId: string) =>
    request<DocumentListResponse>(`/api/v1/sessions/${sessionId}/documents`),

  deleteDocument: (sessionId: string, docId: string) =>
    request<void>(`/api/v1/sessions/${sessionId}/documents/${docId}`, { method: 'DELETE' }),

  startAnalysis: (sessionId: string) =>
    request<{ session_id: string; analysis_id: string; status: string }>(
      `/api/v1/sessions/${sessionId}/analyze`,
      { method: 'POST' },
    ),

  getAnalysisStatus: (sessionId: string) =>
    request<AnalysisStatusResponse>(`/api/v1/sessions/${sessionId}/analysis/status`),

  getAnalysis: (sessionId: string) =>
    request<AnalysisResponse>(`/api/v1/sessions/${sessionId}/analysis`),

  getMarketData: (sessionId: string) =>
    request<MarketDataResponse>(`/api/v1/sessions/${sessionId}/market`),

  deleteSession: (sessionId: string) =>
    request<{ message: string }>(`/api/v1/sessions/${sessionId}`, { method: 'DELETE' }),

  exportSession: (sessionId: string) =>
    request<Record<string, unknown>>(`/api/v1/sessions/${sessionId}/export`),
};
