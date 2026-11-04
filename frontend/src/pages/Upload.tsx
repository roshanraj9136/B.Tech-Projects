import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  FileVideo,
  X,
  AlertCircle,
  Film,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap
} from 'lucide-react';
import { api } from '../services/api';
import type { SampleVideo } from '../types';

export const Upload: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [videoPreviewUrl, setVideoPreviewUrl] = useState<string | null>(null);
  const [videoDimensions, setVideoDimensions] = useState<{ width: number; height: number; duration: number } | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [samples, setSamples] = useState<SampleVideo[]>([]);
  const [selectedSampleKey, setSelectedSampleKey] = useState<string | null>(null);

  // Load sample videos
  useEffect(() => {
    api.getSampleVideos()
      .then((data) => {
        setSamples(data.samples);
      })
      .catch((err) => {
        console.error('Failed to load sample videos:', err);
      });
  }, []);

  // Handle file selection
  const handleFileChange = (file: File) => {
    setErrorMessage(null);
    setSelectedSampleKey(null);

    // Validate extension
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    const validExts = ['.mp4', '.mov', '.avi', '.mkv'];
    if (!validExts.includes(ext)) {
      setErrorMessage(`Unsupported format '${ext}'. Allowed: MP4, MOV, AVI, MKV.`);
      return;
    }

    // Validate size (200MB max)
    const maxSize = 200 * 1024 * 1024;
    if (file.size > maxSize) {
      setErrorMessage('File size exceeds the 200 MB limit.');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setVideoPreviewUrl(url);

    // Extract video dimensions via temporary video element
    const tempVideo = document.createElement('video');
    tempVideo.preload = 'metadata';
    tempVideo.src = url;
    tempVideo.onloadedmetadata = () => {
      setVideoDimensions({
        width: tempVideo.videoWidth,
        height: tempVideo.videoHeight,
        duration: tempVideo.duration,
      });
    };
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleSelectSample = (sample: SampleVideo) => {
    setErrorMessage(null);
    setSelectedFile(null);
    setSelectedSampleKey(sample.sample_key);
    setVideoPreviewUrl(sample.url);
    setVideoDimensions(null);
  };

  const handleClearSelection = () => {
    setSelectedFile(null);
    setSelectedSampleKey(null);
    if (videoPreviewUrl && !selectedSampleKey) {
      URL.revokeObjectURL(videoPreviewUrl);
    }
    setVideoPreviewUrl(null);
    setVideoDimensions(null);
    setErrorMessage(null);
    setUploadProgress(0);
  };

  // Submit and start analysis
  const handleStartAnalysis = async () => {
    if (!selectedFile && !selectedSampleKey) {
      setErrorMessage('Please select a video file or pick a benchmark sample.');
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);

    try {
      let videoId = '';
      if (selectedSampleKey) {
        // Benchmark sample
        const res = await api.selectSample(selectedSampleKey);
        videoId = res.video.video_id;
        const analysisRes = await api.startAnalysis(videoId, selectedSampleKey);
        navigate(`/processing/${analysisRes.analysis_id}`);
      } else if (selectedFile) {
        // Upload user file
        const res = await api.uploadVideo(selectedFile, (percent) => {
          setUploadProgress(percent);
        });
        videoId = res.video.video_id;
        const analysisRes = await api.startAnalysis(videoId);
        navigate(`/processing/${analysisRes.analysis_id}`);
      }
    } catch (err: any) {
      console.error(err);
      setIsUploading(false);
      setErrorMessage(err.response?.data?.detail || err.message || 'Analysis initiation failed.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="max-w-3xl mx-auto text-center mb-10">
        <h1 className="text-3xl font-extrabold text-slate-100 tracking-tight sm:text-4xl mb-3">
          Video Forensics Ingestion
        </h1>
        <p className="text-sm text-slate-400">
          Upload an MP4, MOV, AVI, or MKV video for explainable deepfake inspection, or evaluate our preloaded
          FaceForensics++ research samples.
        </p>
      </div>

      <div className="max-w-4xl mx-auto grid grid-cols-1 gap-8">
        {/* Benchmark Research Samples Picker */}
        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <h3 className="text-sm font-bold text-slate-200">
                FaceForensics++ Research Benchmark Samples
              </h3>
            </div>
            <span className="text-[11px] font-mono text-slate-500">1-Click Instant Evaluation</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {samples.map((s) => {
              const isSelected = selectedSampleKey === s.sample_key;
              const isFake = s.ground_truth === 'FAKE';
              return (
                <div
                  key={s.sample_key}
                  onClick={() => handleSelectSample(s)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-blue-950/30 border-blue-500 ring-1 ring-blue-500/50'
                      : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-mono text-xs font-semibold text-slate-200">{s.name}</span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-bold font-mono ${
                        isFake ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      }`}
                    >
                      Ground Truth: {s.ground_truth}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-3 leading-relaxed">{s.description}</p>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                    <span>Duration: {s.duration}</span>
                    <span className="text-blue-400 flex items-center gap-1 font-semibold">
                      {isSelected ? 'Selected ✓' : 'Select Sample →'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Custom Upload Dropzone */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h3 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
            <UploadCloud className="w-4 h-4 text-blue-400" />
            <span>Upload Custom Video File</span>
          </h3>

          {!selectedFile && !selectedSampleKey ? (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-800 hover:border-blue-500/50 rounded-2xl p-10 text-center cursor-pointer transition-colors bg-slate-950/40 group"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="video/mp4,video/quicktime,video/x-msvideo,video/x-matroska"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileChange(e.target.files[0]);
                  }
                }}
              />
              <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto mb-4 group-hover:scale-105 transition-transform">
                <FileVideo className="w-7 h-7" />
              </div>
              <p className="text-sm font-semibold text-slate-200 mb-1">
                Drag and drop your video here, or <span className="text-blue-400">browse</span>
              </p>
              <p className="text-xs text-slate-500 mb-4">
                Supported formats: MP4, MOV, AVI, MKV (Maximum file size: 200 MB)
              </p>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-slate-900 border border-slate-800 text-[11px] text-slate-400 font-mono">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Files processed locally — no third-party cloud transfer</span>
              </div>
            </div>
          ) : (
            /* Selected Video Preview Card */
            <div className="rounded-xl bg-slate-950 border border-slate-800 p-4">
              <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
                    <Film className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-200">
                      {selectedSampleKey ? `Benchmark Sample: ${selectedSampleKey}.mp4` : selectedFile?.name}
                    </h4>
                    <p className="text-xs text-slate-400">
                      {selectedSampleKey
                        ? 'FaceForensics++ Sample Video'
                        : `${((selectedFile?.size || 0) / (1024 * 1024)).toFixed(2)} MB · Local Upload`}
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleClearSelection}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
                  title="Remove selection"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Video Player Preview */}
              {videoPreviewUrl && (
                <div className="relative rounded-lg overflow-hidden bg-black aspect-video max-h-72 mx-auto mb-4 border border-slate-800/80">
                  <video
                    src={videoPreviewUrl}
                    controls
                    className="w-full h-full object-contain"
                  />
                </div>
              )}

              {/* Video Metrics Badges */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500 block text-[10px]">FORMAT</span>
                  <span className="text-slate-200 font-bold">
                    {selectedSampleKey ? 'MP4 / H.264' : selectedFile?.name.split('.').pop()?.toUpperCase()}
                  </span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500 block text-[10px]">DIMENSIONS</span>
                  <span className="text-slate-200 font-bold">
                    {videoDimensions ? `${videoDimensions.width}×${videoDimensions.height}` : 'Auto-detected'}
                  </span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500 block text-[10px]">DURATION</span>
                  <span className="text-slate-200 font-bold">
                    {videoDimensions?.duration ? `${videoDimensions.duration.toFixed(1)}s` : selectedSampleKey ? '15.8s' : 'Estimating...'}
                  </span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500 block text-[10px]">TARGET SLIDING WINDOW</span>
                  <span className="text-blue-400 font-bold">10 frames / 3.0s</span>
                </div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {errorMessage && (
            <div className="mt-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Upload Progress */}
          {isUploading && (
            <div className="mt-4">
              <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1.5">
                <span>Uploading video to forensic pipeline...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}

          {/* Analyze Button */}
          <div className="mt-6 flex justify-end">
            <button
              onClick={handleStartAnalysis}
              disabled={(!selectedFile && !selectedSampleKey) || isUploading}
              className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium text-sm shadow-md transition-all flex items-center gap-2"
            >
              <Zap className="w-4 h-4" />
              <span>{isUploading ? 'Preparing Pipeline...' : 'Analyze Video'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
