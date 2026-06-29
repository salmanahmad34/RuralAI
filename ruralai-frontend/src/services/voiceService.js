const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

export const isVoiceSupported = !!SpeechRecognition

export const createRecognition = () => {
  if (!isVoiceSupported) return null
  
  const recognition = new SpeechRecognition()
  recognition.continuous = true
  recognition.interimResults = true
  return recognition
}
