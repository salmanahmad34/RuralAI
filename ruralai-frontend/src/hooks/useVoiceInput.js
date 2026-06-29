import { useState, useEffect, useRef } from 'react'
import { isVoiceSupported, createRecognition } from '../services/voiceService'
import { useTranslation } from 'react-i18next'

const useVoiceInput = (onTranscription) => {
  const [isRecording, setIsRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState(null)
  const [confidence, setConfidence] = useState(0)
  const recognitionRef = useRef(null)
  const silenceTimeoutRef = useRef(null)
  const { i18n, t } = useTranslation()

  useEffect(() => {
    if (isVoiceSupported && !recognitionRef.current) {
      recognitionRef.current = createRecognition()
    }
    return () => {
      if (silenceTimeoutRef.current) clearTimeout(silenceTimeoutRef.current)
      if (recognitionRef.current && isRecording) recognitionRef.current.stop()
    }
  }, [isRecording])

  const handleSilence = () => {
    if (silenceTimeoutRef.current) clearTimeout(silenceTimeoutRef.current)
    silenceTimeoutRef.current = setTimeout(() => {
      stopRecording()
    }, 2000)
  }

  const startRecording = () => {
    if (!isVoiceSupported) {
      setError(t('errors.mic_unsupported'))
      return
    }

    if (recognitionRef.current) {
      setError(null)
      setTranscript('')
      setConfidence(0)

      const langMap = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'mr': 'mr-IN',
        'ta': 'ta-IN'
      }
      recognitionRef.current.lang = langMap[i18n.language] || 'en-IN'
      
      recognitionRef.current.onresult = (event) => {
        let finalTranscript = ''
        let interimTranscript = ''
        let latestConfidence = 0

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript
            latestConfidence = event.results[i][0].confidence
          } else {
            interimTranscript += event.results[i][0].transcript
          }
        }
        
        const currentText = finalTranscript || interimTranscript
        setTranscript(prev => prev + currentText)
        if (latestConfidence > 0) setConfidence(Math.round(latestConfidence * 100))
        
        if (finalTranscript && onTranscription) {
          onTranscription(finalTranscript)
        }
        
        handleSilence()
      }

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error', event.error)
        if (event.error === 'not-allowed') {
          setError(t('errors.mic_permission'))
        } else {
          setError(event.error)
        }
        stopRecording()
      }

      recognitionRef.current.onend = () => {
        setIsRecording(false)
        if (silenceTimeoutRef.current) clearTimeout(silenceTimeoutRef.current)
      }

      try {
        recognitionRef.current.start()
        setIsRecording(true)
        handleSilence()
      } catch (err) {
        console.error(err)
      }
    }
  }

  const stopRecording = () => {
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop()
      setIsRecording(false)
    }
    if (silenceTimeoutRef.current) clearTimeout(silenceTimeoutRef.current)
  }

  return {
    transcript,
    isRecording,
    error,
    confidence,
    startRecording,
    stopRecording,
    isSupported: isVoiceSupported
  }
}

export default useVoiceInput
