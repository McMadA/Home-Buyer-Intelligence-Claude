import type { DocumentUploadResponse } from '../../types';

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

interface Props {
  documents: DocumentUploadResponse[];
  onDelete?: (docId: string) => void;
}

export default function UploadProgress({ documents, onDelete }: Props) {
  if (documents.length === 0) return null;

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-gray-700 mb-3">
        Uploaded Documents ({documents.length})
      </h3>
      {documents.map((doc) => (
        <div
          key={doc.id}
          className="flex items-center justify-between bg-white border border-gray-200 rounded-lg px-4 py-3"
        >
          <div className="flex items-center gap-3 min-w-0">
            <svg
              className="w-5 h-5 text-red-500 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M4 4a2 2 0 0 1 2-2h4.586A2 2 0 0 1 12 2.586L15.414 6A2 2 0 0 1 16 7.414V16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4Z"
                clipRule="evenodd"
              />
            </svg>
            <div className="min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{doc.filename}</p>
              <p className="text-xs text-gray-500">
                {formatBytes(doc.file_size_bytes)} &middot; {doc.document_type.replace(/_/g, ' ')}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-green-600 font-medium mr-2">Uploaded</span>
            <a
              href={`/api/v1/sessions/${doc.session_id}/documents/${doc.id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-primary-500 transition-colors p-1"
              title="View document"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.644C3.399 8.049 6.627 6 10 6c3.373 0 6.601 2.049 7.964 5.678.14.373.14.757 0 1.13c-1.363 3.629-4.591 5.678-7.964 5.678-3.373 0-6.601-2.049-7.964-5.678Z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
              </svg>
            </a>
            {onDelete && (
              <button
                onClick={() => onDelete(doc.id)}
                className="text-gray-400 hover:text-red-500 transition-colors p-1"
                title="Delete document"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
