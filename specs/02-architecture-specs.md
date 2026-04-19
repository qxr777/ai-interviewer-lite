---
title: 02-架构规格
---

# 架构规格

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| Web 框架 | FastAPI |
| LLM | DeepSeek-Chat (OpenAI 兼容接口) |
| 数据库 | SQLite |

## 四层架构

```
API → Agent → Tools → Harness → (LLM API)
```

## 目录结构

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

## API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| /api/interview/start | POST | 开始面试 |
| /api/interview/{id}/answer | POST | 提交回答 |
| /api/interview/{id}/report | GET | 获取报告 |
