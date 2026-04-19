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
        
        # 提取简历
        extract_result = await self.resume_extractor.extract(resume_text)
        self.resume_data = extract_result["extracted_data"]
        
        # 记录置信度信息
        if not extract_result["confidence"]["passed"]:
            self.audit.log("interview_warning", {"message": "简历提取置信度过低", "confidence": extract_result["confidence"]})
            
        # 生成第一个问题
        first_question = await self.question_generator.generate(self.position, self.resume_data, len(self.questions) + 1)
        self.questions.append(first_question)
        
        return {
            "session_id": self.session_id,
            "resume": self.resume_data,
            "first_question": first_question,
            "question": first_question,
            "question_idx": 1
        }
    
    async def submit_answer(self, answer: str) -> dict:
        """提交回答"""
        if not self.questions:
            raise ValueError("面试未开始或已结束")
        
        current_question = self.questions[-1]
        
        # 评估回答
        eval_result = await self.answer_evaluator.evaluate(current_question, answer)
        self.scores.append(eval_result)
        
        self.audit.log("answer_evaluated", {
            "session_id": self.session_id,
            "question_idx": len(self.questions),
            "score": eval_result["score"],
            "variance_info": eval_result.get("variance_info")
        })
        
        # 检查方差，如果过大可以记录额外的 audit 日志
        if eval_result.get("variance_info", {}).get("confidence") == "low":
            self.audit.log("evaluation_warning", {"message": "评分方差过大", "variance_info": eval_result["variance_info"]})
        
        # 决定是否结束面试（假设 3 轮）
        if len(self.questions) >= 3:
            self.audit.log("interview_complete", {"session_id": self.session_id, "total_rounds": len(self.questions)})
            report = self.get_report()
            return {
                "action": "complete",
                "status": "complete",
                "overall_score": report["overall_score"],
                "confidence": report["confidence"],
                "question_scores": report["question_scores"],
                "message": "面试结束，感谢您的参与。"
            }
        
        # 生成下一个问题
        next_question = await self.question_generator.generate(self.position, self.resume_data, len(self.questions) + 1)
        self.questions.append(next_question)
        
        return {
            "action": "continue",
            "status": "in_progress",
            "current_score": eval_result["score"],
            "evaluation": eval_result,
            "question": next_question,
            "question_idx": len(self.questions)
        }
    
    def get_report(self) -> dict:
        """生成最终报告"""
        avg_score = sum(s["score"] for s in self.scores) / len(self.scores) if self.scores else 0
        return {
            "session_id": self.session_id,
            "position": self.position,
            "resume": self.resume_data,
            "rounds": len(self.scores),
            "overall_score": round(avg_score, 1),
            "confidence": "High",
            "question_scores": [s["score"] for s in self.scores],
            "details": self.scores,
            "audit_trail": self.audit.get_trail()
        }
