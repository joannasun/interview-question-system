<template>
  <div class="ai-agent-questions">
    <div class="page-hero">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="hero-content">
        <div class="hero-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="currentColor" stroke-width="2"/>
            <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <h1 class="hero-title">AI Agent 面试题</h1>
        <p class="hero-subtitle">LLM / ReAct / MCP / Skills / LangChain / RAG / Memory / Context</p>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="filter-card">
        <div class="filter-header">
          <div class="header-left">
            <div class="filter-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 6H20M4 12H20M4 18H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span>筛选条件</span>
          </div>
          <el-button class="back-btn" @click="goHome" :disabled="generating">
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="btn-icon">
                <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </template>
            <!-- <span class="back-text">返回首页</span> -->
          </el-button>
        </div>
        
        <div class="filter-content">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="6">
              <div class="filter-item">
                <label class="filter-label">难度级别</label>
                <el-checkbox-group v-model="selectedLevels" class="custom-checkbox-group">
                  <el-checkbox label="初级" class="custom-checkbox">
                    <span class="checkbox-content">
                      <span class="dot beginner"></span>
                      初级
                    </span>
                  </el-checkbox>
                  <el-checkbox label="中级" class="custom-checkbox">
                    <span class="checkbox-content">
                      <span class="dot intermediate"></span>
                      中级
                    </span>
                  </el-checkbox>
                  <el-checkbox label="高级" class="custom-checkbox">
                    <span class="checkbox-content">
                      <span class="dot advanced"></span>
                      高级
                    </span>
                  </el-checkbox>
                </el-checkbox-group>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="filter-item">
                <label class="filter-label">技术类型</label>
                <el-checkbox-group v-model="selectedTechnologies" class="tech-checkbox-group">
                  <el-checkbox v-for="tech in ['LLM', 'ReAct', 'MCP', 'Skills', 'LangChain', 'RAG', 'Memory', 'Context']" :key="tech" :label="tech" />
                </el-checkbox-group>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="filter-item">
                <label class="filter-label">模式选择</label>
                <el-radio-group v-model="mode" class="custom-radio-group">
                  <el-radio label="view">
                    <span class="radio-content">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="mode-icon">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
                        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                      </svg>
                      查看模式
                    </span>
                  </el-radio>
                  <el-radio label="quiz">
                    <span class="radio-content">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="mode-icon">
                        <path d="M9 11L12 14L22 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M21 12V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      问答模式
                    </span>
                  </el-radio>
                </el-radio-group>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <div class="filter-item">
                <label class="filter-label">题目数量</label>
                <el-input-number v-model="questionCount" :min="1" :max="50" class="custom-number" />
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :xs="24">
              <div class="filter-item">
                <label class="filter-label">自定义方向（可选）</label>
                <div class="textarea-wrapper">
                  <el-input
                    v-model="userInput"
                    type="textarea"
                    :rows="2"
                    placeholder="输入您想了解的面试题方向..."
                    class="custom-textarea"
                  />
                  <el-tooltip 
                    :content="isRecording ? '点击停止录音' : isUploading ? '正在识别...' : '点击开始语音输入'" 
                    placement="top"
                  >
                    <button 
                      type="button"
                      class="voice-btn"
                      :class="{ active: isRecording, uploading: isUploading }"
                      @click="handleVoiceInput"
                      :disabled="isUploading"
                    >
                      <svg v-if="!isRecording && !isUploading" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 19V23M8 23H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      <svg v-else-if="isRecording" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rotating">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-dasharray="31.4" stroke-dashoffset="10"/>
                      </svg>
                    </button>
                  </el-tooltip>
                </div>
                <div v-if="isRecording" class="voice-hint">
                  <span class="pulse-dot"></span>
                  正在录音，点击按钮停止...
                </div>
                <div v-else-if="isUploading" class="voice-hint uploading">
                  正在识别语音...
                </div>
              </div>
            </el-col>
          </el-row>

          <div class="action-buttons">
            <el-button type="primary" class="generate-btn" @click="generateQuestions" :loading="generating">
              <template #icon>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="btn-icon">
                  <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
              {{ generating ? 'AI 生成中...' : 'AI 智能生成' }}
            </el-button>
          </div>
        </div>
      </div>

      <div class="questions-section">
        <div v-if="questions.length === 0 && !streamingText" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="currentColor" stroke-width="2"/>
              <path d="M9 12H15M9 16H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <p class="empty-text">暂无题目</p>
          <p class="empty-hint">点击上方"AI 智能生成"按钮开始生成面试题</p>
        </div>

        <div v-if="streamingText && questions.length === 0" class="streaming-card">
          <div class="streaming-header">
            <div class="streaming-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rotating">
                <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.07 4.93L16.24 7.76M7.76 16.24L4.93 19.07M19.07 19.07L16.24 16.24M7.76 7.76L4.93 4.93" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <span>AI 正在生成{{ mode === 'quiz' ? '问题' : '内容' }}...</span>
          </div>
          <div class="streaming-content">
            <pre>{{ streamingText }}</pre>
          </div>
        </div>

        <transition-group name="question-list" tag="div" v-if="questions.length > 0">
          <div v-for="(question, index) in questions" :key="index" class="question-card" :style="{ animationDelay: `${index * 0.1}s` }">
            <div class="question-header">
              <div class="question-number">
                <span class="number">{{ index + 1 }}</span>
              </div>
              <div class="question-info">
                <span class="question-title">{{ question.question }}</span>
                <div class="question-meta">
                  <span class="meta-tag level-tag" :class="getLevelClass(question.level)">{{ question.level }}</span>
                  <span class="meta-tag tech-tag">{{ question.technology }}</span>
                </div>
              </div>
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

        <div v-if="questions.length > 0" class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            class="custom-pagination"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAudioRecorder } from '@/composables/useAudioRecorder'

const router = useRouter()

const {
  isRecording,
  isUploading,
  error: recordError,
  toggleRecording
} = useAudioRecorder()

const goHome = () => {
  router.push('/')
}

watch(recordError, (newVal) => {
  if (newVal) {
    ElMessage.warning(newVal)
  }
})

const handleVoiceInput = async () => {
  const text = await toggleRecording()
  if (text) {
    userInput.value = userInput.value ? userInput.value + text : text
  }
}

const {
  isRecording: isAnswerRecording,
  isUploading: isAnswerUploading,
  error: answerRecordError,
  toggleRecording: toggleAnswerRecording
} = useAudioRecorder()

const currentAnswerIndex = ref<number | null>(null)

watch(answerRecordError, (newVal) => {
  if (newVal) {
    ElMessage.warning(newVal)
  }
})

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

interface Question {
  id: number
  question: string
  answer: string
  level: string
  technology: string
}

const selectedLevels = ref<string[]>(['初级', '中级', '高级'])
const selectedTechnologies = ref<string[]>(['LLM', 'ReAct', 'MCP', 'Skills', 'LangChain', 'RAG', 'Memory', 'Context'])
const mode = ref<'view' | 'quiz'>('view')
const userInput = ref('')
const questionCount = ref(10)
const questions = ref<Question[]>([])
const userAnswers = ref<string[]>([])
const showAnswers = ref<boolean[]>([])
const generating = ref(false)
const streamingText = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const getLevelClass = (level: string) => {
  const map: Record<string, string> = {
    '初级': 'beginner',
    '中级': 'intermediate',
    '高级': 'advanced'
  }
  return map[level] || 'beginner'
}

const generateQuestions = async () => {
  generating.value = true
  streamingText.value = ''
  questions.value = []
  userAnswers.value = []
  showAnswers.value = []
  
  try {
    const response = await fetch('/api/questions/generate-stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topic: 'AI Agent',
        levels: selectedLevels.value,
        technologies: selectedTechnologies.value,
        user_input: userInput.value || null,
        page: currentPage.value,
        page_size: pageSize.value,
        count: questionCount.value
      })
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('无法获取响应流')
    }

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          
          if (data === '[DONE]') {
            generating.value = false
            streamingText.value = ''
            ElMessage.success('AI生成题目成功')
            return
          }

          try {
            const parsed = JSON.parse(data)
            
            if (parsed.type === 'chunk') {
              streamingText.value += parsed.content
            } else if (parsed.type === 'questions') {
              streamingText.value = ''
              questions.value = parsed.data
              total.value = parsed.data.length
              userAnswers.value = new Array(parsed.data.length).fill('')
              showAnswers.value = new Array(parsed.data.length).fill(false)
            }
          } catch {
            // Ignore parse errors
          }
        }
      }
    }
  } catch (error) {
    console.error('Stream error:', error)
    ElMessage.error('AI生成题目失败')
  } finally {
    generating.value = false
  }
}

const submitAnswer = (index: number) => {
  showAnswers.value[index] = true
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}
</script>

<style scoped>
.ai-agent-questions {
  min-height: 100%;
  background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
}

.page-hero {
  position: relative;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  padding: 40px 20px;
  overflow: hidden;
}

.floating-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 60px;
  height: 60px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 10%;
  left: 30%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.hero-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: scaleIn 0.6s ease-out;
}

.hero-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 10px;
  animation: slideDown 0.6s ease-out;
}

.hero-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
  animation: slideUp 0.6s ease-out 0.2s both;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.filter-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 25px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  font-size: 18px;
  font-weight: 600;
  color: #334155;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.filter-header .back-btn {
  height: 36px;
  width: 36PX;
  padding: 0 16px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  background: white;
  color: #64748b;
  transition: all 0.3s ease;
}

.filter-header .back-btn:hover:not(:disabled) {
  border-color: #764ba2;
  color: #764ba2;
}

.filter-header .back-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.back-text {
  margin-left: 5px;
}

.filter-content {
  padding: 25px;
}

.filter-item {
  margin-bottom: 20px;
}

.filter-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 12px;
}

.custom-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.custom-checkbox {
  margin-right: 0 !important;
}

.custom-checkbox :deep(.el-checkbox__label) {
  display: flex;
  align-items: center;
}

.checkbox-content {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.beginner {
  background: #22c55e;
}

.dot.intermediate {
  background: #f59e0b;
}

.dot.advanced {
  background: #ef4444;
}

.tech-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-checkbox-group :deep(.el-checkbox) {
  margin-right: 0 !important;
}

.custom-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mode-icon {
  width: 16px;
  height: 16px;
}

.custom-number {
  width: 100%;
}

.custom-number :deep(.el-input__wrapper) {
  border-radius: 8px;
}

.custom-textarea :deep(.el-textarea__inner) {
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.custom-textarea :deep(.el-textarea__inner:focus) {
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
}

.textarea-wrapper {
  position: relative;
}

.textarea-wrapper .custom-textarea {
  width: 100%;
}

.textarea-wrapper .custom-textarea :deep(.el-textarea__inner) {
  padding-right: 50px;
}

.voice-btn {
  position: absolute;
  right: 12px;
  bottom: 12px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.voice-btn:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  transform: scale(1.05);
}

.voice-btn.active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  animation: pulse 1.5s infinite;
}

.voice-btn.uploading {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
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
  color: #764ba2;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulseDot 1s infinite;
}

@keyframes pulseDot {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.generate-btn {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  border: none;
  transition: all 0.3s ease;
}

.generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.questions-section {
  min-height: 300px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #94a3b8;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 8px;
}

.empty-hint {
  font-size: 14px;
  color: #94a3b8;
  margin: 0;
}

.streaming-card {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 20px;
  animation: fadeIn 0.5s ease-out;
}

.streaming-header {
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
}

.streaming-icon {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.streaming-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.streaming-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.streaming-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
}

.question-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  overflow: hidden;
  animation: questionFadeIn 0.5s ease-out both;
  transition: all 0.3s ease;
}

.question-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

@keyframes questionFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.question-header {
  display: flex;
  gap: 15px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.question-number {
  flex-shrink: 0;
}

.number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  font-size: 16px;
  font-weight: 700;
  border-radius: 10px;
}

.question-info {
  flex: 1;
}

.question-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
  line-height: 1.5;
}

.question-meta {
  display: flex;
  gap: 8px;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.level-tag.beginner {
  background: #dcfce7;
  color: #16a34a;
}

.level-tag.intermediate {
  background: #fef3c7;
  color: #d97706;
}

.level-tag.advanced {
  background: #fee2e2;
  color: #dc2626;
}

.tech-tag {
  background: #f3e8ff;
  color: #9333ea;
}

.answer-section,
.quiz-section {
  padding: 20px;
}

.answer-header,
.quiz-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.answer-icon,
.quiz-icon {
  width: 20px;
  height: 20px;
  color: #764ba2;
}

.answer-content {
  padding: 15px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #764ba2;
}

.answer-content p {
  margin: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #334155;
}

.quiz-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.quiz-input :deep(.el-textarea__inner:focus) {
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
}

.quiz-textarea-wrapper {
  position: relative;
}

.quiz-textarea-wrapper .quiz-input {
  width: 100%;
}

.quiz-textarea-wrapper .quiz-input :deep(.el-textarea__inner) {
  padding-right: 50px;
}

.quiz-voice-btn {
  position: absolute;
  right: 12px;
  bottom: 12px;
}

.answer-hint {
  margin-bottom: 10px;
}

.submit-btn {
  margin-top: 15px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
  width: 20px;
  height: 20px;
  color: #22c55e;
}

.correct-answer p {
  margin: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #166534;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.custom-pagination :deep(.el-pager li) {
  border-radius: 8px;
  margin: 0 4px;
}

.custom-pagination :deep(.btn-prev),
.custom-pagination :deep(.btn-next) {
  border-radius: 8px;
}

@media (max-width: 768px) {
  .page-hero {
    padding: 30px 15px;
  }

  .hero-icon {
    width: 60px;
    height: 60px;
    border-radius: 15px;
  }

  .hero-icon svg {
    width: 30px;
    height: 30px;
  }

  .hero-title {
    font-size: 24px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .content-wrapper {
    padding: 20px 15px;
  }

  .filter-header {
    flex-wrap: wrap;
    gap: 10px;
    padding: 15px 20px;
    font-size: 16px;
  }

  .filter-header .back-btn {
    order: -1;
    width: 100%;
    margin-bottom: 5px;
  }

  .header-left {
    width: 100%;
  }

  .filter-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
  }

  .filter-icon svg {
    width: 18px;
    height: 18px;
  }

  .filter-content {
    padding: 20px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .generate-btn {
    width: 100%;
  }

  .question-header {
    flex-direction: column;
    gap: 10px;
  }

  .question-title {
    font-size: 15px;
  }

  .question-meta {
    flex-wrap: wrap;
  }

  .answer-content p,
  .correct-answer p {
    font-size: 14px;
  }

  .pagination-container :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
  }

  .pagination-container :deep(.el-pagination__sizes),
  .pagination-container :deep(.el-pagination__jump) {
    display: none;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 20px;
  }

  .filter-label {
    font-size: 13px;
  }

  .question-title {
    font-size: 14px;
  }

  .meta-tag {
    font-size: 11px;
    padding: 3px 10px;
  }
}
</style>
