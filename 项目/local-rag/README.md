# 本地知识库问答系统 (RAG)

一个完整的本地知识库问答项目，适合学习、演示和面试准备。

---

## ✨ 项目特点

- 📚 **多格式文档支持**: TXT, PDF, DOCX
- 🎯 **分层架构**: 从简单到复杂多个版本
- 🌐 **Web 界面**: Streamlit 提供直观交互
- 📝 **完整文档**: 包含面试指南和使用说明

---

## 🗂️ 项目结构

```
├── knowledge_base/           # 存放知识库文档
├── vector_db/               # 向量数据库存储（进阶版）
├── logs/                    # 日志文件
├── output/                  # 输出目录
│
├── simple_rag.py            # 简化版（纯 Python，无外部依赖）
├── advanced_rag.py          # 进阶版（工程化，含配置和日志）
├── rag_pro.py              # 专业版（多格式，策略模式）
│
├── demo.py                 # 简化版演示
├── demo_advanced.py        # 进阶版演示
├── demo_pro_final.py       # 专业版演示（推荐）
├── 测试多格式.py            # 多格式文档加载测试
├── main.py                 # 主程序入口（进阶版）
│
├── app_simple.py           # Streamlit Web 界面
├── start_web.bat           # Web 界面启动脚本
│
├── document_loader.py      # 基础文档加载器
├── document_loader_pro.py  # 专业版文档加载器（多格式）
├── vector_store.py         # 向量存储模块（进阶版）
├── rag_qa.py              # RAG 问答模块（进阶版）
├── config.py              # 配置管理
├── logger.py              # 日志系统
│
├── 面试项目介绍.md          # 面试项目介绍
├── 面试项目介绍_豪华版.md    # 面试项目介绍（完整版）
├── 面试展示指南.md         # 面试展示技巧
├── 多格式知识库使用说明.md  # 多格式使用说明
├── README.md              # 本文件
│
├── requirements.txt        # 基础依赖
└── requirements-full.txt  # 完整依赖
```

---

## 📋 支持的文档格式

| 格式 | 扩展名 | 依赖 | 状态 |
|------|--------|------|------|
| 纯文本 | .txt, .md | 无 | ✅ |
| Word | .docx | python-docx | ✅ |
| PDF | .pdf | pypdf | ✅ |

---

## 🚀 快速开始

### 0. 安装依赖

```bash
# 基础依赖（仅 TXT）
# 无需额外安装

# 标准依赖（支持多格式）
pip install pypdf python-docx

# 完整依赖（包含 Web 界面）
pip install streamlit pypdf python-docx
```

### 1. 准备文档

将您的文档放入 `knowledge_base/` 文件夹中（支持 .txt, .docx, .pdf）。

### 2. 运行演示

**推荐：专业版演示（支持多格式）**

```bash
python demo_pro_final.py
```

**其他选项：**

```bash
# 简化版演示（无外部依赖）
python demo.py

# 进阶版演示
python demo_advanced.py
```

### 3. 交互式问答

```bash
# 专业版（推荐，支持多格式）
python rag_pro.py

# 进阶版
python advanced_rag.py

# 简化版
python simple_rag.py
```

### 4. Web 界面

```bash
pip install streamlit
streamlit run app_simple.py
```

---

## 🎯 版本选择指南

| 版本 | 特点 | 适用场景 | 文件 |
|------|------|----------|------|
| **简化版** | 纯 Python，无外部依赖 | 快速上手，学习核心逻辑 | `simple_rag.py` |
| **进阶版** | 工程化，配置+日志 | 项目实战，展示代码规范 | `advanced_rag.py` |
| **专业版** | 多格式支持，策略模式 | 完整功能，面试演示 | `rag_pro.py` |
| **Web 版** | 可视化界面 | 演示效果最好 | `app_simple.py` |

---

## 📚 技术栈

| 技术 | 用途 |
|------|------|
| **Python** | 核心编程语言 |
| **Streamlit** | Web 界面 |
| **PyPDF** | PDF 文档解析 |
| **python-docx** | Word 文档解析 |
| **策略模式** | 文档解析器设计 |

---

## 📖 面试准备

### 核心文档

- [面试项目介绍_豪华版.md](面试项目介绍_豪华版.md) - 完整项目介绍
- [面试展示指南.md](面试展示指南.md) - 面试技巧和问题准备

### 推荐展示流程

1. 运行 `demo_pro_final.py` 演示功能
2. 或使用 `streamlit run app_simple.py` 展示 Web 界面
3. 讲解 `document_loader_pro.py` 中的策略模式设计
4. 展示 `rag_pro.py` 的模块化架构

---

## 📝 自定义配置

### 专业版配置

编辑 `rag_pro.py` 中的参数：

```python
# 文本分割配置
self.splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
```

### 进阶版配置

编辑 `config.py`：

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3
```

---

## 🔍 测试

```bash
# 测试多格式文档加载
python 测试多格式.py

# 运行各版本演示
python demo_pro_final.py  # 专业版
python demo_advanced.py   # 进阶版
python demo.py            # 简化版
```

---

## 📦 依赖说明

| 包 | 用途 | 必需 |
|----|------|------|
| pypdf | PDF 解析 | 可选 |
| python-docx | Word 解析 | 可选 |
| streamlit | Web 界面 | 可选 |

---

## ⚠️ 注意事项

- 首次使用多格式功能需要安装 pypdf 和 python-docx
- 建议使用 Python 3.8+
- 文档越多，加载时间越长
- Windows 控制台建议使用 UTF-8 编码

---

## 📄 许可证

本项目仅供学习和演示使用。

---

## 📞 说明

这是一个适合面试的 RAG 项目，包含从简单到复杂的多个版本，以及完整的面试指导文档。
