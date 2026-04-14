import os
import json
import time
from typing import List, Dict, Optional, Generator
from langchain_community.chat_models import ChatTongyi

class LLMService:
    def __init__(self):
        self._llm = None
        self._api_key = None
    
    def _get_llm(self):
        if self._llm is None:
            api_key = os.environ.get("QIANWEN-API-KEY", "") or os.environ.get("QIANWEN_API_KEY", "")
            if api_key:
                self._api_key = api_key
                self._llm = ChatTongyi(
                    model="qwen-turbo",
                    dashscope_api_key=api_key,
                    temperature=0.7,
                    streaming=True
                )
                print(f"LLM initialized successfully with API key: {api_key[:8]}...")
            else:
                print("No API key found in environment variables (QIANWEN-API-KEY or QIANWEN_API_KEY)")
        return self._llm
    
    def generate_questions(
        self,
        topic: str,
        levels: List[str],
        technologies: List[str],
        user_input: Optional[str] = None,
        context: Optional[List[str]] = None,
        count: int = 10
    ) -> List[Dict]:
        start_time = time.time()
        
        prompt = self._build_prompt(topic, levels, technologies, user_input, context, count)
        print(f"[LLM] Prompt length: {prompt[:100]}... chars")
        
        llm = self._get_llm()
        if not llm:
            print("LLM not initialized, using default questions")
            return self._get_default_questions(topic, levels, technologies)
        
        try:
            response = llm.invoke(prompt)
            result_text = response.content
            elapsed = time.time() - start_time
            print(f"[LLM] Response time: {elapsed:.2f}s")
            
            questions = self._parse_response(result_text)
            if questions:
                return questions
            
            return self._get_default_questions(topic, levels, technologies)
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._get_default_questions(topic, levels, technologies)
    
    def generate_questions_stream(
        self,
        topic: str,
        levels: List[str],
        technologies: List[str],
        user_input: Optional[str] = None,
        context: Optional[List[str]] = None,
        count: int = 10
    ) -> Generator[str, None, None]:
        prompt = self._build_prompt(topic, levels, technologies, user_input, context, count)
        print(f"[LLM Stream] Prompt length: {prompt[:100]}... chars")
        
        llm = self._get_llm()
        if not llm:
            defaults = self._get_default_questions(topic, levels, technologies)
            yield f"data: {json.dumps({'type': 'questions', 'data': defaults}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
            return
        
        try:
            full_response = ""
            for chunk in llm.stream(prompt):
                if chunk.content:
                    full_response += chunk.content
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk.content}, ensure_ascii=False)}\n\n"
            
            questions = self._parse_response(full_response)
            if not questions:
                questions = self._get_default_questions(topic, levels, technologies)
            
            yield f"data: {json.dumps({'type': 'questions', 'data': questions}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            print(f"Error in stream: {e}")
            defaults = self._get_default_questions(topic, levels, technologies)
            yield f"data: {json.dumps({'type': 'questions', 'data': defaults}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
    
    def _build_prompt(
        self,
        topic: str,
        levels: List[str],
        technologies: List[str],
        user_input: Optional[str],
        context: Optional[List[str]],
        count: int
    ) -> str:
        parts = [
            f"生成{count}道{topic}面试题。",
            f"难度：{', '.join(levels)}",
            f"技术：{', '.join(technologies[:5])}"
        ]
        
        if user_input:
            parts.append(f"重点：{user_input}")
        
        if context:
            context_text = ' | '.join(context[:2])
            parts.append(f"参考：{context_text[:200]}")
        
        parts.append(f"返回JSON数组，每个JSON数组，每个元素包含id/question/answer/level/technology， 生成数组数量和{count}一致，如果{user_input}优先生成{user_input}相关的面试题")
        
        return '\n'.join(parts)
    
    def _parse_response(self, response_text: str) -> List[Dict]:
        try:
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
        
        return []
    
    def _get_default_questions(
        self,
        topic: str,
        levels: List[str],
        technologies: List[str]
    ) -> List[Dict]:
        if topic == "前端技术":
            return self._get_frontend_defaults(levels, technologies)
        else:
            return self._get_ai_agent_defaults(levels, technologies)
    
    def _get_frontend_defaults(self, levels: List[str], technologies: List[str]) -> List[Dict]:
        questions = [
            {"id": 1, "question": "什么是HTML5语义化标签？", "answer": "HTML5语义化标签如header、nav、section等，提高代码可读性和SEO。", "level": "初级", "technology": "HTML"},
            {"id": 2, "question": "CSS盒模型是什么？", "answer": "盒模型包含content、padding、border、margin。标准盒模型width只含content，IE含padding+border。", "level": "初级", "technology": "CSS"},
            {"id": 3, "question": "JavaScript闭包是什么？", "answer": "闭包是能访问外部变量的函数，用于数据私有化和延长变量生命周期。", "level": "中级", "technology": "JavaScript"},
            {"id": 4, "question": "TypeScript泛型是什么？", "answer": "泛型允许定义时使用类型参数，提高代码复用性和类型安全。", "level": "中级", "technology": "TypeScript"},
            {"id": 5, "question": "Vue3 Composition API区别？", "answer": "Composition API按功能组织代码，更好的TS支持，适合逻辑复用。", "level": "高级", "technology": "Vue"},
            {"id": 6, "question": "React Hooks是什么？", "answer": "Hooks让函数组件使用状态，解决逻辑复用和this指向问题。", "level": "高级", "technology": "React"}
        ]
        return [q for q in questions if q["level"] in levels and q["technology"] in technologies]
    
    def _get_ai_agent_defaults(self, levels: List[str], technologies: List[str]) -> List[Dict]:
        questions = [
            {"id": 1, "question": "什么是LLM？", "answer": "大型语言模型，数十亿参数，能理解和生成自然语言。", "level": "初级", "technology": "LLM"},
            {"id": 2, "question": "ReAct框架是什么？", "answer": "推理+行动结合的AI Agent框架，通过思考-行动-观察循环解决问题。", "level": "中级", "technology": "ReAct"},
            {"id": 3, "question": "MCP是什么？", "answer": "Model Context Protocol，允许AI与外部工具和服务交互的协议。", "level": "中级", "technology": "MCP"},
            {"id": 4, "question": "AI Agent Skills是什么？", "answer": "Agent可执行的特定功能或能力，需定义输入输出接口。", "level": "中级", "technology": "Skills"},
            {"id": 5, "question": "LangChain是什么？", "answer": "构建LLM应用的框架，主要组件包括Chains、Agents、Memory、Tools。", "level": "高级", "technology": "LangChain"},
            {"id": 6, "question": "RAG是什么？", "answer": "检索增强生成，从外部知识库检索信息输入给LLM，减少幻觉。", "level": "高级", "technology": "RAG"},
            {"id": 7, "question": "Memory类型有哪些？", "answer": "短期记忆、长期记忆、知识记忆、情境记忆。", "level": "高级", "technology": "Memory"},
            {"id": 8, "question": "Context管理方法？", "answer": "设置窗口大小、保留重要信息、使用摘要压缩、实现层次化管理。", "level": "高级", "technology": "Context"}
        ]
        return [q for q in questions if q["level"] in levels and q["technology"] in technologies]

    def generate_questions_from_prompt(self, prompt: str, count: int = 10) -> List[Dict]:
        start_time = time.time()
        
        print(f"[LLM] Generating {count} questions from custom prompt...")
        
        llm = self._get_llm()
        if not llm:
            print("LLM not initialized, returning empty list")
            return []
        
        try:
            response = llm.invoke(prompt)
            result_text = response.content
            elapsed = time.time() - start_time
            print(f"[LLM] Response time: {elapsed:.2f}s")
            
            questions = self._parse_response(result_text)
            if questions:
                return questions[:count]
            
            return []
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return []

llm_service = LLMService()
