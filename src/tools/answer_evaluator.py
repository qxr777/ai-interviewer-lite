# src/tools/answer_evaluator.py
# TODO: 实现评估工具

from src.harness.quality_check import check_variance


class AnswerEvaluator:
    """工具：回答评估"""
    
    async def evaluate(self, question: str, answer: str) -> dict:
        """评估回答"""
        # TODO: 调用 LLM 评估（运行 3 次取平均）
        # 1. 运行 3 次独立评估
        # 2. 计算方差
        # 3. 返回结果
        pass
