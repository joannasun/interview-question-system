<template>
  <div class="app">
    <el-container>
      <el-header height="60px" class="header">
        <h1 class="title">智能面试问答系统</h1>
      </el-header>
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
      <el-footer height="40px" class="footer">
        <p>© 2026 智能面试问答系统</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 1px;
  animation: titleFadeIn 0.8s ease-out;
}

@keyframes titleFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-content {
  flex: 1;
  overflow-y: auto;
  margin-top: 60px;
  margin-bottom: 40px;
  padding: 0;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #909399;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.05);
}

/* 页面切换动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .header {
    height: 50px !important;
    padding: 0 15px;
  }

  .title {
    font-size: 16px;
  }

  .main-content {
    margin-top: 50px;
    margin-bottom: 35px;
  }

  .footer {
    height: 35px !important;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .header {
    height: 45px !important;
    padding: 0 10px;
  }

  .title {
    font-size: 14px;
  }

  .main-content {
    margin-top: 45px;
    margin-bottom: 30px;
  }

  .footer {
    height: 30px !important;
    font-size: 11px;
  }
}
</style>
