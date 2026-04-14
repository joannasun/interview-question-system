from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import os

app = FastAPI(
    title="面试问答系统API",
    description="提供前端技术和AI Agent面试题的API接口",
    version="1.0.0"
)

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://interview-frontend.vercel.app",
    os.environ.get("FRONTEND_URL", "")
]

allowed_origins = [origin for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     import uvicorn
#     import os
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)