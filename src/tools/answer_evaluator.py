# src/tools/answer_evaluator.py
# TODO: 实现评估工具

from src.harness.quality_check import check_variance


class AnswerEvaluator:
    """工具：回答评估"""
    
    async def evaluate(self, question: str, answer: str) -> dict:
        """评估回答"""
        from src.tools.llm_client import call_llm
        import json
        import asyncio
        
        prompt = f"""
        你是一位严格的技术面试官。请对候选人的回答进行打分（0-100分）并提供简短反馈。
        
        面试问题：{question}
        候选人回答：{answer}
        
        评分标准：
        - 技术准确性 (0-50分)
        - 表达清晰度 (0-30分)
        - 完整性 (0-20分)
        
        请以如下JSON格式返回：
        {{
            "score": <0-100的整数>,
            "feedback": "<简短的原因反馈>"
        }}
        
        只返回合法的 JSON 对象，不包含任何外部说明。
        """
        
        # 1. 运行 3 次独立评估
        tasks = []
        for _ in range(3):
            tasks.append(call_llm(prompt, response_format="json"))
            
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        scores = []
        feedbacks = []
        
        for resp in responses:
            if isinstance(resp, Exception):
                continue
            try:
                # 清理 markdown
                if resp.startswith("```json"):
                    resp = resp[7:]
                if resp.endswith("```"):
                    resp = resp[:-3]
                    
                data = json.loads(resp.strip())
                if "score" in data and isinstance(data["score"], (int, float)):
                    scores.append(float(data["score"]))
                    if "feedback" in data:
                        feedbacks.append(data["feedback"])
            except json.JSONDecodeError:
                pass
                
        if not scores: # 如果三次都失败了
            return {
                "score": 0,
                "feedback": "评分内部错误，未能生成有效打分。",
                "variance_info": {"variance": 0, "confidence": "low"}
            }
            
        # 2. 计算方差
        variance_info = check_variance(scores)
        
        # 3. 返回结果 (取平均分)
        avg_score = sum(scores) / len(scores)
        
        return {
            "score": round(avg_score, 1),
            "feedback": feedbacks[0] if feedbacks else "",
            "variance_info": variance_info,
            "raw_scores": scores
        }
