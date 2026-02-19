import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface Props {
  onFilesSelected: (files: File[]) => void;
  isUploading: boolean;
}

export default function DocumentUploader({ onFilesSelected, isUploading }: Props) {
  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted.length > 0) onFilesSelected(accepted);
    },
    [onFilesSelected],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    disabled: isUploading,
    multiple: true,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
        isDragActive
          ? 'border-accent-400 bg-accent-50'
          : isUploading
            ? 'border-gray-200 bg-gray-50 cursor-not-allowed'
            : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
      }`}
    >
      <input {...getInputProps()} />
      <svg
        className="w-12 h-12 mx-auto mb-4 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"
        />
      </svg>
      {isDragActive ? (
        <p className="text-lg font-medium text-accent-500">Drop your PDF files here...</p>
      ) : isUploading ? (
        <p className="text-lg font-medium text-gray-400">Uploading...</p>
      ) : (
        <>
          <p className="text-lg font-medium text-gray-700 mb-1">
            Drag &amp; drop PDF files here
          </p>
          <p className="text-sm text-gray-500">
            or click to browse. Supports koopovereenkomst, energy labels, inspection reports, and
            more.
          </p>
        </>
      )}
    </div>
  );
}
