import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/frontend',
    name: 'frontend',
    component: () => import('../views/FrontendQuestions.vue')
  },
  {
    path: '/ai-agent',
    name: 'aiAgent',
    component: () => import('../views/AIAgentQuestions.vue')
  },
  {
    path: '/custom',
    name: 'custom',
    component: () => import('../views/CustomQuestions.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router