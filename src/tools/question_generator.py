# src/tools/question_generator.py
# TODO: 实现问题生成工具


class QuestionGenerator:
    """工具：问题生成"""
    
    async def generate(self, position: str, resume_data: dict, question_idx: int) -> str:
        """生成面试问题"""
        from src.tools.llm_client import call_llm
        
        skills = ", ".join(resume_data.get("skills", ["基础知识"]))
        experiences = resume_data.get("experience", [])
        exp_text = ""
        for exp in experiences:
            exp_text += f"- {exp.get('company', '某公司')}: {exp.get('role', '后端开发')}\n"
            
        prompt = f"""
        你是一位高级技术面试官，正在面试候选人。
        面试职位：{position}
        候选人技能：{skills}
        候选人经历：
        {exp_text}
        
        这是第 {question_idx} 个问题。
        请根据候选人的背景，提出一个专业、有深度、且具体的技术面试问题。
        请直接输出问题内容，不要包含任何客套话或其他说明。
        """
        
        question = await call_llm(prompt, response_format="text")
        return question.strip()
