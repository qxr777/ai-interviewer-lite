# AGENTS.md
# AI Interviewer Lite - 项目开发指南

> **每次 Code Agent 启动时自动读取此文件**

---

## 🎯 项目目标

构建一个带**简历提取**的技术面试 Agent 系统。

### 核心流程

```
上传简历 → 提取信息 → Schema 验证 → 
问题 1 → 回答 1 → 评估 → 问题 2 → ... → 报告
```

---

## 📐 架构规则

### 1. 分层依赖（必须遵守）

```
API → Agent → Tools → Harness → (LLM API)
```

| 层 | 可以导入 | 禁止导入 |
|----|---------|---------|
| `api/` | `agent/`, `harness/` | `tools/`（直接） |
| `agent/` | `tools/`, `harness/` | 不能跳过 Tools 直接调用 LLM |
| `tools/` | `harness/` | 不能反向依赖 Agent |
| `harness/` | 标准库 | 无 |

### 2. 文件组织

```
src/
├── agent/interview_agent.py
├── tools/
│   ├── resume_extractor.py
│   ├── question_generator.py
│   └── answer_evaluator.py
├── harness/
│   ├── quality_check.py
│   ├── output_validator.py
│   └── audit_log.py
└── api/
    ├── routes.py
    └── static/index.html
```

---

## ⚠️ 常见陷阱

| 错误 | 解决方案 |
|------|---------|
| 一次性生成多个问题 | 每次只返回一个问题 |
| 跳过评估环节 | 每轮必须调用 evaluate() |
| 方差过大不处理 | 运行 3 次取平均 |
| 简历字段缺失 | Schema 验证必须通过 |
| 审计日志丢失 | 必须使用 JSONL 格式持久化落盘 |

---

## 🧪 测试要求

### 必做测试（4 个）

1. **简历提取 + Schema 验证** (`test_resume_extractor.py`)
2. **完整面试流程** (`test_agent.py`)
3. **方差测试** (`test_harness.py`)
4. **E2E 测试** (`test_frontend_e2e.py`)

### 运行测试

```bash
pytest tests/ -v
```

---

## 🚀 开发流程

### 第 1 步：实现 Harness 组件
1. `src/harness/output_validator.py`
2. `src/harness/quality_check.py`
3. `src/harness/audit_log.py`

### 第 2 步：实现 Tools
1. `src/tools/resume_extractor.py`
2. `src/tools/question_generator.py`
3. `src/tools/answer_evaluator.py`

### 第 3 步：实现 Agent
1. `src/agent/interview_agent.py`

### 第 4 步：实现 API
1. `src/api/routes.py`
2. `src/api/static/index.html`（已提供）

---

## 📋 质量要求

| 指标 | 阈值 |
|------|------|
| 简历提取置信度 | > 0.7 |
| Schema 验证 | 100% 通过 |
| 评分方差 | < 10 |
| 响应时间 | < 10 秒/轮 |
| 审计日志 | 100% 持久化落盘 (JSONL) |

---

## 🔧 快速参考

### 调用 LLM

```python
import os
import httpx

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.bianxie.ai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

async def call_llm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LLM_API_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
```

### Schema 验证

```python
from src.harness.output_validator import OutputValidator
validator = OutputValidator("resume_schema.yaml")
passed, errors = validator.validate(data)
```

### 方差检查

```python
from src.harness.quality_check import check_variance
result = check_variance([75, 78, 76])
```

---

*版本：1.0 | 最后更新：2026-04-19*
