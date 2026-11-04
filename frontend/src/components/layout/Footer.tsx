import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-900 bg-slate-950 py-6 text-slate-500 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p className="font-mono">
          DFD-FCG Explainable Video Deepfake Detection · CVPR 2025
        </p>
        <p className="text-slate-600 text-[11px]">
          Probabilistic Forensic Instrument · Evaluated on FaceForensics++ Benchmark
        </p>
      </div>
    </footer>
  );
};
