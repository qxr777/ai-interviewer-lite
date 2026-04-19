# tests/test_resume_extractor.py
# TODO: 实现简历提取测试

import pytest
from unittest.mock import patch
from src.tools.resume_extractor import ResumeExtractor

@pytest.mark.asyncio
async def test_resume_extraction():
    """测试简历提取"""
    extractor = ResumeExtractor()
    resume_text = "我叫王五。我会写 Python 和 React。我在阿里云做过后端工程师。"
    
    mock_json_response = '''
    {
        "name": "王五",
        "skills": ["Python", "React", "Docker"],
        "experience": [{"company": "阿里云", "role": "后端工程师"}]
    }
    '''
    
    with patch("src.tools.llm_client.call_llm") as mock_call:
        mock_call.return_value = mock_json_response
        result = await extractor.extract(resume_text)
        
        assert result["extracted_data"]["name"] == "王五"
        assert len(result["extracted_data"]["skills"]) == 3
        assert result["confidence"]["passed"] is True
