
"""
项目整理脚本
把两个项目清晰地分开到不同目录
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"c:\Users\21222\Desktop\新建文件夹")

# ==============
# 1. 本地知识库问答系统
# ==============
LOCAL_RAG_DIR = BASE_DIR / "local-rag"
LOCAL_RAG_DIR.mkdir(exist_ok=True)

# 知识库项目文件
local_rag_files = [
    # 代码文件
    "simple_rag.py",
    "config.py",
    "logger.py",
    "document_loader.py",
    "document_loader_pro.py",
    "rag_qa.py",
    "advanced_rag.py",
    "app_simple.py",
    "app.py",
    "demo.py",
    "demo_advanced.py",
    "requirements.txt",
    "requirements-full.txt",
    "start_web.bat",
    
    # 测试文件
    "test_rag.py",
    "quick_test.py",
    "测试新文档.py",
    "测试多格式.py",
    "安装与测试.py",
    
    # 文档
    "README.md",
    "面试项目介绍.md",
    "面试项目介绍_豪华版.md",
    "面试展示指南.md",
    "面试问题大全及答案.md",
    "AI应用开发岗面试问题大全.md",
    "知识库使用完整指南.txt",
    "添加文档指南.txt",
    "多格式知识库使用说明.md"
]

print("正在整理本地知识库问答系统...")
for filename in local_rag_files:
    src = BASE_DIR / filename
    if src.exists():
        dst = LOCAL_RAG_DIR / filename
        shutil.copy2(src, dst)
        print(f"  [OK] 复制: {filename}")

# 移动知识库存数据
if (BASE_DIR / "knowledge_base").exists():
    kb_src = BASE_DIR / "knowledge_base"
    kb_dst = LOCAL_RAG_DIR / "data" / "knowledge_base"
    kb_dst.mkdir(exist_ok=True)
    for item in kb_src.iterdir():
        shutil.copy2(item, kb_dst / item.name)
    print("  [OK] 复制知识库数据")

# 移动日志
if (BASE_DIR / "logs").exists():
    logs_src = BASE_DIR / "logs"
    logs_dst = LOCAL_RAG_DIR / "logs"
    for item in logs_src.iterdir():
        if item.is_file():
            shutil.copy2(item, logs_dst / item.name)


# ==============
# 2. SupplyGuard 项目
# ==============
# supplyguard 已经存在了，我们只需要把 supplyguard/ 改名为 supplyguard-standalone
print("\n正在整理 SupplyGuard 项目...")
if (BASE_DIR / "supplyguard").exists() and not (BASE_DIR / "supplyguard-standalone").exists():
    shutil.move(str(BASE_DIR / "supplyguard"), str(BASE_DIR / "supplyguard-standalone"))
    print("  [OK] 移动 supplyguard 到 supplyguard-standalone")


# ==============
# 3. 清理中间文件
# ==============
print("\n清理临时文件...")
if (BASE_DIR / "organize_projects.py").exists():
    pass  # 保留这个脚本

for item in BASE_DIR.iterdir():
    # 删除我们已整理过的根目录文件
    if item.is_file() and item.name in local_rag_files:
        if item.name not in ["organize_projects.py"]:
            try:
                os.remove(str(item))
                print(f"  [OK] 删除: {item.name}")
            except:
                pass

# 清理 __pycache__
if (BASE_DIR / "__pycache__").exists():
    try:
        shutil.rmtree(BASE_DIR / "__pycache__")
        print("  [OK] 删除 __pycache__")
    except:
        pass

print("\n[OK] 项目整理完成！")
print("\n项目结构：")
print("├── local-rag/          本地知识库问答系统（基础版/进阶版/专业版）")
print("└── supplyguard-standalone/  供应链风控平台")
