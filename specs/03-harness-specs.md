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

## 4. 审计日志 (Audit Log)

### 4.1 功能要求
- **持久化要求**：审计日志**必须**实时持久化到磁盘文件（推荐：`logs/audit.jsonl`）。
- **可查询性**：必须提供 API 接口（如 `/api/audit/logs`）或 CLI 工具，确保外部系统或开发者可随时调取日志流。
- **记录范围**：必须包含关键生命周期事件（开始、解析、验证失败、评估、结束）。

### 4.2 历史教训 (Lessons Learned)
- **遗漏点**：初始版本将日志存储在 `AuditLogger` 的实例变量（内存）中，导致应用重启或请求结束后数据丢失。
- **修正方案**：后续版本强制要求使用追加写（Append-only）的文件存储，并增加全局审计接口。
