<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="title-line" v-for="(line, index) in titleLines" :key="index" :style="{ animationDelay: `${index * 0.2}s` }">
              {{ line }}
            </span>
          </h1>
          <p class="hero-subtitle">选择您的面试方向，开始智能学习之旅</p>
        </div>
        <div class="hero-illustration">
          <div class="floating-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
            <div class="shape shape-4"></div>
            <div class="shape shape-5"></div>
          </div>
          <div class="code-window">
            <div class="window-header">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <div class="window-content">
              <div class="code-line" v-for="(line, index) in codeLines" :key="index" :style="{ animationDelay: `${index * 0.3}s` }">
                <span class="code-text">{{ line }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="cards-section">
      <p class="section-title">请选择面试类型</p>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12">
          <el-card class="type-card frontend-card" @click="navigateTo('/frontend')">
            <div class="card-glow"></div>
            <div class="card-icon-wrapper">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </div>
            <h3>前端技术</h3>
            <p class="card-desc">HTML / CSS / JavaScript / TypeScript / Vue / React</p>
            <div class="card-tags">
              <span class="tag">Vue3</span>
              <span class="tag">React</span>
              <span class="tag">TypeScript</span>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12">
          <el-card class="type-card ai-card" @click="navigateTo('/ai-agent')">
            <div class="card-glow"></div>
            <div class="card-icon-wrapper">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" fill="currentColor"/>
                  <path d="M12 5V9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M12 15V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M5 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M15 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
            <h3>AI Agent</h3>
            <p class="card-desc">LLM / ReAct / MCP / Skills / LangChain / RAG</p>
            <div class="card-tags">
              <span class="tag">LangChain</span>
              <span class="tag">RAG</span>
              <span class="tag">MCP</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="features-section">
      <div class="feature-item" v-for="(feature, index) in features" :key="index" :style="{ animationDelay: `${index * 0.15}s` }">
        <div class="feature-icon">{{ feature.icon }}</div>
        <div class="feature-text">
          <h4>{{ feature.title }}</h4>
          <p>{{ feature.desc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const titleLines = ref(['智能面试问答系统', 'AI Powered Interview'])

const codeLines = ref([
  'const interview = new AI();',
  'interview.generate({',
  '  topic: "Frontend",',
  '  level: "Advanced"',
  '});'
])

const features = ref([
  { icon: '🎯', title: '智能生成', desc: 'AI 驱动的题目生成' },
  { icon: '📚', title: '多领域覆盖', desc: '前端、AI Agent 等' },
  { icon: '💡', title: '实时反馈', desc: '即时查看参考答案' }
])

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home {
  min-height: calc(100vh - 100px);
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

/* Hero Section */
.hero-section {
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  animation: patternMove 20s linear infinite;
}

@keyframes patternMove {
  0% { background-position: 0 0; }
  100% { background-position: 60px 60px; }
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  position: relative;
  z-index: 1;
}

.hero-text {
  flex: 1;
}

.hero-title {
  margin: 0 0 20px 0;
  color: white;
}

.title-line {
  display: block;
  font-size: 42px;
  font-weight: 700;
  line-height: 1.3;
  animation: slideInLeft 0.8s ease-out forwards;
  opacity: 0;
}

.title-line:nth-child(2) {
  font-size: 24px;
  font-weight: 400;
  opacity: 0.9;
  margin-top: 10px;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  animation: fadeInUp 0.8s ease-out 0.4s forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Code Window */
.hero-illustration {
  flex: 1;
  display: flex;
  justify-content: center;
  position: relative;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  top: -20px;
  left: 20%;
  animation-delay: 0s;
}

.shape-2 {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  top: 50%;
  right: -10px;
  animation-delay: 1s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.08);
  bottom: -30px;
  left: 10%;
  animation-delay: 2s;
}

.shape-4 {
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.2);
  top: 20%;
  left: -10px;
  animation-delay: 3s;
}

.shape-5 {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.12);
  bottom: 20%;
  right: 20%;
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

.code-window {
  background: rgba(30, 30, 30, 0.95);
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  animation: windowAppear 0.8s ease-out 0.3s forwards;
  opacity: 0;
  transform: translateY(30px);
}

@keyframes windowAppear {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.window-header {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(60, 60, 60, 0.5);
  border-radius: 12px 12px 0 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ff5f57; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #28ca42; }

.window-content {
  padding: 20px;
}

.code-line {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.8;
  animation: typeIn 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes typeIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.code-text {
  color: #e6e6e6;
}

.code-line:nth-child(1) .code-text { color: #c678dd; }
.code-line:nth-child(2) .code-text { color: #e5c07b; }
.code-line:nth-child(3) .code-text { color: #98c379; }
.code-line:nth-child(4) .code-text { color: #61afef; }
.code-line:nth-child(5) .code-text { color: #c678dd; }

/* Cards Section */
.cards-section {
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 30px;
  animation: fadeIn 0.8s ease-out 0.6s forwards;
  opacity: 0;
}

@keyframes fadeIn {
  to { opacity: 1; }
}

.type-card {
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: none;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  animation: cardSlideUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
}

.type-card:nth-child(1) { animation-delay: 0.7s; }
.type-card:nth-child(2) { animation-delay: 0.85s; }

@keyframes cardSlideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.type-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #409EFF, #67c23a);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.type-card:hover .card-glow {
  transform: scaleX(1);
}

.frontend-card .card-glow {
  background: linear-gradient(90deg, #409EFF, #66b1ff);
}

.ai-card .card-glow {
  background: linear-gradient(90deg, #764ba2, #667eea);
}

.card-icon-wrapper {
  padding: 30px 0 20px;
  display: flex;
  justify-content: center;
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s ease;
}

.frontend-card .card-icon {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  color: white;
}

.ai-card .card-icon {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
}

.card-icon svg {
  width: 40px;
  height: 40px;
}

.type-card:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
}

.type-card h3 {
  margin: 0 0 10px 0;
  font-size: 22px;
  font-weight: 600;
  color: #303133;
  text-align: center;
}

.card-desc {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #909399;
  text-align: center;
  padding: 0 20px;
}

.card-tags {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 0 20px 25px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 12px;
  background: #f5f7fa;
  border-radius: 12px;
  font-size: 12px;
  color: #606266;
  transition: all 0.3s ease;
}

.type-card:hover .tag {
  background: #ecf5ff;
  color: #409EFF;
}

/* Features Section */
.features-section {
  padding: 20px 20px 40px;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  animation: featureFadeIn 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes featureFadeIn {
  to { opacity: 1; }
}

.feature-icon {
  font-size: 32px;
}

.feature-text h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #303133;
}

.feature-text p {
  margin: 0;
  font-size: 13px;
  color: #909399;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .title-line {
    font-size: 28px;
  }

  .title-line:nth-child(2) {
    font-size: 16px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .hero-illustration {
    width: 100%;
  }

  .code-window {
    max-width: 100%;
  }

  .section-title {
    font-size: 20px;
  }

  .type-card {
    margin-bottom: 15px;
  }

  .card-icon {
    width: 60px;
    height: 60px;
  }

  .card-icon svg {
    width: 30px;
    height: 30px;
  }

  .type-card h3 {
    font-size: 18px;
  }

  .features-section {
    flex-direction: column;
    gap: 15px;
  }

  .feature-item {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 30px 15px;
  }

  .title-line {
    font-size: 24px;
  }

  .code-line {
    font-size: 11px;
  }

  .cards-section {
    padding: 30px 15px;
  }

  .card-desc {
    font-size: 12px;
  }

  .tag {
    font-size: 11px;
    padding: 3px 10px;
  }
}
</style>
