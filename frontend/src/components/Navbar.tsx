import React from 'react';
import { Cpu } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <nav className="border-b border-gray-800 bg-[#0B0F19] text-white px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="bg-blue-600 p-2 rounded-lg">
          <Cpu className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="font-semibold text-lg leading-tight tracking-wide">PCB Defect Detection</h1>
          <p className="text-gray-400 text-xs">AI Powered Quality Inspection</p>
        </div>
      </div>
      <div className="flex items-center gap-2 text-gray-400 text-sm">
        <span className="w-2 h-2 rounded-full border border-gray-500 flex items-center justify-center"></span>
        v2.4.1
      </div>
    </nav>
  );
};
