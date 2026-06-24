import React from 'react';
import { Eye, Download, AlertTriangle, CheckCircle, BarChart } from 'lucide-react';
import type { PredictResponse } from '../types';

interface ResultComponentProps {
  result: PredictResponse | null;
  isLoading: boolean;
  onDownloadReport: () => void;
}

export const ResultComponent: React.FC<ResultComponentProps> = ({ result, isLoading, onDownloadReport }) => {
  if (isLoading) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-[#0d131f] rounded-xl border border-gray-800">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-400 font-medium animate-pulse">Processing image...</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-[#0d131f] border border-gray-800 rounded-xl">
        <div className="p-4 bg-gray-800/50 rounded-2xl mb-4">
          <Eye className="w-8 h-8 text-gray-500" />
        </div>
        <p className="text-gray-400 font-medium">No results yet</p>
        <p className="text-gray-600 text-sm mt-1">Upload a PCB image to start detection</p>
      </div>
    );
  }

  const { detections, image } = result;
  const totalDefects = detections.reduce((acc, curr) => acc + curr.count, 0);
  const isHealthy = totalDefects === 0;

  let mostFrequentDefect = '';
  if (detections.length > 0) {
    mostFrequentDefect = detections.reduce((prev, current) => (prev.count > current.count) ? prev : current).class;
  }

  return (
    <div className="h-full flex flex-col gap-4">
      {/* Image Preview Container */}
      <div className="bg-[#0d131f] border border-gray-800 rounded-xl flex-1 flex flex-col p-4 overflow-hidden relative">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-semibold text-white flex items-center gap-2">
            <Eye className="w-5 h-5 text-blue-500" />
            Detection Result
          </h3>
          <button
            onClick={onDownloadReport}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
          >
            <Download className="w-4 h-4" />
            Generate Report
          </button>
        </div>
        <div className="flex-1 rounded-lg overflow-hidden bg-black/40 flex items-center justify-center border border-gray-800/50">
          <img
            src={`data:image/jpeg;base64,${image}`}
            alt="Processed PCB"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>

      {/* Stats Container */}
      <div className="bg-[#0B0F19] rounded-xl grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status */}
        <div className="bg-[#111827] border border-gray-800 p-4 rounded-xl flex items-center gap-4">
          <div className={`p-3 rounded-lg ${isHealthy ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
            {isHealthy ? <CheckCircle className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
          </div>
          <div>
            <p className="text-gray-400 text-xs uppercase font-semibold tracking-wider">Status</p>
            <p className={`font-bold text-lg ${isHealthy ? 'text-green-500' : 'text-red-500'}`}>
              {isHealthy ? 'Passed' : 'Defective'}
            </p>
          </div>
        </div>

        {/* Total Defects */}
        <div className="bg-[#111827] border border-gray-800 p-4 rounded-xl flex items-center gap-4">
          <div className="p-3 rounded-lg bg-blue-500/10 text-blue-500">
            <BarChart className="w-6 h-6" />
          </div>
          <div>
            <p className="text-gray-400 text-xs uppercase font-semibold tracking-wider">Total Defects</p>
            <p className="font-bold text-lg text-white">{totalDefects}</p>
          </div>
        </div>

        {/* Breakdown */}
        <div className="bg-[#111827] border border-gray-800 p-4 rounded-xl flex flex-col justify-center">
          <p className="text-gray-400 text-xs uppercase font-semibold tracking-wider mb-2">Defect Types</p>
          {detections.length === 0 ? (
            <p className="text-gray-500 text-sm">None detected</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {detections.map((d, idx) => (
                <span
                  key={idx}
                  className={`px-2 py-1 rounded text-xs font-medium border ${
                    d.class === mostFrequentDefect
                      ? 'bg-red-500/20 border-red-500/50 text-red-400'
                      : 'bg-gray-800 border-gray-600 text-gray-300'
                  }`}
                  title={d.class === mostFrequentDefect ? 'Most frequent' : ''}
                >
                  {d.class}: {d.count}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
