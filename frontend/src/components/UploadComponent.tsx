import React, { useCallback, useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';

interface UploadComponentProps {
  onImageSelect: (file: File) => void;
  isLoading: boolean;
}

export const UploadComponent: React.FC<UploadComponentProps> = ({ onImageSelect, isLoading }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [localPreview, setLocalPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!isLoading) setIsDragOver(true);
  }, [isLoading]);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (isLoading) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        setLocalPreview(URL.createObjectURL(file));
        onImageSelect(file);
      }
    }
  }, [onImageSelect, isLoading]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setLocalPreview(URL.createObjectURL(file));
      onImageSelect(file);
    }
  };

  return (
    <div className="flex flex-col gap-4 h-full">
      <div className="flex items-center gap-2 text-blue-400 font-medium">
        <UploadCloud className="w-5 h-5" />
        <span>Upload PCB Image</span>
      </div>
      <div
        className={`flex-1 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all bg-[#0d131f] relative overflow-hidden group
          ${isDragOver ? 'border-blue-500 bg-[#162136]' : 'border-gray-700 hover:border-gray-500'}
          ${isLoading ? 'opacity-80 cursor-not-allowed' : 'cursor-pointer'}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept="image/jpeg, image/png, image/jpg"
          onChange={handleFileChange}
          disabled={isLoading}
        />
        
        {localPreview ? (
          <>
            <img src={localPreview} alt="Preview" className={`absolute inset-0 w-full h-full object-contain p-2 ${isLoading ? 'opacity-40 blur-sm' : 'opacity-80 group-hover:opacity-100 transition-opacity'}`} />
            {isLoading && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/40 z-10">
                <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
                <p className="text-white font-medium drop-shadow-md">Uploading...</p>
              </div>
            )}
            {!isLoading && (
               <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity z-10">
                 <p className="text-white font-medium flex items-center gap-2 drop-shadow-md"><UploadCloud className="w-5 h-5" /> Click or drop to replace</p>
               </div>
            )}
          </>
        ) : (
          <>
            <div className="p-4 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl mb-6 shadow-lg shadow-blue-500/20">
              <UploadCloud className="w-8 h-8 text-white" />
            </div>
            <p className="text-white font-medium mb-2">Drag & drop your PCB image</p>
            <p className="text-gray-500 text-sm">or click to browse - JPG, PNG</p>
          </>
        )}
      </div>
    </div>
  );
};
