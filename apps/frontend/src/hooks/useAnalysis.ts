import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function useCreateSession() {
  return useMutation({ mutationFn: () => api.createSession() });
}

export function useUploadDocument(sessionId: string) {
  return useMutation({ mutationFn: (file: File) => api.uploadDocument(sessionId, file) });
}

export function useStartAnalysis() {
  return useMutation({ mutationFn: (sessionId: string) => api.startAnalysis(sessionId) });
}

export function useAnalysisStatus(sessionId: string | undefined, enabled: boolean) {
  return useQuery({
    queryKey: ['analysisStatus', sessionId],
    queryFn: () => api.getAnalysisStatus(sessionId!),
    enabled: !!sessionId && enabled,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === 'complete' || status === 'failed') return false;
      return 2000;
    },
  });
}

export function useAnalysis(sessionId: string | undefined) {
  return useQuery({
    queryKey: ['analysis', sessionId],
    queryFn: () => api.getAnalysis(sessionId!),
    enabled: !!sessionId,
  });
}

export function useMarketData(sessionId: string | undefined) {
  return useQuery({
    queryKey: ['market', sessionId],
    queryFn: () => api.getMarketData(sessionId!),
    enabled: !!sessionId,
  });
}

export function useDeleteSession() {
  return useMutation({ mutationFn: (sessionId: string) => api.deleteSession(sessionId) });
}

export function useExportData() {
  return useMutation({ mutationFn: (sessionId: string) => api.exportSession(sessionId) });
}
