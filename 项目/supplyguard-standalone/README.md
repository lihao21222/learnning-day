# SupplyGuard - 供应链风控 Agent 平台

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 项目简介

SupplyGuard 是一个面向企业级的供应链风控智能平台，采用 **多 Agent 协作架构**，结合知识图谱与大语言模型技术，实现对供应商风险的实时监控、智能分析与预警。

**核心能力：**
- 🔍 **多源数据融合** - 自动收集、清洗和处理多维度供应商数据
- 🤖 **智能风险分析** - 基于规则与语义的风险识别与评估
- 👥 **人工在环** - 人机协作模式，AI 建议 + 人工决策
- 📊 **可视化看板** - 实时监控、风险画像与统计分析
- 📝 **全链路审计** - 所有决策可追溯，符合合规要求

---

## 🎯 适用场景

1. **供应商风险管理** - 定期评估供应商风险状态
2. **供应链健康度监控** - 端到端供应链风险可视
3. **风险预警系统** - 异常情况提前预测预警
4. **供应商准入评估** - 新供应商引入前的综合评估

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户接入层                                 │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Streamlit UI  │  │  Web Console │  │  API Clients     │    │
│  └─────────────────┘  └──────────────┘  └──────────────────┘    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      API 服务层 (FastAPI)                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │
│  │  Suppliers   │ │  Assessment  │ │  Knowledge   │ │ Reports │ │
│  │   API        │ │    API       │ │    Base API  │ │   API   │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └─────────┘ │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                   业务逻辑层 (Multi-Agent System)                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │       ┌──────────┐     ┌──────────┐     ┌─────────┐    │   │
│  │       │ Data     │────▶│ Risk     │────▶│ Report  │    │   │
│  │       │ Collector│     │ Analyst  │     │ Agent   │    │   │
│  │       └──────────┘     └──────────┘     └─────────┘    │   │
│  │             │                                       │   │
│  │             ▼                                       │   │
│  │       ┌──────────────┐                             │   │
│  │       │  Cross Valid │                             │   │
│  │       └──────────────┘                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                        数据服务层                                 │
│  ┌──────────────┐  ┌──────────────────┐ ┌──────────────────┐    │
│  │  RAG Engine  │  │ Knowledge Graph  │ │  Vector Store    │    │
│  └──────────────┘  └──────────────────┘ └──────────────────┘    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                        持久化层                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    │
│  │ PostgreSQL  │  │   Qdrant    │  │  S3 / Object Storage │    │
│  └─────────────┘  └─────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
supplyguard/
│
├── 📄 核心配置
│   ├── config.py              # 风险规则与基础配置
│   ├── settings.py            # Pydantic 配置管理（支持 .env）
│   └── .env.example           # 环境变量模板
│
├── 🤖 业务逻辑
│   ├── models.py              # Pydantic & 数据模型
│   ├── knowledge_base.py      # 知识库与检索引擎
│   └── agents.py              # Multi-Agent 编排系统
│
├── 💾 数据层
│   └── database.py            # SQLAlchemy ORM & 数据库抽象
│
├── 🚀 服务层
│   ├── main.py                # FastAPI 服务器
│   ├── app.py                 # Streamlit Web 界面
│   └── demo.py                # 命令行演示
│
├── 📊 数据目录
│   ├── data/
│   │   ├── knowledge_base/    # 知识库文档
│   │   ├── suppliers/         # 供应商数据
│   │   └── reports/           # 评估报告
│   └── logs/                  # 运行日志
│
├── 📖 文档
│   ├── README.md              # 本文件
│   └── 面试准备.md            # 面试指南
│
└── 📦 依赖
    └── requirements.txt       # 项目依赖
```

---

## 🚀 快速开始

### 方式一：命令行演示（最快捷）

```bash
cd supplyguard
python demo.py
```

### 方式二：Streamlit Web 界面

```bash
cd supplyguard
pip install -r requirements.txt
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

### 方式三：FastAPI 服务

```bash
cd supplyguard
pip install -r requirements.txt
python main.py
```

访问 http://localhost:8000/docs 查看 Swagger API 文档

---

## 📦 依赖说明

| 依赖 | 用途 | 必选 |
|-----|------|-----|
| streamlit | Web 界面 | 否（可选）|
| fastapi + uvicorn | API 服务 | 否（可选）|
| pydantic | 数据验证 | 否（可选）|
| pandas + plotly | 数据分析与可视化 | 否（可选）|
| sqlalchemy | 数据库 ORM | 否（可选）|
| langchain + langgraph | LLM 应用框架 | 否（可选）|
| qdrant-client | 向量数据库 | 否（可选）|

---

## 🤖 Multi-Agent 系统

### Agent 角色设计

| Agent | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Data Collector** | 多源数据收集与聚合 | 供应商 ID | 结构化数据 |
| **Risk Analyst** | 风险识别与评分 | 数据集合 | 风险发现列表 |
| **Cross Validator** | 交叉验证与置信度计算 | 风险发现 | 验证后的发现 |
| **Report Generator** | 报告生成与建议 | 验证结果 | 完整风险报告 |

### 编排流程

```
Start
  │
  ├─▶ Data Collection Agent
  │       │
  │       └─▶ Collect: Supplier Info, Financial Data, News, etc.
  │
  ├─▶ Risk Analysis Agent
  │       │
  │       └─▶ Analyze: Rule-based + Semantic Matching
  │
  ├─▶ Cross Validation Agent
  │       │
  │       └─▶ Verify: Multi-source confirmation
  │
  └─▶ Report Generation Agent
          │
          └─▶ Generate: Risk report + Mitigation suggestions
```

---

## 📊 风险评估维度

SupplyGuard 从 6 个维度评估供应商风险：

1. **财务风险** (权重: 0.25) - 负债、亏损、资金链状况
2. **质量风险** (权重: 0.20) - 质量问题、产品召回
3. **供应链中断风险** (权重: 0.20) - 停产、缺货、产能
4. **合规风险** (权重: 0.15) - 环保、劳动法、合规问题
5. **地缘政治风险** (权重: 0.10) - 贸易摩擦、关税影响
6. **供应商关系风险** (权重: 0.10) - 合同纠纷、拖欠货款

---

## 🔧 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

### 关键配置项

| 配置项 | 说明 | 默认值 |
|-------|------|--------|
| ENVIRONMENT | 运行环境 | development |
| API_HOST/API_PORT | API 服务地址 | 0.0.0.0:8000 |
| DATABASE_URL | 数据库连接 (SQLite/PostgreSQL) | null |
| LLM_PROVIDER | LLM 提供商 (ollama/openai) | null |

---

## 📝 生产环境部署建议

### 1. 数据库

从 SQLite 迁移到 PostgreSQL：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/supplyguard
```

### 2. 缓存

添加 Redis 缓存评估结果：

```env
REDIS_URL=redis://localhost:6379/0
```

### 3. 向量数据库

集成 Qdrant 进行语义检索：

```env
VECTOR_STORE_TYPE=qdrant
QDRANT_URL=http://localhost:6333
```

### 4. LLM 集成

使用 Ollama 本地大模型：

```env
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## 🔜 项目路线图

| 阶段 | 任务 | 状态 |
|------|------|------|
| Phase 1 | Core Framework & Multi-Agent System | ✅ 完成 |
| Phase 2 | FastAPI & Streamlit UI | ✅ 完成 |
| Phase 3 | Vector Database Integration | ⏳ 计划中 |
| Phase 4 | LLM Integration | ⏳ 计划中 |
| Phase 5 | Knowledge Graph | ⏳ 计划中 |
| Phase 6 | Production Deployment | ⏳ 计划中 |

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

如有问题，请通过以下方式联系：
- 提交 Issue
- 发送邮件

---

**注意：** 这是一个完整的架构设计与实现项目，适合作为学习参考、面试项目与原型开发。
