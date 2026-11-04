import React from 'react';

interface ForensicLogoProps {
  className?: string;
  size?: number;
  scanning?: boolean;
}

export const ForensicLogo: React.FC<ForensicLogoProps> = ({
  className = "w-16 h-16",
  size = 64,
  scanning = true
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="Video Deepfake Detection Forensic Symbol"
    >
      <defs>
        <linearGradient id="forensicGridGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.8" />
          <stop offset="50%" stopColor="#3b82f6" stopOpacity="0.4" />
          <stop offset="100%" stopColor="#1d4ed8" stopOpacity="0.1" />
        </linearGradient>
        
        <linearGradient id="scanBeam" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#38bdf8" stopOpacity="0" />
          <stop offset="50%" stopColor="#38bdf8" stopOpacity="0.75" />
          <stop offset="100%" stopColor="#38bdf8" stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Frame outer corner crosshairs / target brackets */}
      <path d="M 12 24 L 12 12 L 24 12" stroke="#38bdf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M 88 24 L 88 12 L 76 12" stroke="#38bdf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M 12 76 L 12 88 L 24 88" stroke="#38bdf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M 88 76 L 88 88 L 76 88" stroke="#38bdf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />

      {/* Subtle outer bounding box border */}
      <rect x="18" y="18" width="64" height="64" rx="10" stroke="#1e293b" strokeWidth="1.2" strokeDasharray="3 3" />

      {/* Geometric Facial Contour */}
      <path
        d="M 50 25 C 64 25 72 35 72 50 C 72 65 62 76 50 81 C 38 76 28 65 28 50 C 28 35 36 25 50 25 Z"
        stroke="url(#forensicGridGrad)"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Midline symmetry guide */}
      <line x1="50" y1="28" x2="50" y2="78" stroke="#38bdf8" strokeWidth="0.8" strokeOpacity="0.3" strokeDasharray="2 2" />

      {/* Horizontal eye-level line */}
      <line x1="34" y1="45" x2="66" y2="45" stroke="#38bdf8" strokeWidth="0.8" strokeOpacity="0.25" />

      {/* Eye landmark points & targets */}
      {/* Left Eye */}
      <circle cx="41" cy="45" r="2.5" fill="#38bdf8" fillOpacity="0.9" />
      <circle cx="41" cy="45" r="5" stroke="#38bdf8" strokeWidth="0.75" strokeOpacity="0.4" />
      
      {/* Right Eye */}
      <circle cx="59" cy="45" r="2.5" fill="#38bdf8" fillOpacity="0.9" />
      <circle cx="59" cy="45" r="5" stroke="#38bdf8" strokeWidth="0.75" strokeOpacity="0.4" />

      {/* Nose Landmark Structure */}
      <path d="M 50 42 L 50 56 L 46 58 L 54 58" stroke="#38bdf8" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" strokeOpacity="0.8" />
      <circle cx="50" cy="56" r="1.5" fill="#38bdf8" />

      {/* Mouth / Lips Landmark Arch */}
      <path d="M 42 66 Q 50 64 58 66" stroke="#38bdf8" strokeWidth="1.4" strokeLinecap="round" strokeOpacity="0.85" />
      <path d="M 44 67 Q 50 71 56 67" stroke="#38bdf8" strokeWidth="1.2" strokeLinecap="round" strokeOpacity="0.7" />
      <circle cx="42" cy="66" r="1.2" fill="#38bdf8" />
      <circle cx="58" cy="66" r="1.2" fill="#38bdf8" />

      {/* Chin Landmark point */}
      <circle cx="50" cy="78" r="1.5" fill="#38bdf8" fillOpacity="0.9" />

      {/* Subtle Horizontal Scanning Line */}
      {scanning && (
        <line
          x1="22"
          y1="50"
          x2="78"
          y2="50"
          stroke="url(#scanBeam)"
          strokeWidth="2.5"
          className="animate-pulse"
        />
      )}
    </svg>
  );
};
