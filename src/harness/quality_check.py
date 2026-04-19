# src/harness/quality_check.py

from typing import List, Dict, Any


def check_variance(scores: List[float]) -> Dict[str, Any]:
    """Harness：评分方差检查"""
    if len(scores) < 2:
        return {"variance": 0.0, "confidence": "high"}
    
    avg = sum(scores) / len(scores)
    variance = sum((s - avg) ** 2 for s in scores) / len(scores)
    
    return {
        "variance": round(variance, 2),
        "confidence": "high" if variance < 5 else "medium" if variance < 10 else "low"
    }


def check_resume_confidence(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """Harness：简历提取置信度检查"""
    score = 0.0
    
    if all(k in extracted for k in ["name", "skills", "experience"]):
        score += 0.4
    if len(extracted.get("skills", [])) >= 3:
        score += 0.2
    if len(extracted.get("experience", [])) >= 1:
        score += 0.2
    if extracted.get("education"):
        score += 0.2
    
    return {
        "confidence": round(score, 2),
        "passed": score >= 0.7,
        "details": {
            "skills_count": len(extracted.get("skills", [])),
            "experience_count": len(extracted.get("experience", []))
        }
    }
