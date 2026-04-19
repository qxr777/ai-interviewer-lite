import os
import httpx
import json

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.bianxie.ai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

async def call_llm(prompt: str, response_format: str = "text") -> str:
    """封装对 LLM 的调用。支持返回纯文本和 JSON"""
    messages = [{"role": "user", "content": prompt}]
    
    payload = {
        "model": LLM_MODEL,
        "messages": messages
    }
    
    if response_format == "json":
        payload["response_format"] = {"type": "json_object"}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{LLM_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            # 记录异常并抛出
            print(f"[LLM Client Error]: {str(e)}")
            raise e
