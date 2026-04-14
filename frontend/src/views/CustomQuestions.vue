<template>
  <div class="custom-questions">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="header-icon">
              <path d="M9 12H15M12 9V15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>简历面试题生成</span>
          </div>
          <el-button type="primary" @click="goHome" class="back-btn">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="btn-icon">
              <path d="M15 19L8 12L15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <!-- 返回首页 -->
          </el-button>
        </div>
      </template>

      <div class="upload-section">
        <div class="section-title">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 18V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 15L12 12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>上传简历</span>
        </div>
        
        <el-upload
          ref="uploadRef"
          class="upload-area"
          drag
          action="/api/resume/upload"
          :auto-upload="false"
          :limit="1"
          accept=".pdf"
          :on-change="handleFileChange"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :file-list="fileList"
        >
          <div class="upload-content">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="upload-icon">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M17 8L12 3L7 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="upload-text">
              <p class="upload-hint">拖拽 PDF 简历到此处，或 <em>点击上传</em></p>
              <p class="upload-tip">支持 .pdf 格式，文件大小不超过 10MB</p>
            </div>
          </div>
        </el-upload>

        <div class="settings-section">
          <div class="setting-item">
            <label class="setting-label">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8.22891 16C8.77614 17.6663 10.2533 18.8909 12 18.8909C13.7467 18.8909 15.2239 17.6663 15.7711 16M9 10H9.01M15 10H15.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              面试题数量
            </label>
            <el-input-number 
              v-model="questionCount" 
              :min="5" 
              :max="30" 
              :step="5"
              class="count-input"
            />
          </div>

          <div class="setting-item">
            <label class="setting-label">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 6V4M12 20V18M18 12H20M4 12H6M15.5355 8.4645L16.9497 7.05029M7.05025 16.9497L8.46447 15.5355M15.5355 15.5355L16.9497 16.9497M7.05025 7.05029L8.46447 8.4645" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              难度级别
            </label>
            <el-checkbox-group v-model="selectedLevels" class="level-group">
              <el-checkbox label="初级">初级</el-checkbox>
              <el-checkbox label="中级">中级</el-checkbox>
              <el-checkbox label="高级">高级</el-checkbox>
            </el-checkbox-group>
          </div>

          <div class="setting-item">
            <label class="setting-label">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" stroke="currentColor" stroke-width="2"/>
                <path d="M2.45825 12C3.73253 7.94288 7.52281 5 12.0004 5C16.4781 5 20.2684 7.94291 21.5426 12C20.2684 16.0571 16.4781 19 12.0005 19C7.52281 19 3.73251 16.0571 2.45825 12Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              答题模式
            </label>
            <el-radio-group v-model="mode" class="mode-group">
              <el-radio label="view">查看模式</el-radio>
              <el-radio label="quiz">问答模式</el-radio>
            </el-radio-group>
          </div>
        </div>

        <el-button 
          type="primary" 
          size="large" 
          class="generate-btn"
          :loading="generating"
          :disabled="!uploadedResume"
          @click="generateQuestions"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </template>
          {{ generating ? '正在生成面试题...' : '生成面试题' }}
        </el-button>
      </div>

      <transition name="fade">
        <div v-if="questions.length > 0" class="questions-section">
          <div class="section-title">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 6H21M8 12H21M8 18H21M3 6H3.01M3 12H3.01M3 18H3.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>面试题列表</span>
            <span class="question-count">共 {{ questions.length }} 题</span>
          </div>

          <transition-group name="list" tag="div" class="questions-list">
            <div v-for="(question, index) in paginatedQuestions" :key="question.id" class="question-card">
              <div class="question-header">
                <div class="question-number">
                  <span>{{ (currentPage - 1) * pageSize + index + 1 }}</span>
                </div>
                <div class="question-info">
                  <span class="question-level" :class="getLevelClass(question.level)">
                    {{ question.level }}
                  </span>
                  <span v-if="question.technology" class="question-tech">
                    {{ question.technology }}
                  </span>
                </div>
              </div>
              
              <div class="question-content">
                <p>{{ question.question }}</p>
              </div>

              <div v-if="mode === 'view'" class="answer-section">
                <div class="answer-header">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="answer-icon">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>参考答案</span>
                </div>
                <div class="answer-content">
                  <p>{{ question.answer }}</p>
                </div>
              </div>
              
              <div v-else class="quiz-section">
                <div class="quiz-header">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="quiz-icon">
                    <path d="M11 4H4C2.89543 4 2 4.89543 2 6V20C2 21.1046 2.89543 22 4 22H18C19.1046 22 20 21.1046 20 20V13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M18.5 2.5C19.3284 1.67157 20.6716 1.67157 21.5 2.5C22.3284 3.32843 22.3284 4.67157 21.5 5.5L12 15L8 16L9 12L18.5 2.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  <span>你的答案</span>
                </div>
                <div class="quiz-textarea-wrapper">
                  <el-input
                    type="textarea"
                    :rows="4"
                    v-model="userAnswers[index]"
                    placeholder="请输入你的答案..."
                    class="quiz-input"
                  />
                  <el-tooltip 
                    :content="isAnswerRecording && currentAnswerIndex === index ? '点击停止录音' : isAnswerUploading ? '正在识别...' : '点击开始语音输入'" 
                    placement="top"
                  >
                    <button 
                      type="button"
                      class="voice-btn quiz-voice-btn"
                      :class="{ active: isAnswerRecording && currentAnswerIndex === index, uploading: isAnswerUploading && currentAnswerIndex === index }"
                      @click="handleAnswerVoiceInput(index)"
                      :disabled="isAnswerUploading || (isAnswerRecording && currentAnswerIndex !== index)"
                    >
                      <svg v-if="(!isAnswerRecording || currentAnswerIndex !== index) && !isAnswerUploading" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 19V23M8 23H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      <svg v-else-if="isAnswerRecording && currentAnswerIndex === index" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rotating">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-dasharray="31.4" stroke-dashoffset="10"/>
                      </svg>
                    </button>
                  </el-tooltip>
                </div>
                <div v-if="isAnswerRecording && currentAnswerIndex === index" class="voice-hint answer-hint">
                  <span class="pulse-dot"></span>
                  正在录音，点击按钮停止...
                </div>
                <div v-else-if="isAnswerUploading && currentAnswerIndex === index" class="voice-hint answer-hint uploading">
                  正在识别语音...
                </div>
                <el-button type="primary" @click="submitAnswer(index)" class="submit-btn">
                  <template #icon>
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="btn-icon">
                      <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </template>
                  提交答案
                </el-button>
                <transition name="fade">
                  <div v-if="showAnswers[index]" class="correct-answer">
                    <div class="correct-header">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="correct-icon">
                        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      <span>参考答案</span>
                    </div>
                    <p>{{ question.answer }}</p>
                  </div>
                </transition>
              </div>
            </div>
          </transition-group>

          <div v-if="questions.length > pageSize" class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[5, 10, 20]"
              :total="questions.length"
              layout="total, sizes, prev, pager, next"
              class="custom-pagination"
            />
          </div>
        </div>
      </transition>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAudioRecorder } from '../composables/useAudioRecorder'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

interface Question {
  id: number
  question: string
  answer: string
  level: string
  technology?: string
}

interface UploadFile {
  name: string
  url?: string
  raw?: File
}

const fileList = ref<UploadFile[]>([])
const uploadedResume = ref<boolean>(false)
const questionCount = ref(10)
const selectedLevels = ref<string[]>(['初级', '中级', '高级'])
const mode = ref<'view' | 'quiz'>('view')
const questions = ref<Question[]>([])
const userAnswers = ref<string[]>([])
const showAnswers = ref<boolean[]>([])
const generating = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

const {
  isRecording: isAnswerRecording,
  isUploading: isAnswerUploading,
  error: answerRecordError,
  toggleRecording: toggleAnswerRecording
} = useAudioRecorder()

const currentAnswerIndex = ref<number | null>(null)

const paginatedQuestions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return questions.value.slice(start, end)
})

const handleFileChange = (file: any, fileList_: any) => {
  if (file.raw) {
    fileList.value = [file]
    uploadedResume.value = true
  }
}

const handleUploadSuccess = (response: any) => {
  if (response.success) {
    ElMessage.success('简历上传成功')
  } else {
    ElMessage.error(response.error || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败，请重试')
}

const generateQuestions = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请先上传简历')
    return
  }

  generating.value = true
  questions.value = []
  
  try {
    const formData = new FormData()
    formData.append('file', fileList.value[0].raw as File)
    formData.append('count', questionCount.value.toString())
    formData.append('levels', JSON.stringify(selectedLevels.value))

    const response = await fetch('/api/resume/generate-questions', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('生成失败')
    }

    const data = await response.json()
    
    if (data.questions && data.questions.length > 0) {
      questions.value = data.questions
      userAnswers.value = new Array(data.questions.length).fill('')
      showAnswers.value = new Array(data.questions.length).fill(false)
      ElMessage.success(`成功生成 ${data.questions.length} 道面试题`)
    } else {
      ElMessage.warning('未能生成面试题，请检查简历内容')
    }
  } catch (error) {
    console.error('Generate questions error:', error)
    ElMessage.error('生成面试题失败，请重试')
  } finally {
    generating.value = false
  }
}

const getLevelClass = (level: string) => {
  const map: Record<string, string> = {
    '初级': 'beginner',
    '中级': 'intermediate',
    '高级': 'advanced'
  }
  return map[level] || 'beginner'
}

const handleAnswerVoiceInput = async (index: number) => {
  if (currentAnswerIndex.value !== null && currentAnswerIndex.value !== index && isAnswerRecording.value) {
    return
  }
  
  currentAnswerIndex.value = index
  const text = await toggleAnswerRecording()
  if (text) {
    userAnswers.value[index] = userAnswers.value[index] 
      ? userAnswers.value[index] + text 
      : text
  }
  if (!isAnswerRecording.value) {
    currentAnswerIndex.value = null
  }
}

const submitAnswer = (index: number) => {
  showAnswers.value[index] = true
}
</script>

<style scoped>
.custom-questions {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.main-card {
  max-width: 900px;
  margin: 0 auto;
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: #667eea;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.upload-section {
  padding: 30px;
  background: linear-gradient(135deg, #fafbfc 0%, #f0f4f8 100%);
  border-radius: 12px;
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 20px;
}

.section-title svg {
  width: 22px;
  height: 22px;
  color: #667eea;
}

.question-count {
  margin-left: auto;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  background: #e5e7eb;
  padding: 4px 12px;
  border-radius: 20px;
}

.upload-area {
  margin-bottom: 25px;
}

.upload-area :deep(.el-upload-dragger) {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  background: white;
  transition: all 0.3s ease;
}

.upload-area :deep(.el-upload-dragger:hover) {
  border-color: #667eea;
  background: #f8faff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #9ca3af;
  margin-bottom: 16px;
}

.upload-text {
  text-align: center;
}

.upload-hint {
  font-size: 16px;
  color: #4b5563;
  margin: 0 0 8px 0;
}

.upload-hint em {
  color: #667eea;
  font-style: normal;
}

.upload-tip {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

.settings-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
}

.setting-label svg {
  width: 18px;
  height: 18px;
  color: #667eea;
}

.count-input {
  width: 100%;
}

.level-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.mode-group {
  display: flex;
  gap: 20px;
}

.generate-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.questions-section {
  margin-top: 30px;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.question-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.question-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.question-info {
  display: flex;
  gap: 10px;
}

.question-level {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.question-level.beginner {
  background: #dcfce7;
  color: #16a34a;
}

.question-level.intermediate {
  background: #fef3c7;
  color: #d97706;
}

.question-level.advanced {
  background: #fee2e2;
  color: #dc2626;
}

.question-tech {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: #e0e7ff;
  color: #4f46e5;
}

.question-content {
  margin-bottom: 20px;
}

.question-content p {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  color: #1f2937;
}

.answer-section {
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.answer-header,
.quiz-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #4b5563;
}

.answer-icon,
.quiz-icon {
  width: 18px;
  height: 18px;
  color: #22c55e;
}

.quiz-icon {
  color: #667eea;
}

.answer-content p {
  margin: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #334155;
}

.quiz-textarea-wrapper {
  position: relative;
}

.quiz-textarea-wrapper .quiz-input {
  width: 100%;
}

.quiz-textarea-wrapper .quiz-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  padding-right: 50px;
}

.quiz-textarea-wrapper .quiz-input :deep(.el-textarea__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.quiz-voice-btn {
  position: absolute;
  right: 12px;
  bottom: 12px;
}

.answer-hint {
  margin-bottom: 10px;
}

.voice-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.voice-btn:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: scale(1.05);
}

.voice-btn.active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  animation: pulse 1.5s infinite;
}

.voice-btn.uploading {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.voice-btn:disabled {
  cursor: not-allowed;
}

.voice-btn svg {
  width: 18px;
  height: 18px;
}

.voice-btn .rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
}

.voice-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 13px;
  color: #ef4444;
}

.voice-hint.uploading {
  color: #667eea;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulseDot 1s infinite;
}

@keyframes pulseDot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.submit-btn {
  margin-top: 15px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
}

.correct-answer {
  margin-top: 20px;
  padding: 15px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
  border-left: 4px solid #22c55e;
}

.correct-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #16a34a;
}

.correct-icon {
  width: 18px;
  height: 18px;
}

.correct-answer p {
  margin: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #166534;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.custom-pagination {
  padding: 15px;
  background: white;
  border-radius: 12px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .custom-questions {
    padding: 10px;
  }

  .upload-section {
    padding: 20px;
  }

  .settings-section {
    grid-template-columns: 1fr;
  }

  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .question-info {
    flex-wrap: wrap;
  }
}
</style>
