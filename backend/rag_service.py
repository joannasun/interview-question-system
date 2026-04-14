import os
import json
import pickle
import asyncio
import aiofiles
from typing import List, Optional, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FE_DATA_DIR = os.path.join(DATA_DIR, "fe")
AI_DATA_DIR = os.path.join(DATA_DIR, "ai")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
TEXT_CACHE_DIR = os.path.join(CACHE_DIR, "texts")
VECTOR_CACHE_DIR = os.path.join(CACHE_DIR, "vectors")
PROCESSED_FILES_PATH = os.path.join(BASE_DIR, "processed_files.json")

MAX_WORKERS = 10
BATCH_SIZE = 20

class RAGService:
    def __init__(self):
        self._embeddings = None
        self.vectorstore: Optional[Chroma] = None
        self._initialized = False
        self._processed_files = self._load_processed_files()
        self._ensure_cache_dirs()
    
    def _ensure_cache_dirs(self):
        for dir_path in [CACHE_DIR, TEXT_CACHE_DIR, VECTOR_CACHE_DIR, CHROMA_DIR]:
            os.makedirs(dir_path, exist_ok=True)
    
    def _load_processed_files(self) -> dict:
        if os.path.exists(PROCESSED_FILES_PATH):
            try:
                with open(PROCESSED_FILES_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_processed_files(self):
        try:
            with open(PROCESSED_FILES_PATH, 'w', encoding='utf-8') as f:
                json.dump(self._processed_files, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving processed files: {e}")
    
    def _get_file_hash(self, file_path: str) -> str:
        try:
            return f"{os.path.basename(file_path)}_{os.path.getsize(file_path)}_{int(os.path.getmtime(file_path))}"
        except:
            return os.path.basename(file_path)
    
    def _get_text_cache_path(self, file_path: str) -> str:
        file_hash = self._get_file_hash(file_path)
        safe_name = file_hash.replace(':', '_').replace('\\', '_').replace('/', '_')
        return os.path.join(TEXT_CACHE_DIR, f"{safe_name}.json")
    
    def _get_vector_cache_path(self, file_path: str) -> str:
        file_hash = self._get_file_hash(file_path)
        safe_name = file_hash.replace(':', '_').replace('\\', '_').replace('/', '_')
        return os.path.join(VECTOR_CACHE_DIR, f"{safe_name}.pkl")
    
    def _get_embeddings(self):
        if self._embeddings is None:
            api_key = os.environ.get("QIANWEN_API_KEY") or os.environ.get("QIANWEN-API-KEY")
            if api_key:
                self._embeddings = DashScopeEmbeddings(
                    dashscope_api_key=api_key,
                    model="text-embedding-v1"
                )
                print("Embeddings initialized successfully")
            else:
                print("No API key found for embeddings")
        return self._embeddings
    
    def _load_text_cache(self, file_path: str) -> Optional[List[dict]]:
        cache_path = self._get_text_cache_path(file_path)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def _save_text_cache(self, file_path: str, chunks: List[dict]):
        cache_path = self._get_text_cache_path(file_path)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving text cache: {e}")
    
    def _load_vector_cache(self, file_path: str) -> Optional[Tuple[List[str], List[List[float]]]]:
        cache_path = self._get_vector_cache_path(file_path)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except:
                pass
        return None
    
    def _save_vector_cache(self, file_path: str, texts: List[str], vectors: List[List[float]]):
        cache_path = self._get_vector_cache_path(file_path)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump((texts, vectors), f)
        except Exception as e:
            print(f"Error saving vector cache: {e}")
    
    def _init_vectorstore(self):
        if self._initialized:
            return
        
        embeddings = self._get_embeddings()
        if not embeddings:
            print("Cannot initialize vectorstore without embeddings")
            return
        
        if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
            try:
                self.vectorstore = Chroma(
                    persist_directory=CHROMA_DIR,
                    embedding_function=embeddings
                )
                count = self.vectorstore._collection.count()
                print(f"Vectorstore loaded from disk, {count} documents")
            except Exception as e:
                print(f"Error loading vectorstore: {e}")
                self.vectorstore = None
        
        self._initialized = True
    
    def _should_process_file(self, file_path: str, topic: str) -> bool:
        file_hash = self._get_file_hash(file_path)
        key = f"{topic}_{os.path.basename(file_path)}"
        return self._processed_files.get(key) != file_hash
    
    def _mark_file_processed(self, file_path: str, topic: str):
        file_hash = self._get_file_hash(file_path)
        key = f"{topic}_{os.path.basename(file_path)}"
        self._processed_files[key] = file_hash
        self._save_processed_files()
    
    def _parse_pdf(self, pdf_path: str, topic: str) -> List[dict]:
        cached = self._load_text_cache(pdf_path)
        if cached:
            print(f"  [Cache Hit] Text: {os.path.basename(pdf_path)}")
            return cached
        
        print(f"  [Parsing] {os.path.basename(pdf_path)}")
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)
            
            chunks = []
            for i, split in enumerate(splits):
                chunks.append({
                    "id": i,
                    "text": split.page_content,
                    "metadata": {
                        "topic": topic,
                        "source_file": os.path.basename(pdf_path),
                        "page": split.metadata.get("page", 0)
                    }
                })
            
            self._save_text_cache(pdf_path, chunks)
            return chunks
        except Exception as e:
            print(f"  [Error] Parsing {pdf_path}: {e}")
            return []
    
    def _embed_texts_batch(self, texts: List[str], embeddings) -> List[List[float]]:
        cached_vectors = self._load_vector_cache_from_texts(texts)
        if cached_vectors:
            return cached_vectors
        
        all_vectors = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            try:
                vectors = embeddings.embed_documents(batch)
                all_vectors.extend(vectors)
                print(f"    Embedded batch {i//BATCH_SIZE + 1}/{(len(texts)-1)//BATCH_SIZE + 1}")
            except Exception as e:
                print(f"    Error embedding batch: {e}")
                all_vectors.extend([[0.0] * 1536 for _ in batch])
        
        return all_vectors
    
    def _load_vector_cache_from_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        return None
    
    def _embed_texts_concurrent(self, texts: List[str], embeddings) -> List[List[float]]:
        def embed_batch(batch):
            try:
                return embeddings.embed_documents(batch)
            except Exception as e:
                print(f"    Error in batch: {e}")
                return [[0.0] * 1536 for _ in batch]
        
        all_vectors = []
        batches = [texts[i:i + BATCH_SIZE] for i in range(0, len(texts), BATCH_SIZE)]
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(embed_batch, batch) for batch in batches]
            
            for i, future in enumerate(futures):
                try:
                    vectors = future.result(timeout=60)
                    all_vectors.extend(vectors)
                    print(f"    Embedded batch {i + 1}/{len(batches)}")
                except Exception as e:
                    print(f"    Error getting batch {i + 1}: {e}")
                    all_vectors.extend([[0.0] * 1536 for _ in batches[i]])
        
        return all_vectors
    
    def _process_single_pdf(self, pdf_path: str, topic: str, use_cache: bool = True) -> Tuple[List[str], List[dict], List[List[float]]]:
        vector_cache = self._load_vector_cache(pdf_path) if use_cache else None
        if vector_cache:
            texts, vectors = vector_cache
            print(f"  [Cache Hit] Vector: {os.path.basename(pdf_path)} ({len(texts)} chunks)")
            chunks = [{"text": t, "metadata": {"topic": topic}} for t in texts]
            return texts, chunks, vectors
        
        chunks = self._parse_pdf(pdf_path, topic)
        if not chunks:
            return [], [], []
        
        texts = [c["text"] for c in chunks]
        embeddings = self._get_embeddings()
        
        if embeddings:
            vectors = self._embed_texts_concurrent(texts, embeddings)
            self._save_vector_cache(pdf_path, texts, vectors)
        else:
            vectors = []
        
        return texts, chunks, vectors
    
    def load_pdfs_from_directory(self, directory: str, topic: str = "general", 
                                  force_reload: bool = False, use_cache: bool = True) -> int:
        embeddings = self._get_embeddings()
        if not embeddings:
            print("Cannot load PDFs without embeddings")
            return 0
        
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            os.makedirs(directory, exist_ok=True)
            return 0
        
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"No PDF files found in {directory}")
            return 0
        
        if not force_reload:
            files_to_process = [
                f for f in pdf_files 
                if self._should_process_file(os.path.join(directory, f), topic)
            ]
        else:
            files_to_process = pdf_files
        
        if not files_to_process:
            print(f"All PDF files in {directory} already processed")
            return 0
        
        print(f"Processing {len(files_to_process)} PDF files in {directory}")
        
        all_texts = []
        all_metadatas = []
        all_vectors = []
        
        for pdf_file in files_to_process:
            pdf_path = os.path.join(directory, pdf_file)
            texts, chunks, vectors = self._process_single_pdf(pdf_path, topic, use_cache)
            
            if texts and vectors:
                all_texts.extend(texts)
                all_metadatas.extend([c["metadata"] for c in chunks])
                all_vectors.extend(vectors)
        
        if not all_texts:
            return 0
        
        print(f"  Adding {len(all_texts)} chunks to vectorstore...")
        
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_texts(
                texts=all_texts,
                embedding=embeddings,
                metadatas=all_metadatas,
                persist_directory=CHROMA_DIR
            )
        else:
            self.vectorstore.add_texts(
                texts=all_texts,
                metadatas=all_metadatas
            )
        
        for pdf_file in files_to_process:
            self._mark_file_processed(os.path.join(directory, pdf_file), topic)
        
        return len(all_texts)
    
    def load_all_pdfs(self, force_reload: bool = False, use_cache: bool = True) -> dict:
        results = {}
        
        print("\n[Loading Frontend PDFs]")
        total_fe = self.load_pdfs_from_directory(FE_DATA_DIR, "frontend", force_reload, use_cache)
        results["frontend"] = total_fe
        
        print("\n[Loading AI Agent PDFs]")
        total_ai = self.load_pdfs_from_directory(AI_DATA_DIR, "ai_agent", force_reload, use_cache)
        results["ai_agent"] = total_ai
        
        print("\n[Loading General PDFs]")
        total_general = self.load_pdfs_from_directory(DATA_DIR, "general", force_reload, use_cache)
        results["general"] = total_general
        
        return results
    
    def clear_cache(self) -> bool:
        try:
            import shutil
            for dir_path in [TEXT_CACHE_DIR, VECTOR_CACHE_DIR]:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    os.makedirs(dir_path)
            print("Cache cleared")
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
    
    def clear_vectorstore(self) -> bool:
        try:
            import shutil
            if os.path.exists(CHROMA_DIR):
                shutil.rmtree(CHROMA_DIR)
                os.makedirs(CHROMA_DIR)
                print("Vectorstore cleared")
            
            if os.path.exists(PROCESSED_FILES_PATH):
                os.remove(PROCESSED_FILES_PATH)
                self._processed_files = {}
            
            self.vectorstore = None
            self._initialized = False
            return True
        except Exception as e:
            print(f"Error clearing vectorstore: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        text_files = os.listdir(TEXT_CACHE_DIR) if os.path.exists(TEXT_CACHE_DIR) else []
        vector_files = os.listdir(VECTOR_CACHE_DIR) if os.path.exists(VECTOR_CACHE_DIR) else []
        
        text_size = sum(os.path.getsize(os.path.join(TEXT_CACHE_DIR, f)) for f in text_files)
        vector_size = sum(os.path.getsize(os.path.join(VECTOR_CACHE_DIR, f)) for f in vector_files)
        
        return {
            "text_cache_count": len(text_files),
            "vector_cache_count": len(vector_files),
            "text_cache_size_mb": round(text_size / 1024 / 1024, 2),
            "vector_cache_size_mb": round(vector_size / 1024 / 1024, 2)
        }
    
    def search(self, query: str, k: int = 5, topic: Optional[str] = None) -> List[str]:
        self._init_vectorstore()
        
        if not self.vectorstore:
            return []
        
        try:
            if topic:
                results = self.vectorstore.similarity_search(
                    query, 
                    k=k,
                    filter={"topic": topic}
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def has_data(self) -> bool:
        self._init_vectorstore()
        return self.vectorstore is not None
    
    def get_document_count(self) -> int:
        self._init_vectorstore()
        if not self.vectorstore:
            return 0
        try:
            return self.vectorstore._collection.count()
        except:
            return 0

rag_service = RAGService()
