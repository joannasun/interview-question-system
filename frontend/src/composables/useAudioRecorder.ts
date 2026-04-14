import { ref, onUnmounted } from 'vue'

export function useAudioRecorder() {
  const isRecording = ref(false)
  const isUploading = ref(false)
  const error = ref('')
  
  let mediaRecorder: MediaRecorder | null = null
  let audioChunks: Blob[] = []

  const startRecording = async () => {
    try {
      error.value = ''
      audioChunks = []
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000
        } 
      })
      
      const mimeType = MediaRecorder.isTypeSupported('audio/webm') 
        ? 'audio/webm' 
        : 'audio/mp4'
      
      mediaRecorder = new MediaRecorder(stream, { mimeType })
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }
      
      mediaRecorder.start(1000)
      isRecording.value = true
    } catch (e) {
      console.error('Failed to start recording:', e)
      if (e instanceof Error) {
        if (e.name === 'NotAllowedError') {
          error.value = '请允许麦克风权限以使用语音输入功能'
        } else if (e.name === 'NotFoundError') {
          error.value = '未检测到麦克风设备'
        } else {
          error.value = '启动录音失败，请重试'
        }
      }
    }
  }

  const stopRecording = (): Promise<Blob | null> => {
    return new Promise((resolve) => {
      if (!mediaRecorder || !isRecording.value) {
        resolve(null)
        return
      }
      
      mediaRecorder.onstop = () => {
        const mimeType = mediaRecorder?.mimeType || 'audio/webm'
        const audioBlob = new Blob(audioChunks, { type: mimeType })
        
        if (mediaRecorder?.stream) {
          mediaRecorder.stream.getTracks().forEach(track => track.stop())
        }
        
        isRecording.value = false
        mediaRecorder = null
        resolve(audioBlob)
      }
      
      mediaRecorder.stop()
    })
  }

  const uploadAndTranscribe = async (audioBlob: Blob): Promise<string> => {
    isUploading.value = true
    error.value = ''
    
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.webm')
      
      const response = await fetch('/api/speech/transcribe', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Transcription failed')
      }
      
      const data = await response.json()
      return data.text || ''
    } catch (e) {
      console.error('Transcription error:', e)
      error.value = '语音识别失败，请重试'
      return ''
    } finally {
      isUploading.value = false
    }
  }

  const toggleRecording = async (): Promise<string> => {
    if (isRecording.value) {
      const audioBlob = await stopRecording()
      if (audioBlob) {
        return await uploadAndTranscribe(audioBlob)
      }
      return ''
    } else {
      await startRecording()
      return ''
    }
  }

  onUnmounted(() => {
    if (mediaRecorder && isRecording.value) {
      mediaRecorder.stream.getTracks().forEach(track => track.stop())
    }
  })

  return {
    isRecording,
    isUploading,
    error,
    startRecording,
    stopRecording,
    uploadAndTranscribe,
    toggleRecording
  }
}
