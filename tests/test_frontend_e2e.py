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
