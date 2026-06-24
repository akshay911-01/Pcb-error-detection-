import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { UploadComponent } from './components/UploadComponent';
import { ResultComponent } from './components/ResultComponent';
import { uploadImage, downloadReport } from './api';
import type { PredictResponse } from './types';
import { AlertCircle, X } from 'lucide-react';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Optional: keep track of the uploaded file for raw preview if needed,
  // but for now we focus on the resulting processed base64 image.
  // const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleImageSelect = async (file: File) => {
    // setSelectedFile(file);
    setIsLoading(true);
    setError(null);
    setResult(null); // Clear previous
    
    try {
      const data = await uploadImage(file);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during prediction.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    try {
      await downloadReport();
    } catch (err: any) {
      setError(err.message || 'Failed to download report.');
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-200 flex flex-col font-sans">
      <Navbar />

      {/* Main Content Area */}
      <main className="flex-1 p-6 md:p-8 max-w-[1600px] w-full mx-auto">
        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/50 text-red-500 p-4 rounded-xl flex items-start justify-between backdrop-blur-sm">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <p className="text-sm font-medium">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="text-red-500 hover:text-white transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-140px)] min-h-[600px]">
          {/* Left Panel: Upload */}
          <div className="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col">
            <UploadComponent onImageSelect={handleImageSelect} isLoading={isLoading} />
          </div>

          {/* Right Panel: Result */}
          <div className="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col overflow-y-auto">
            <ResultComponent
              result={result}
              isLoading={isLoading}
              onDownloadReport={handleDownloadReport}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
