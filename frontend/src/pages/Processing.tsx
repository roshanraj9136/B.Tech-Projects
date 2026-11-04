import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  ShieldCheck
} from 'lucide-react';
import { api } from '../services/api';
import type { AnalysisStatus, ProcessingStage } from '../types';

export const Processing: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();

  const [statusData, setStatusData] = useState<AnalysisStatus | null>(null);
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!analysisId) return;

    let timer: any = null;
    let pollInterval: any = null;

    // Elapsed timer
    const startTime = Date.now();
    timer = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    // Poll status from FastAPI backend
    const checkStatus = async () => {
      try {
        const data = await api.getAnalysisStatus(analysisId);
        setStatusData(data);

        if (data.status === 'completed') {
          clearInterval(pollInterval);
          clearInterval(timer);
          setTimeout(() => {
            navigate(`/results/${analysisId}`);
          }, 800);
        } else if (data.status === 'failed') {
          clearInterval(pollInterval);
          clearInterval(timer);
          setError(data.error_message || 'Video analysis encountered an unexpected error.');
        }
      } catch (err: any) {
        console.error('Polling error:', err);
      }
    };

    checkStatus();
    pollInterval = setInterval(checkStatus, 1500);

    return () => {
      clearInterval(timer);
      clearInterval(pollInterval);
    };
  }, [analysisId, navigate]);

  const stages: ProcessingStage[] = statusData?.stages || [
    { id: 'video_validation', name: 'Video validation & integrity check', status: 'completed', progress: 100 },
    { id: 'frame_extraction', name: 'Frame extraction & temporal indexing', status: 'in_progress', progress: 30 },
    { id: 'face_detection', name: 'Face detection & 68 landmark extraction', status: 'pending', progress: 0 },
    { id: 'quality_assessment', name: 'Video quality & blur variance assessment', status: 'pending', progress: 0 },
    { id: 'dfd_fcg_inference', name: 'DFD-FCG spatial-temporal neural inference', status: 'pending', progress: 0 },
    { id: 'region_attribution', name: '16×16 patch & region attribution', status: 'pending', progress: 0 },
    { id: 'result_aggregation', name: 'Forensic evidence synthesis & PDF report', status: 'pending', progress: 0 },
  ];

  const overallProgress = statusData?.progress || 15;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono font-medium mb-3">
          <Activity className="w-3.5 h-3.5 animate-pulse" />
          <span>Active Forensic Pipeline</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
          Analyzing Video Deepfake Evidence
        </h1>
        <p className="text-xs text-slate-400 mt-2 font-mono">
          Analysis ID: <span className="text-slate-300">{analysisId}</span> · Elapsed: {elapsedTime}s
        </p>
      </div>

      {/* Main Status Container */}
      <div className="p-6 sm:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-xs font-mono text-slate-300 mb-2">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-ping" />
              <span>Overall Progress</span>
            </span>
            <span className="font-bold text-blue-400">{overallProgress}%</span>
          </div>
          <div className="w-full bg-slate-950 rounded-full h-3 border border-slate-800 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-600 to-indigo-500 h-3 rounded-full transition-all duration-500 shadow-sm"
              style={{ width: `${overallProgress}%` }}
            />
          </div>
        </div>

        {/* Stages Checklist */}
        <div className="space-y-3 mb-8">
          {stages.map((st, idx) => {
            const isCompleted = st.status === 'completed';
            const isInProgress = st.status === 'in_progress';
            const isFailed = st.status === 'failed';

            return (
              <div
                key={st.id}
                className={`p-3.5 rounded-xl border flex items-center justify-between transition-colors ${
                  isInProgress
                    ? 'bg-blue-950/20 border-blue-500/50 shadow-sm'
                    : isCompleted
                    ? 'bg-slate-950/50 border-slate-800/80'
                    : 'bg-slate-950/20 border-slate-900 text-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-mono ${
                      isCompleted
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : isInProgress
                        ? 'bg-blue-500/20 text-blue-400 border border-blue-500/40 animate-pulse'
                        : isFailed
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : 'bg-slate-800 text-slate-500'
                    }`}
                  >
                    {isCompleted ? <CheckCircle2 className="w-3.5 h-3.5" /> : idx + 1}
                  </div>
                  <div>
                    <span
                      className={`text-xs font-medium block ${
                        isInProgress
                          ? 'text-blue-300 font-semibold'
                          : isCompleted
                          ? 'text-slate-200'
                          : 'text-slate-500'
                      }`}
                    >
                      {st.name}
                    </span>
                    {st.message && isInProgress && (
                      <span className="text-[11px] text-slate-400 font-mono block">{st.message}</span>
                    )}
                  </div>
                </div>

                <div className="text-right text-[11px] font-mono">
                  {isCompleted && <span className="text-emerald-400">Done</span>}
                  {isInProgress && <span className="text-blue-400 animate-pulse">Processing...</span>}
                  {st.status === 'pending' && <span className="text-slate-600">Pending</span>}
                  {isFailed && <span className="text-rose-400">Failed</span>}
                </div>
              </div>
            );
          })}
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs mb-6 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold mb-1">Analysis Failed</p>
              <p className="text-rose-400/90 leading-relaxed mb-3">{error}</p>
              <Link
                to="/upload"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-medium text-xs transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Try Another Video</span>
              </Link>
            </div>
          </div>
        )}

        {/* Information Callout */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Exact float64 Shapley decomposition · Zero residual term</span>
          </div>
          <span className="font-mono text-[11px] text-slate-500 hidden sm:inline">DFD-FCG CVPR 2025</span>
        </div>
      </div>
    </div>
  );
};
