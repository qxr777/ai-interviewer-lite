# tests/test_harness.py

from src.harness.quality_check import check_variance, check_resume_confidence


def test_check_variance():
    """测试方差检查"""
    # 稳定评分
    result = check_variance([75, 76, 75])
    assert result["variance"] < 5
    assert result["confidence"] == "high"
    
    # 波动评分
    result = check_variance([50, 90, 70])
    assert result["variance"] > 20
    assert result["confidence"] == "low"


def test_check_resume_confidence():
    """测试简历置信度"""
    # 完整简历
    result = check_resume_confidence({
        "name": "张三",
        "skills": ["Python", "Java"],
        "experience": [{"company": "ABC"}],
        "education": [{"school": "XX"}]
    })
    assert result["confidence"] >= 0.7
    assert result["passed"] == True
    
    # 不完整简历
    result = check_resume_confidence({
        "name": "李四",
        "skills": [],
        "experience": []
    })
    assert result["confidence"] < 0.7
    assert result["passed"] == False
