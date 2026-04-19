# tests/test_agent.py
# TODO: 实现 Agent 流程测试

import pytest
from unittest.mock import patch, AsyncMock
from src.agent.interview_agent import InterviewAgent

@pytest.mark.asyncio
async def test_interview_flow():
    """测试完整面试流程"""
    agent = InterviewAgent("test-session-123", "后端开发")
    
    # 我们不 mock 网络，改为 mock tools 防止真正的 API 消耗。
    # 也可以直接 mock call_llm。
    with patch("src.tools.resume_extractor.ResumeExtractor.extract", new_callable=AsyncMock) as mock_extract, \
         patch("src.tools.question_generator.QuestionGenerator.generate", new_callable=AsyncMock) as mock_gen, \
         patch("src.tools.answer_evaluator.AnswerEvaluator.evaluate", new_callable=AsyncMock) as mock_eval:
         
        mock_extract.return_value = {
            "extracted_data": {"name": "Test", "skills": ["Python"], "experience": []},
            "confidence": {"passed": True, "confidence": 0.9}
        }
        mock_gen.return_value = "你对 Python 的 GIL 怎么看？"
        mock_eval.return_value = {"score": 85.0, "feedback": "还行", "variance_info": {"variance": 2.0, "confidence": "high"}}
        
        # 1. Start
        start_result = await agent.start("我的简历内容...")
        assert start_result["question_idx"] == 1
        assert start_result["question"] == "你对 Python 的 GIL 怎么看？"
        
        # 2. 回答第一问
        ans1_result = await agent.submit_answer("GIL 会限制多线程...")
        assert ans1_result["status"] == "in_progress"
        assert ans1_result["question_idx"] == 2
        
        # 3. 回答第二问
        ans2_result = await agent.submit_answer("另一个回答...")
        assert ans2_result["status"] == "in_progress"
        assert ans2_result["question_idx"] == 3
        
        # 4. 回答第三问 (结束)
        ans3_result = await agent.submit_answer("第三个回答...")
        assert ans3_result["status"] == "complete"
        assert len(agent.scores) == 3
        
        report = agent.get_report()
        assert report["rounds"] == 3
        assert report["total_score"] == 85.0
