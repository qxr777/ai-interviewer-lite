# src/tools/resume_extractor.py
# TODO: 实现简历提取工具

from src.harness.output_validator import OutputValidator
from src.harness.quality_check import check_resume_confidence
from src.harness.audit_log import AuditLogger


class ResumeExtractor:
    """工具：简历提取"""
    
    def __init__(self):
        self.validator = OutputValidator("resume_schema.yaml")
        self.audit = AuditLogger()
    
    async def extract(self, resume_text: str) -> dict:
        """提取简历信息"""
        from src.tools.llm_client import call_llm
        import json
        
        prompt = f"""
        你是一个专业的简历提取助手。你需要从以下简历文本中提取信息，并以 JSON 格式输出。
        
        必须包含的字段：
        - name (字符串)
        - skills (字符串数组)
        - experience (对象数组，每个对象包含 company 和 role)
        
        可选考虑的字段：
        - email (字符串)
        - education (数组)
        - years_of_experience (整数)
        
        简历文本：
        ===
        {resume_text}
        ===
        
        只返回合法的 JSON 对象，不要返回任何其他内容或 Markdown 标记。如果是Markdown标记也请确保内部是标准的可解析JSON。
        """
        
        # 1. 调用 LLM 提取
        response_text = await call_llm(prompt, response_format="json")
        
        # 尝试解析 JSON
        try:
            # 清理可能的 markdown 代码块
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            data = json.loads(response_text.strip())
        except json.JSONDecodeError:
            self.audit.log("resume_extract_error", {"error": "JSON解析失败", "text": response_text})
            raise ValueError("无法解析简历内容为 JSON")
            
        # 2. Schema 验证
        passed, errors = self.validator.validate(data)
        if not passed:
            self.audit.log("resume_extract_invalid", {"errors": errors, "data": data})
            raise ValueError(f"简历数据格式不合法: {errors}")
            
        # 3. 置信度检查
        confidence_result = check_resume_confidence(data)
        
        # 4. 记录审计日志
        self.audit.log("resume_extracted", {
            "confidence": confidence_result["confidence"],
            "passed": confidence_result["passed"],
            "data": data
        })
        
        return {
            "extracted_data": data,
            "confidence": confidence_result
        }
