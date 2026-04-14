from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from rag_service import rag_service
from llm_service import llm_service
import os
import tempfile

router = APIRouter()

class Question(BaseModel):
    id: int
    question: str
    answer: str
    level: str
    technology: Optional[str] = None

class QuestionRequest(BaseModel):
    topic: str
    levels: List[str]
    technologies: List[str]
    user_input: Optional[str] = None
    page: int = 1
    page_size: int = 10
    count: int = 10

class QuestionResponse(BaseModel):
    questions: List[Question]
    total: int
    page: int
    page_size: int
    total_pages: int

class LoadPDFRequest(BaseModel):
    pass

@router.on_event("startup")
async def startup_event():
    print("Checking vectorstore status...")
    if rag_service.has_data():
        doc_count = rag_service.get_document_count()
        print(f"Vectorstore already exists with {doc_count} documents")
    else:
        print("No vectorstore found, loading PDFs...")
        results = rag_service.load_all_pdfs()
        print(f"PDF loading results: {results}")

@router.post("/api/questions/generate", response_model=QuestionResponse)
def generate_questions(request: QuestionRequest):
    context = None
    topic_filter = "frontend" if request.topic == "前端技术" else "ai_agent"
    
    if request.user_input:
        context = rag_service.search(request.user_input, k=2, topic=topic_filter)
    elif rag_service.has_data():
        context = rag_service.search(
            f"{request.topic} {' '.join(request.technologies[:3])}", 
            k=2,
            topic=topic_filter
        )
    
    if context:
        context = [c[:300] for c in context]
    
    all_questions = llm_service.generate_questions(
        topic=request.topic,
        levels=request.levels,
        technologies=request.technologies,
        user_input=request.user_input,
        context=context,
        count=request.count
    )
    
    total = len(all_questions)
    start_idx = (request.page - 1) * request.page_size
    end_idx = start_idx + request.page_size
    paginated_questions = all_questions[start_idx:end_idx]
    
    total_pages = (total + request.page_size - 1) // request.page_size
    
    return QuestionResponse(
        questions=[Question(**q) for q in paginated_questions],
        total=total,
        page=request.page,
        page_size=request.page_size,
        total_pages=total_pages
    )

@router.post("/api/questions/generate-stream")
async def generate_questions_stream(request: QuestionRequest):
    context = None
    topic_filter = "frontend" if request.topic == "前端技术" else "ai_agent"
    
    if request.user_input:
        context = rag_service.search(request.user_input, k=2, topic=topic_filter)
    elif rag_service.has_data():
        context = rag_service.search(
            f"{request.topic} {' '.join(request.technologies[:3])}", 
            k=2,
            topic=topic_filter
        )
    
    if context:
        context = [c[:300] for c in context]
    
    def event_generator():
        for chunk in llm_service.generate_questions_stream(
            topic=request.topic,
            levels=request.levels,
            technologies=request.technologies,
            user_input=request.user_input,
            context=context,
            count=request.count
        ):
            yield chunk
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/api/questions/load-pdf")
def load_pdf_files(force: bool = False):
    results = rag_service.load_all_pdfs(force_reload=force)
    total_chunks = sum(results.values())
    return {
        "message": f"成功加载PDF文件，共{total_chunks}个新文本块" if total_chunks > 0 else "没有新的PDF文件需要处理",
        "details": results,
        "total_chunks": total_chunks
    }

@router.post("/api/questions/clear")
def clear_vectorstore():
    success = rag_service.clear_vectorstore()
    if success:
        return {"message": "向量库已清空"}
    else:
        raise HTTPException(status_code=500, detail="清空向量库失败")

@router.post("/api/questions/clear-cache")
def clear_cache():
    success = rag_service.clear_cache()
    if success:
        return {"message": "缓存已清空"}
    else:
        raise HTTPException(status_code=500, detail="清空缓存失败")

@router.get("/api/questions/status")
def get_rag_status():
    doc_count = rag_service.get_document_count()
    cache_stats = rag_service.get_cache_stats()
    return {
        "has_data": rag_service.has_data(),
        "document_count": doc_count,
        "cache_stats": cache_stats,
        "message": f"RAG系统已就绪，共{doc_count}个文档块" if rag_service.has_data() else "请先加载PDF文件"
    }

@router.get("/api/frontend-questions", response_model=QuestionResponse)
def get_frontend_questions(
    levels: Optional[str] = None, 
    technologies: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    count: int = 10
):
    if rag_service.has_data():
        context = rag_service.search(
            f"前端技术面试题 {' '.join(technologies.split(',')) if technologies else ''}",
            k=5,
            topic="frontend"
        )
        
        all_questions = llm_service.generate_questions(
            topic="前端技术",
            levels=levels.split(",") if levels else ["初级", "中级", "高级"],
            technologies=technologies.split(",") if technologies else ["HTML", "CSS", "JavaScript", "TypeScript", "Vue", "React"],
            context=context,
            count=count
        )
    else:
        all_questions = _get_default_frontend_questions()
    
    if levels:
        level_list = levels.split(",")
        all_questions = [q for q in all_questions if q["level"] in level_list]
    
    if technologies:
        tech_list = technologies.split(",")
        all_questions = [q for q in all_questions if q.get("technology") in tech_list]
    
    total = len(all_questions)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_questions = all_questions[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size
    
    return QuestionResponse(
        questions=[Question(**q) for q in paginated_questions],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/api/ai-agent-questions", response_model=QuestionResponse)
def get_ai_agent_questions(
    levels: Optional[str] = None, 
    technologies: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    count: int = 10
):
    if rag_service.has_data():
        context = rag_service.search(
            f"AI Agent面试题 {' '.join(technologies.split(',')) if technologies else ''}",
            k=5,
            topic="ai_agent"
        )
        
        all_questions = llm_service.generate_questions(
            topic="AI Agent",
            levels=levels.split(",") if levels else ["初级", "中级", "高级"],
            technologies=technologies.split(",") if technologies else ["LLM", "ReAct", "MCP", "Skills", "LangChain", "RAG", "Memory", "Context"],
            context=context,
            count=count
        )
    else:
        all_questions = _get_default_ai_agent_questions()
    
    if levels:
        level_list = levels.split(",")
        all_questions = [q for q in all_questions if q["level"] in level_list]
    
    if technologies:
        tech_list = technologies.split(",")
        all_questions = [q for q in all_questions if q.get("technology") in tech_list]
    
    total = len(all_questions)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_questions = all_questions[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size
    
    return QuestionResponse(
        questions=[Question(**q) for q in paginated_questions],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

def _get_default_frontend_questions():
    return [
        {
            "id": 1,
            "question": "什么是HTML5的语义化标签？它们有什么作用？",
            "answer": "HTML5的语义化标签是指具有特定含义的标签，如<header>、<nav>、<main>、<section>、<article>、<footer>等。它们的作用是：1. 提高代码的可读性和可维护性；2. 有利于搜索引擎优化(SEO)；3. 改善无障碍访问性。",
            "level": "初级",
            "technology": "HTML"
        },
        {
            "id": 2,
            "question": "CSS中的盒模型是什么？标准盒模型和IE盒模型有什么区别？",
            "answer": "CSS盒模型是指元素在页面中所占的空间，包括内容(content)、内边距(padding)、边框(border)和外边距(margin)。标准盒模型的width和height只包含内容区域，而IE盒模型的width和height包含内容、内边距和边框。",
            "level": "中级",
            "technology": "CSS"
        },
        {
            "id": 3,
            "question": "JavaScript中的闭包是什么？它有什么作用和缺点？",
            "answer": "闭包是指函数能够访问其词法作用域之外的变量。作用：1. 保护变量不被外部访问；2. 实现数据私有化；3. 延长变量的生命周期。缺点：1. 可能导致内存泄漏；2. 增加代码复杂度。",
            "level": "中级",
            "technology": "JavaScript"
        },
        {
            "id": 4,
            "question": "TypeScript中的泛型是什么？它有什么作用？",
            "answer": "泛型是TypeScript中允许在定义函数、接口或类时使用类型参数的特性。作用：1. 提高代码的复用性；2. 增强类型安全性；3. 使代码更加灵活。",
            "level": "中级",
            "technology": "TypeScript"
        },
        {
            "id": 5,
            "question": "Vue3中的Composition API与Options API有什么区别？",
            "answer": "Composition API是Vue3引入的新API风格，与Options API的区别：1. 组织代码的方式不同，Composition API按功能组织代码，Options API按选项组织代码；2. Composition API提供了更好的TypeScript支持；3. Composition API更适合复杂组件的逻辑复用。",
            "level": "高级",
            "technology": "Vue"
        },
        {
            "id": 6,
            "question": "React中的Hooks是什么？它们解决了什么问题？",
            "answer": "Hooks是React 16.8引入的新特性，允许在函数组件中使用状态和其他React特性。解决的问题：1. 组件之间逻辑复用困难；2. 复杂组件的逻辑分散在不同生命周期方法中；3. class组件的this指向问题。",
            "level": "高级",
            "technology": "React"
        }
    ]

def _get_default_ai_agent_questions():
    return [
        {
            "id": 1,
            "question": "什么是LLM？它的主要特点是什么？",
            "answer": "LLM是Large Language Model的缩写，指大型语言模型。主要特点包括：1. 参数量大，通常数十亿到数千亿参数；2. 能够理解和生成自然语言；3. 具有广泛的知识覆盖；4. 能够执行多种语言任务，如问答、翻译、摘要等。",
            "level": "初级",
            "technology": "LLM"
        },
        {
            "id": 2,
            "question": "ReAct框架是什么？它的工作原理是什么？",
            "answer": "ReAct是一种将推理(Reasoning)和行动(Action)相结合的AI Agent框架。工作原理：1. Agent通过思考(Thought)分析问题；2. 基于思考选择行动(Action)；3. 执行行动获取观察(Observation)；4. 根据观察更新状态，重复上述过程直到问题解决。",
            "level": "中级",
            "technology": "ReAct"
        },
        {
            "id": 3,
            "question": "MCP是什么？它在AI Agent中起到什么作用？",
            "answer": "MCP是Model Context Protocol的缩写，是一种允许AI模型与外部工具和服务交互的协议。作用：1. 扩展AI模型的能力；2. 允许模型访问实时信息；3. 实现与外部系统的集成；4. 提高Agent的实用性和灵活性。",
            "level": "中级",
            "technology": "MCP"
        },
        {
            "id": 4,
            "question": "什么是AI Agent的Skills？如何开发和管理Skills？",
            "answer": "Skills是AI Agent可以执行的特定功能或能力。开发和管理Skills的方法：1. 定义明确的输入和输出接口；2. 实现具体的功能逻辑；3. 注册到Agent的技能库中；4. 提供适当的文档和示例；5. 定期更新和维护Skills。",
            "level": "中级",
            "technology": "Skills"
        },
        {
            "id": 5,
            "question": "LangChain是什么？它的主要组件有哪些？",
            "answer": "LangChain是一个用于构建基于LLM的应用程序的框架。主要组件包括：1. Chains：将多个步骤组合在一起；2. Agents：基于用户输入和环境做出决策；3. Memory：存储和管理对话历史；4. Retrievers：从外部数据源获取信息；5. Tools：与外部系统交互的接口。",
            "level": "高级",
            "technology": "LangChain"
        },
        {
            "id": 6,
            "question": "RAG是什么？它如何增强LLM的能力？",
            "answer": "RAG是Retrieval-Augmented Generation的缩写，指检索增强生成。它通过以下方式增强LLM的能力：1. 从外部知识库检索相关信息；2. 将检索到的信息与用户查询一起输入给LLM；3. 使LLM能够基于最新、准确的信息生成回答；4. 减少LLM的 hallucination（幻觉）问题。",
            "level": "高级",
            "technology": "RAG"
        },
        {
            "id": 7,
            "question": "AI Agent中的Memory是什么？它有哪些类型？",
            "answer": "Memory是AI Agent存储和管理信息的能力。主要类型包括：1. 短期记忆：存储当前对话的上下文；2. 长期记忆：存储历史对话和重要信息；3. 知识记忆：存储结构化的知识库信息；4. 情境记忆：存储特定情境下的经验和决策。",
            "level": "高级",
            "technology": "Memory"
        },
        {
            "id": 8,
            "question": "Context在AI Agent中起到什么作用？如何有效管理Context？",
            "answer": "Context是AI Agent理解和响应用户请求的背景信息。作用：1. 帮助Agent理解用户意图；2. 提供相关的历史信息；3. 指导Agent的决策过程。有效管理Context的方法：1. 合理设置Context窗口大小；2. 优先保留重要信息；3. 使用摘要技术压缩信息；4. 实现Context的层次化管理。",
            "level": "高级",
            "technology": "Context"
        }
    ]

@router.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.txt', '.jpg', '.jpeg', '.png', '.pdf')):
        raise HTTPException(status_code=400, detail="只支持 .txt、.jpg、.jpeg、.png、.pdf 文件")
    
    import os
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"filename": file.filename, "message": "文件上传成功"}


class TranscriptionResponse(BaseModel):
    text: str
    success: bool
    error: Optional[str] = None

_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        import imageio_ffmpeg
        import os
        import shutil
        
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        
        if not os.path.exists(ffmpeg_exe):
            shutil.copy(ffmpeg_path, ffmpeg_exe)
        
        current_path = os.environ.get("PATH", "")
        if ffmpeg_dir not in current_path:
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + current_path
        
        import whisper
        _whisper_model = whisper.load_model("base")
    return _whisper_model

@router.post("/api/speech/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_content = await audio.read()
        
        print(f"收到音频文件: {audio.filename}, 大小: {len(audio_content)} bytes")
        
        if len(audio_content) == 0:
            return TranscriptionResponse(
                text="",
                success=False,
                error="音频文件为空"
            )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            temp_file.write(audio_content)
            temp_file_path = temp_file.name
        
        wav_path = temp_file_path.replace(".webm", ".wav")
        
        try:
            import subprocess
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            print(f"使用 ffmpeg: {ffmpeg_exe}")
            print(f"转换音频: {temp_file_path} -> {wav_path}")
            
            result = subprocess.run(
                [ffmpeg_exe, "-y", "-i", temp_file_path, "-ar", "16000", "-ac", "1", wav_path],
                capture_output=True,
                text=True
            )
            
            print(f"ffmpeg stdout: {result.stdout}")
            print(f"ffmpeg stderr: {result.stderr}")
            
            if result.returncode != 0:
                return TranscriptionResponse(
                    text="",
                    success=False,
                    error=f"音频转换失败: {result.stderr}"
                )
            
            wav_size = os.path.getsize(wav_path)
            print(f"wav 文件大小: {wav_size} bytes")
            
            model = get_whisper_model()
            print("开始 Whisper 识别...")
            transcribe_result = model.transcribe(wav_path, language="zh")
            
            text = transcribe_result["text"]
            
            import zhconv
            text = zhconv.convert(text, "zh-cn")
            
            print(f"识别结果: {text}")
            
            return TranscriptionResponse(
                text=text,
                success=True
            )
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            if os.path.exists(wav_path):
                os.unlink(wav_path)
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        return TranscriptionResponse(
            text="",
            success=False,
            error=str(e)
        )
