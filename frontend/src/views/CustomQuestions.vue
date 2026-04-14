<template>
  <div class="custom-questions">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="goHome" class="back-btn">
            <el-icon><Back /></el-icon>
            返回首页
          </el-button>
          <span>自定义面试题</span>
        </div>
      </template>
      <div class="upload-section">
        <el-form-item label="上传文件">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :file-list="fileList"
            :auto-upload="false"
            accept=".txt,.jpg,.jpeg,.png"
          >
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <template #tip>
              <div class="el-upload__tip">
                支持上传 .txt、.jpg、.jpeg、.png 文件
              </div>
            </template>
          </el-upload>
          <el-button type="success" @click="submitUpload">上传并解析</el-button>
        </el-form-item>
      </div>
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="难度级别">
              <el-checkbox-group v-model="selectedLevels">
                <el-checkbox label="初级">初级</el-checkbox>
                <el-checkbox label="中级">中级</el-checkbox>
                <el-checkbox label="高级">高级</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="模式选择">
              <el-radio-group v-model="mode">
                <el-radio label="view">查看模式</el-radio>
                <el-radio label="quiz">问答模式</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-button type="primary" @click="loadQuestions">加载题目</el-button>
      </div>
      <div class="questions-section">
        <div v-if="questions.length === 0" class="empty-state">
          <el-empty description="暂无题目，请先上传文件" />
        </div>
        <div v-else>
          <el-card v-for="(question, index) in questions" :key="index" class="question-card">
            <template #header>
              <div class="question-header">
                <span class="question-title">问题 {{ index + 1 }}</span>
                <span class="question-meta">{{ question.level }}</span>
              </div>
            </template>
            <div class="question-content">
              <p>{{ question.question }}</p>
            </div>
            <div v-if="mode === 'view'" class="answer-section">
              <el-divider content-position="left">答案</el-divider>
              <p>{{ question.answer }}</p>
            </div>
            <div v-else class="quiz-section">
              <el-divider content-position="left">你的答案</el-divider>
              <el-input
                type="textarea"
                :rows="4"
                v-model="userAnswers[index]"
                placeholder="请输入你的答案"
              />
              <el-button type="primary" @click="submitAnswer(index)">提交答案</el-button>
              <div v-if="showAnswers[index]" class="correct-answer">
                <el-divider content-position="left">参考答案</el-divider>
                <p>{{ question.answer }}</p>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Back } from '@element-plus/icons-vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

interface Question {
  id: number
  question: string
  answer: string
  level: string
}

interface UploadFile {
  name: string
  url: string
}

const fileList = ref<UploadFile[]>([])
const selectedLevels = ref<string[]>(['初级', '中级', '高级'])
const mode = ref<'view' | 'quiz'>('view')
const questions = ref<Question[]>([])
const userAnswers = ref<string[]>([])
const showAnswers = ref<boolean[]>([])

const handleUploadSuccess = (_: any, uploadFile: any) => {
  fileList.value.push(uploadFile)
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const submitUpload = () => {
  // 模拟上传成功
  ElMessage.success('文件解析成功')
}

const loadQuestions = () => {
  // 模拟数据，实际应该从后端API获取
  questions.value = [
    {
      id: 1,
      question: '请解释什么是响应式设计？',
      answer: '响应式设计是一种网页设计方法，使网站能够根据不同设备的屏幕尺寸和方向自动调整布局和内容，以提供最佳的用户体验。',
      level: '初级'
    },
    {
      id: 2,
      question: '请描述一下TypeScript中的接口和类型别名的区别？',
      answer: '接口和类型别名都可以用来定义类型，但它们有一些区别：1. 接口只能定义对象类型，而类型别名可以定义任何类型；2. 接口可以被合并，而类型别名不能；3. 接口可以被类实现，而类型别名不能。',
      level: '中级'
    },
    {
      id: 3,
      question: '请解释一下Vue3中的Pinia是什么？它与Vuex有什么区别？',
      answer: 'Pinia是Vue3的官方状态管理库，是Vuex的替代品。与Vuex的区别：1. Pinia使用Composition API，更符合Vue3的设计理念；2. Pinia没有mutations，直接通过actions修改状态；3. Pinia支持TypeScript，提供更好的类型推断；4. Pinia的API更简洁，学习成本更低。',
      level: '高级'
    }
  ]
  
  // 过滤题目
  questions.value = questions.value.filter(q => 
    selectedLevels.value.includes(q.level)
  )
  
  // 重置用户答案和显示状态
  userAnswers.value = new Array(questions.value.length).fill('')
  showAnswers.value = new Array(questions.value.length).fill(false)
}

const submitAnswer = (index: number) => {
  showAnswers.value[index] = true
}
</script>

<style scoped>
.custom-questions {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.back-btn {
  margin-right: 10px;
}

.upload-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.filter-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.questions-section {
  margin-top: 20px;
}

.empty-state {
  text-align: center;
  padding: 50px 0;
}

.question-card {
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-title {
  font-weight: bold;
  font-size: 16px;
}

.question-meta {
  font-size: 14px;
  color: #909399;
}

.question-content {
  margin: 20px 0;
  font-size: 16px;
  line-height: 1.6;
}

.answer-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.quiz-section {
  margin-top: 20px;
}

.correct-answer {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f9eb;
  border-radius: 4px;
  border-left: 4px solid #67c23a;
}
</style>