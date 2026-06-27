#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证核心功能
"""

print("="*60)
print("  知识库问答系统 - 快速测试")
print("="*60)

# 测试 1: 导入检查
print("\n[1/4] 检查核心模块...")
try:
    from document_loader_pro import DocumentLoaderPro
    print("  [OK] 文档加载器: OK")
except Exception as e:
    print(f"  [ER] 文档加载器: {e}")

try:
    import streamlit
    print("  [OK] Streamlit: OK (Web 界面可用)")
except ImportError:
    print("  [WARN] Streamlit: 未安装 (运行 Web 界面需要安装)")

# 测试 2: 检查示例文档
print("\n[2/4] 检查知识库...")
import os
kb_dir = "knowledge_base"
if os.path.exists(kb_dir):
    files = [f for f in os.listdir(kb_dir) if os.path.isfile(os.path.join(kb_dir, f))]
    print(f"  [INFO] 找到 {len(files)} 个文件")
    for f in files:
        print(f"         - {f}")
else:
    print(f"  [WARN] 知识库目录不存在: {kb_dir}")

# 测试 3: 显示可用命令
print("\n[3/4] 可用命令:")
print("  1. 运行 Web 界面:")
print("     streamlit run app_simple.py")
print("     (或双击: start_web.bat)")
print("\n  2. 运行命令行演示:")
print("     python demo_advanced.py")
print("\n  3. 交互式问答:")
print("     python advanced_rag.py")

# 测试 4: 提示安装
print("\n[4/4] 安装提示:")
print("  如需完整功能，请安装:")
print("  pip install streamlit")
print("  pip install pypdf python-docx")
print("\n" + "="*60)
print("\n提示:")
print("  - 运行 'streamlit run app_simple.py' 启动 Web 界面")
print("  - 运行 'demo_advanced.py' 查看命令行演示")
print("  - 阅读 '面试项目介绍_豪华版.md' 了解项目详情")
print("="*60)
