import React from 'react'
import { Mic, Square, AlertCircle } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import useVoiceInput from '../hooks/useVoiceInput'

const VoiceInput = ({ onTranscription }) => {
  const { t } = useTranslation()
  const { transcript, isRecording, error, confidence, startRecording, stopRecording, isSupported } = useVoiceInput(onTranscription)

  if (!isSupported) {
    return (
      <div className="flex items-center text-red-500 p-4 border border-red-200 rounded bg-red-50 dark:bg-red-900/10 text-sm" role="alert">
        <AlertCircle className="w-5 h-5 mr-2" aria-hidden="true" />
        {t('errors.mic_unsupported')}
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center p-6 border rounded-xl bg-card shadow-sm transition-all hover:shadow-md h-full">
      {error && (
        <div className="mb-4 text-sm text-red-500 flex items-center bg-red-50 dark:bg-red-900/10 p-2 rounded w-full" role="alert">
          <AlertCircle className="w-4 h-4 mr-1 flex-shrink-0" aria-hidden="true" />
          <span>{error}</span>
        </div>
      )}
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`p-6 rounded-full transition-all duration-300 focus:outline-none focus-visible:ring-4 focus-visible:ring-green-500 focus-visible:ring-offset-2 ${
          isRecording 
            ? 'bg-red-500 hover:bg-red-600 animate-pulse text-white shadow-[0_0_15px_rgba(239,68,68,0.5)] scale-110' 
            : 'bg-green-500 hover:bg-green-600 text-white shadow-md hover:scale-105'
        }`}
        aria-label={isRecording ? "Stop voice recording" : "Start voice recording"}
        aria-pressed={isRecording}
      >
        {isRecording ? <Square className="h-8 w-8" aria-hidden="true" /> : <Mic className="h-8 w-8" aria-hidden="true" />}
      </button>
      
      <p className="mt-4 text-sm font-medium text-gray-600 dark:text-gray-300 text-center min-h-[40px]" aria-live="polite">
        {isRecording ? "Listening... (Stops after 2s silence)" : t('input.voice_placeholder')}
      </p>

      {isRecording && transcript && (
        <div 
          className="mt-4 w-full p-3 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm text-gray-800 dark:text-gray-200 break-words border border-gray-200 dark:border-gray-700 animate-in fade-in"
          aria-live="polite"
        >
          <span className="sr-only">Live transcript:</span>
          "{transcript}"
        </div>
      )}

      {confidence > 0 && isRecording && (
        <div className="mt-2 text-xs text-gray-400" aria-live="polite">
          Confidence: {confidence}%
        </div>
      )}
    </div>
  )
}

export default VoiceInput
