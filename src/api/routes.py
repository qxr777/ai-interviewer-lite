# src/api/routes.py
# TODO: 实现 API 路由

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="AI Interviewer Lite")

# 挂载静态文件
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_path, "index.html"))


from src.agent.interview_agent import InterviewAgent
import uuid

# 全局存储，在实际生产环境中应替换为数据库或 Redis
sessions = {}

@app.post("/api/interview/start")
async def start_interview(position: str, resume_text: str):
    """开始面试"""
    session_id = str(uuid.uuid4())
    agent = InterviewAgent(session_id, position)
    
    try:
        result = await agent.start(resume_text)
        sessions[session_id] = agent
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/interview/{session_id}/answer")
async def submit_answer(session_id: str, answer: str):
    """提交回答"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
        
    agent = sessions[session_id]
    try:
        result = await agent.submit_answer(answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/interview/{session_id}/report")
async def get_report(session_id: str):
    """获取报告"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
        
    agent = sessions[session_id]
    return agent.get_report()
