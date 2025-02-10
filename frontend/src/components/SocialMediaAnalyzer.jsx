import React, { useState } from 'react';
import axios from 'axios';
import { Message, YouTube, Mic, Upload, AudioFile } from '@mui/icons-material';

const SocialMediaAnalyzer = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [text, setText] = useState('');
  const [link, setLink] = useState('');
  const [audioFile, setAudioFile] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTabChange = (index) => {
    setActiveTab(index);
    setResult(null);
  };

  const handleAnalyze = async (inputType) => {
    if ((inputType === 'link' && !link) ||
      (inputType === 'comment' && !text) ||
      (inputType === 'audio' && !audioFile)) {
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      let formData = new FormData();
      if (inputType === 'link') {
        formData.append('link', link);
      } else if (inputType === 'comment') {
        formData.append('text', text);
      } else if (inputType === 'audio') {
        formData.append('audio', audioFile);
      }

      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: { 'Content-Type': 'application/json' }
      });

      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAudioUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
    }
  };

  const startRecording = () => {
    setIsRecording(true);
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then((stream) => {
        const recorder = new MediaRecorder(stream);
        setMediaRecorder(recorder);

        const audioChunks = [];
        recorder.ondataavailable = (event) => audioChunks.push(event.data);

        recorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          setAudioFile(new File([audioBlob], "recording.wav"));
          setIsRecording(false);
        };

        recorder.start();
      })
      .catch(() => {
        setIsRecording(false);
      });
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
  };

  const getSeverityColor = (percentage) => {
    if (percentage <= 25) return 'bg-green-500';
    if (percentage <= 50) return 'bg-yellow-500';
    if (percentage <= 75) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-100 backdrop-blur-md">
        <h1 className="text-4xl font-bold text-center mb-4">Hate Speech Detection</h1>
        <p className="text-md text-center text-gray-600 mb-6">
          Analyze content for hateful speech across multiple languages like Hindi, Marathi & Bangla
        </p>

        <div className="flex justify-center mb-6">
          <button
            className={`px-6 py-2 mr-4 text-lg font-semibold rounded-lg ${activeTab === 0 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => handleTabChange(0)}
          >
            <Message className="inline-block mr-2" /> Text
          </button>
          <button
            className={`px-6 py-2 mr-4 text-lg font-semibold rounded-lg ${activeTab === 1 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => handleTabChange(1)}
          >
            <YouTube className="inline-block mr-2" /> YouTube
          </button>
          <button
            className={`px-6 py-2 text-lg font-semibold rounded-lg ${activeTab === 2 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => handleTabChange(2)}
          >
            <Mic className="inline-block mr-2" /> Audio
          </button>
        </div>

        {/* Text Analysis Tab */}
        {activeTab === 0 && (
          <div className="space-y-4">
            <textarea
              className="w-full p-3 border rounded-lg border-gray-300"
              rows={4}
              placeholder="Enter text to analyze"
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button
              className={`w-full py-2 bg-blue-500 text-white rounded-lg ${loading || !text ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => handleAnalyze('comment')}
              disabled={loading || !text}
            >
              {loading ? <div className="animate-spin border-4 border-t-4 border-white rounded-full w-5 h-5 mx-auto" /> : 'Analyze Text'}
            </button>
          </div>
        )}

        {/* YouTube Tab */}
        {activeTab === 1 && (
          <div className="space-y-4">
            <input
              type="text"
              className="w-full p-3 border rounded-lg border-gray-300"
              placeholder="Enter YouTube Video URL"
              value={link}
              onChange={(e) => setLink(e.target.value)}
            />
            <button
              className={`w-full py-2 bg-blue-500 text-white rounded-lg ${loading || !link ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => handleAnalyze('link')}
              disabled={loading || !link}
            >
              {loading ? <div className="animate-spin border-4 border-t-4 border-white rounded-full w-5 h-5 mx-auto" /> : 'Analyze Video Comments'}
            </button>
          </div>
        )}

        {/* Audio Tab */}
        {activeTab === 2 && (
          <div className="space-y-4">
            <div className="flex space-x-4">
              <button
                className="px-6 py-2 bg-gray-100 border rounded-lg w-full"
                onClick={() => document.getElementById('audio-upload').click()}
              >
                <Upload className="inline-block mr-2" /> Upload Audio
                <input
                  id="audio-upload"
                  type="file"
                  accept="audio/*"
                  className="hidden"
                  onChange={handleAudioUpload}
                />
              </button>
              <button
                className={`px-6 py-2 bg-${isRecording ? 'red-500' : 'blue-500'} text-white rounded-lg w-full`}
                onClick={isRecording ? stopRecording : startRecording}
              >
                <Mic className="inline-block mr-2" />
                {isRecording ? 'Stop Recording' : 'Record Audio'}
              </button>
            </div>
            {audioFile && (
              <div className="mt-2 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
                <AudioFile className="inline-block mr-2" />
                Audio file ready: {audioFile.name}
              </div>
            )}
            <button
              className={`w-full py-2 bg-blue-500 text-white rounded-lg ${loading || !audioFile ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => handleAnalyze('audio')}
              disabled={loading || !audioFile}
            >
              {loading ? <div className="animate-spin border-4 border-t-4 border-white rounded-full w-5 h-5 mx-auto" /> : 'Analyze Audio'}
            </button>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="mt-8 space-y-4">
            {result.transcription && (
              <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
                <strong>Transcription:</strong>
                <p>{result.transcription}</p>
              </div>
            )}

            <div className="p-4 border rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
              <div className="mb-4">
                <div className="flex justify-between mb-2">
                  <span>Hateful Content Detection</span>
                  <span>{result.hateSpeechPercentage.toFixed(1)}%</span>
                </div>
                <div className="relative pt-1">
                  <div className={`w-full h-2 rounded-lg ${getSeverityColor(result.hateSpeechPercentage)}`} style={{ width: `${result.hateSpeechPercentage}%` }} />
                </div>
              </div>

              {result.relatedTags && (
                <div>
                  <strong>Related Tags:</strong>
                  <ul className="list-disc pl-6">
                    {result.relatedTags.map((tag, index) => (
                      <li key={index}>{tag}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialMediaAnalyzer;
