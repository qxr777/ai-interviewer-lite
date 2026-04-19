# src/agent/interview_agent.py
# TODO: 实现主编排 Agent

from src.tools.resume_extractor import ResumeExtractor
from src.tools.question_generator import QuestionGenerator
from src.tools.answer_evaluator import AnswerEvaluator
from src.harness.audit_log import AuditLogger


class InterviewAgent:
    """主编排 Agent"""
    
    def __init__(self, session_id: str, position: str):
        self.session_id = session_id
        self.position = position
        self.audit = AuditLogger(session_id)
        self.resume_extractor = ResumeExtractor()
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.resume_data = None
        self.questions = []
        self.scores = []
    
    async def start(self, resume_text: str) -> dict:
        """开始面试"""
        self.audit.log("interview_start", {"session_id": self.session_id, "position": self.position})
        self.resume_data = await self.resume_extractor.extract(resume_text)
        # TODO: 生成第一个问题
        return {"session_id": self.session_id, "resume": self.resume_data}
    
    async def submit_answer(self, answer: str) -> dict:
        """提交回答"""
        # TODO: 评估回答，生成下一个问题或结束
        pass
