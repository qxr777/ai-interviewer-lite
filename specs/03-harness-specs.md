---
title: 03-Harness 规格
---

# Harness 规格

## 1. resume_schema.yaml

必填字段：name, skills, experience

## 2. OutputValidator

验证 Schema 符合性，返回 (passed, errors)

## 3. 质量检查

```python
# 方差检查
def check_variance(scores):
    avg = sum(scores) / len(scores)
    variance = sum((s - avg) ** 2 for s in scores) / len(scores)
    return {"variance": variance, "confidence": "high" if variance < 5 else "low"}

# 置信度检查
def check_resume_confidence(extracted):
    score = 0.0
    if all(k in extracted for k in ["name", "skills", "experience"]):
        score += 0.4
    if len(extracted.get("skills", [])) >= 3:
        score += 0.2
    if len(extracted.get("experience", [])) >= 1:
        score += 0.2
    if extracted.get("education"):
        score += 0.2
    return {"confidence": score, "passed": score >= 0.7}
```

## 4. 审计日志

记录事件：interview_start, resume_extracted, answer_evaluated, interview_complete
