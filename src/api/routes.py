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


@app.post("/api/interview/start")
async def start_interview(position: str, resume_text: str):
    """开始面试"""
    # TODO: 实现
    pass


@app.post("/api/interview/{session_id}/answer")
async def submit_answer(session_id: str, answer: str):
    """提交回答"""
    # TODO: 实现
    pass


@app.get("/api/interview/{session_id}/report")
async def get_report(session_id: str):
    """获取报告"""
    # TODO: 实现
    pass
