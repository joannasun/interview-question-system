# 面试问答系统

一个针对前端技术和AI Agent的面试问答系统，支持查看模式和问答模式，可根据用户需求自定义题目方向和难度级别。

## 技术栈

- **前端**：Vue 3 + TypeScript + Element Plus + Vite
- **后端**：Python + FastAPI

## 功能特性

1. **题目分类**：
   - 前端技术：HTML、CSS、JavaScript、TypeScript、Vue、React
   - AI Agent：LLM、ReAct、MCP、Skills、LangChain、RAG、Memory、Context
   - 自定义：上传图片或TXT文档

2. **难度级别**：
   - 初级
   - 中级
   - 高级

3. **模式选择**：
   - 查看模式：显示问题及完整答案
   - 问答模式：显示问题，支持用户输入答案

## 项目结构

```
interview-system/
├── frontend/           # 前端项目
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── router/      # 路由
│   │   ├── api/         # API调用
│   │   ├── types/       # TypeScript类型定义
│   │   ├── App.vue      # 根组件
│   │   └── main.ts      # 入口文件
│   ├── package.json     # 依赖配置
│   ├── tsconfig.json    # TypeScript配置
│   ├── vite.config.ts   # Vite配置
│   └── index.html       # HTML入口
├── backend/            # 后端项目
│   ├── uploads/         # 上传文件目录
│   ├── app.py           # FastAPI应用入口
│   ├── routes.py        # API路由
│   └── requirements.txt # 依赖配置
└── README.md           # 项目说明
```

## 运行指南

### 前端

1. 进入前端目录：
   ```bash
   cd frontend
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动开发服务器：
   ```bash
   npm run dev
   ```

4. 构建生产版本：
   ```bash
   npm run build
   ```

### 后端

1. 进入后端目录：
   ```bash
   cd backend
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 启动后端服务器：
   ```bash
   python app.py
   ```

## API接口

- **GET /api/frontend-questions**：获取前端技术面试题
  - 参数：
    - levels：难度级别，多个级别用逗号分隔（如 "初级,中级"）
    - technologies：技术类型，多个类型用逗号分隔（如 "HTML,CSS"）

- **GET /api/ai-agent-questions**：获取AI Agent面试题
  - 参数：
    - levels：难度级别，多个级别用逗号分隔
    - technologies：技术类型，多个类型用逗号分隔

- **POST /api/upload**：上传文件
  - 支持 .txt、.jpg、.jpeg、.png 文件

## 注意事项

- 后端服务器默认运行在 http://localhost:8000
- 前端开发服务器默认运行在 http://localhost:3000
- 上传的文件会保存在 backend/uploads/ 目录
- 目前系统使用模拟数据，实际部署时需要替换为真实的数据库存储