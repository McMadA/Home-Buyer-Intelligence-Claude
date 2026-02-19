import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DocumentUploader from '../components/upload/DocumentUploader';
import UploadProgress from '../components/upload/UploadProgress';
import { api } from '../api/client';
import type { DocumentUploadResponse } from '../types';

export default function UploadPage() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [documents, setDocuments] = useState<DocumentUploadResponse[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.createSession().then((s) => setSessionId(s.session_id)).catch(() => setError('Failed to create session'));
  }, []);

  const handleFilesSelected = async (files: File[]) => {
    if (!sessionId) return;
    setIsUploading(true);
    setError(null);

    for (const file of files) {
      try {
        const doc = await api.uploadDocument(sessionId, file);
        setDocuments((prev) => [...prev, doc]);
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Upload failed');
      }
    }
    setIsUploading(false);
  };

  const handleDelete = async (docId: string) => {
    if (!sessionId) return;
    try {
      await api.deleteDocument(sessionId, docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  const handleAnalyze = async () => {
    if (!sessionId || documents.length === 0) return;
    setIsAnalyzing(true);
    try {
      await api.startAnalysis(sessionId);
      navigate(`/analysis/${sessionId}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start analysis');
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-primary-500 mb-2">Upload Documents</h1>
      <p className="text-gray-600 mb-8">
        Upload your Dutch property documents (PDF) to get started with the analysis.
      </p>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <div className="space-y-6">
        <DocumentUploader onFilesSelected={handleFilesSelected} isUploading={isUploading} />
        <UploadProgress documents={documents} onDelete={handleDelete} />

        {documents.length > 0 && (
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Starting Analysis...
              </span>
            ) : (
              `Analyze ${documents.length} Document${documents.length > 1 ? 's' : ''}`
            )}
          </button>
        )}
      </div>
    </div>
  );
}
