# AI Interviewer Lite

> AI 技术面试 Agent 系统（教学简化版）  
> **CS599 企业级应用软件设计与开发** | 武汉理工大学 | 2026 年春季

---

## 📋 项目概述

构建一个带**简历提取**的技术面试 Agent 系统，用于教学 Harness Engineering 核心概念。

### 核心功能

- ✅ 简历提取（姓名、技能、经历、教育）
- ✅ Schema 验证（输出格式检查）
- ✅ 置信度检查（质量评估）
- ✅ 多轮问答（3-5 轮）
- ✅ 回答评估（方差 < 10）
- ✅ 审计日志（关键事件追踪）

### 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| Web 框架 | FastAPI |
| LLM | DeepSeek-Chat (OpenAI 兼容接口) |
| 数据库 | SQLite |
| 测试 | pytest |

---

## 🚀 快速开始

### 1. 环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 设置 API Key
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY
```

### 2. 启动服务

```bash
uvicorn src.api.routes:app --reload
```

访问：http://localhost:8000

### 3. 运行测试

```bash
# 单元测试
pytest tests/ -v

# E2E 测试
playwright install  # 首次运行
pytest tests/test_frontend_e2e.py -v
```

---

## 📁 项目结构

```
ai-interviewer-lite/
├── specs/                        # 规格文档
│   ├── 01-product-specs.md
│   ├── 02-architecture-specs.md
│   ├── 03-harness-specs.md
│   ├── 04-test-specs.md
│   └── 05-frontend-specs.md
├── src/
│   ├── agent/
│   │   └── interview_agent.py
│   ├── tools/
│   │   ├── resume_extractor.py
│   │   ├── question_generator.py
│   │   └── answer_evaluator.py
│   ├── harness/
│   │   ├── quality_check.py
│   │   ├── output_validator.py
│   │   └── audit_log.py
│   └── api/
│       ├── routes.py
│       └── static/
│           └── index.html
├── tests/
│   ├── test_resume_extractor.py
│   ├── test_agent.py
│   ├── test_harness.py
│   └── test_frontend_e2e.py
├── AGENTS.md
├── .env.example
├── .gitignore
├── pytest.ini
├── resume_schema.yaml
├── rubric.yaml
├── test_resume.txt
├── requirements.txt
└── README.md
```

---

## 📖 开发文档

| 文档 | 内容 |
|------|------|
| **AGENTS.md** | Code Agent 必读开发指南 |
| specs/01-product-specs.md | 产品需求 |
| specs/02-architecture-specs.md | 架构设计 |
| specs/03-harness-specs.md | Harness 约束 |
| specs/04-test-specs.md | 测试规格 |
| specs/05-frontend-specs.md | 前端设计 |

---

## 🎯 Harness Engineering 概念

| 概念 | 实现位置 |
|------|---------|
| Feedforward Guide | AGENTS.md, System Prompt |
| Feedback Sensor | quality_check.py |
| Output Validation | output_validator.py |
| Audit Trail | audit_log.py |

---

*版本：1.0 | 最后更新：2026-04-19*
