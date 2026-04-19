---
title: 05-前端规格
---

# 前端规格

## 单页面三区域

1. 上传简历 - textarea + 职位选择 + 开始按钮
2. 面试进行中 - 进度点 + 对话记录 + 回答输入
3. 面试报告 - 总分 + 置信度 + 各轮分数

## API 交互

```javascript
// 开始面试
POST /api/interview/start
→ {session_id, resume, first_question}

// 提交回答
POST /api/interview/{id}/answer
→ {action: "continue"|"complete", question, score}

// 获取报告
GET /api/interview/{id}/report
→ {overall_score, question_scores, resume}
```
