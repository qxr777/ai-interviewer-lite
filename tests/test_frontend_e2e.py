# tests/test_frontend_e2e.py
# TODO: 实现 E2E 测试（需要 playwright）

import pytest
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    """测试首页加载"""
    page.goto("http://localhost:8000")
    
    # 检查页面标题
    expect(page).to_have_title("AI Interviewer Lite")
    
    # 检查关键元素
    expect(page.locator("h1")).to_contain_text("AI Interviewer Lite")
    expect(page.get_by_role("button", name="开始面试")).to_be_visible()

def test_full_interview_flow(page: Page):
    """测试完整面试流程"""
    page.goto("http://localhost:8000")
    
    # 1. 输入简历并开始
    resume_content = "张三，五年 Python 后端经验，精通 FastAPI 和微服务架构。"
    page.fill("#resume-text", resume_content)
    page.select_option("#position", "Python Developer")
    page.click("#start-btn")
    
    # 2. 等待第一个问题出现
    # 面试区域应该是可见的
    expect(page.locator("#section-interview")).to_be_visible(timeout=20000)
    expect(page.locator(".chat-question")).to_have_count(1)
    
    # 3. 进行三轮回答
    for i in range(1, 4):
        # 输入回答
        page.fill("#answer-input", f"这是针对第 {i} 个问题的回答。")
        page.click("#submit-btn")
        
        if i < 3:
            # 等待下一轮问题（问题数量增加）
            expect(page.locator(".chat-question")).to_have_count(i + 1, timeout=20000)
        else:
            # 最后一轮，等待报告出现
            expect(page.locator("#section-report")).to_be_visible(timeout=20000)
            
    # 4. 检查报告内容
    expect(page.locator("#report-content")).not_to_be_empty()
    expect(page.locator("#report-content .score")).to_be_visible()
    
    # 5. 测试重置功能
    page.click("text=开始新面试")
    expect(page.locator("#section-resume")).to_be_visible()
    expect(page.locator("#resume-text")).to_have_value("")
