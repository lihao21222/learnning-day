# SupplyGuard 架构设计文档

> **注意：** 本文档描述了 SupplyGuard 的完整架构设计与实现思路，适合作为学习与面试参考。

---

## 📋 目录

1. [整体架构](#整体架构)
2. [核心模块设计](#核心模块设计)
3. [关键技术选型](#关键技术选型)
4. [扩展性设计](#扩展性设计)
5. [性能优化](#性能优化)
6. [安全考虑](#安全考虑)

---

## 整体架构

### 分层架构

SupplyGuard 采用清晰的分层架构，各层职责明确，便于开发、测试和维护。

```
┌─────────────────────────────────────────────────────┐
│         Presentation Layer (UI / API)                │
│  - Streamlit Dashboard                              │
│  - FastAPI REST API                                 │
│  - Third-party Integrations                         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         Business Logic Layer (Core)                 │
│  - Multi-Agent System                               │
│  - Orchestrator                                     │
│  - Risk Analysis Engine                             │
│  - Reporting Service                                │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         Data Service Layer                           │
│  - Knowledge Base Service                           │
│  - Vector Store Service                             │
│  - Graph Database Service                           │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         Infrastructure Layer                         │
│  - Persistent Storage (PostgreSQL / SQLite)         │
│  - Cache (Redis)                                    │
│  - Message Queue (RabbitMQ / Kafka)                 │
└─────────────────────────────────────────────────────┘
```

---

## 核心模块设计

### 1. Multi-Agent 系统 (agents.py)

#### 设计模式：策略模式 + 责任链

```python
class BaseAgent(ABC):
    @abstractmethod
    def execute(self, context: AgentContext) -> AgentContext:
        pass

class DataCollectorAgent(BaseAgent):
    """负责数据收集"""
    pass

class RiskAnalysisAgent(BaseAgent):
    """负责风险分析"""
    pass

class CrossValidationAgent(BaseAgent):
    """负责交叉验证"""
    pass

class ReportGeneratorAgent(BaseAgent):
    """负责报告生成"""
    pass
```

#### 扩展性设计

每个 Agent 实现 `BaseAgent` 接口，可以独立开发、测试和部署。

```python
# TODO: Phase 3 - 可添加更多 Agent
# class FraudDetectionAgent(BaseAgent): ...
# class MarketTrendAgent(BaseAgent): ...
# class SustainabilityAgent(BaseAgent): ...
```

### 2. 知识库系统 (knowledge_base.py)

#### 当前实现
- 内存存储（演示模式）
- 关键词匹配检索
- 规则引擎

#### 升级路径 (Phase 3)

```python
# TODO: Phase 3 - 集成向量数据库
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class VectorKnowledgeBase(KnowledgeBase):
    """
    基于向量检索的知识库，支持语义搜索
    """
    def __init__(self):
        # 初始化 Embedding 模型
        self.model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
        # 初始化向量数据库
        self.qdrant = QdrantClient(url=settings.QDRANT_URL)
        # ...
```

### 3. 数据库抽象层 (database.py)

#### 设计模式：工厂模式 + 适配器

```python
class Database(ABC):
    """数据库抽象接口"""
    
    @abstractmethod
    def save_supplier(self, supplier: Supplier) -> bool:
        pass
    
    @abstractmethod
    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        pass

# 不同的数据库实现
class SQLiteDatabase(Database): ...
class PostgreSQLDatabase(Database): ...
class InMemoryDatabase(Database): ...  # 当前演示模式
```

---

## 关键技术选型

### 后端框架：FastAPI vs Flask vs Django

| 考虑因素 | FastAPI | Flask | Django |
|---------|--------|------|-------|
| 性能 | 🏆 高性能，基于 Starlette | ⭐ 轻量 | ⭐ 全功能 |
| 类型安全 | ✅ Pydantic 集成 | ❌ 无 | ⭐ ORM |
| API 文档 | ✅ 自动 Swagger/ReDoc | ❌ 需手动 | ⭐ DRF |
| 异步支持 | ✅ 原生支持 | ⭐ 扩展支持 | ❌ 有限 |

**选择理由：** FastAPI 适合高性能的 API 服务，且类型安全，自动文档。

### 向量数据库：Qdrant vs Chroma vs Weaviate

| 考虑因素 | Qdrant | Chroma | Weaviate |
|---------|--------|--------|---------|
| 部署简易 | ⭐ Docker | ⭐ Docker/Python | ⭐ Docker |
| 性能 | 🏆 高 | ⭐ 中 | ⭐ 中高 |
| Python SDK | ✅ 好 | ✅ 好 | ✅ 好 |
| 生态集成 | ⭐ LangChain 支持 | ⭐ LangChain 支持 | ⭐ LangChain 支持 |

**推荐选择：** Qdrant - 性能优秀，Docker 部署简单。

---

## 扩展性设计

### 1. 插件化架构

```python
class BasePlugin(ABC):
    """插件基类"""
    name: str
    version: str
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def execute(self, data):
        pass

# 示例插件
class FinancialDataPlugin(BasePlugin):
    """接入财务数据"""
    pass

class NewsDataPlugin(BasePlugin):
    """接入新闻数据"""
    pass
```

### 2. 配置驱动

使用 Pydantic Settings 管理配置，支持环境变量与 .env 文件：

```python
class Settings(BaseSettings):
    LLM_PROVIDER: Optional[str] = None
    VECTOR_STORE_TYPE: Optional[str] = None
    DATABASE_URL: Optional[str] = None
```

---

## 性能优化

### 1. 缓存策略

```python
# TODO: Phase 4 - 添加缓存层
from functools import lru_cache
import redis
import json

class RiskCache:
    """
    风险评估结果缓存
    缓存策略：
    - 相同供应商 + 相同时间窗口 = 缓存命中
    - TTL: 24小时
    """
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
    
    def get(self, supplier_id: str):
        key = f"risk:assess:{supplier_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def set(self, supplier_id: str, result: dict, ttl: int = 86400):
        key = f"risk:assess:{supplier_id}"
        self.redis.setex(key, ttl, json.dumps(result))
```

### 2. 异步处理

```python
# TODO: Phase 4 - 异步评估
from fastapi import BackgroundTasks

@app.post("/api/assess/async")
async def assess_async(supplier_id: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(_run_assessment, supplier_id, task_id)
    return {"task_id": task_id, "status": "pending"}
```

---

## 安全考虑

### 1. 身份验证与授权

```python
# TODO: Phase 6 - 添加 OAuth2 / JWT
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return User(username=username)
```

### 2. 输入验证

使用 Pydantic 进行强类型验证，防止注入攻击：

```python
class RiskAssessmentRequest(BaseModel):
    supplier_id: str = Field(..., min_length=3, max_length=50)  # 限制长度
    # ...
```

### 3. 审计日志

所有关键操作记录审计日志，可追溯：

```python
def log_action(action: str, actor: str, entity_id: str, details: dict):
    """记录审计日志"""
    entry = AuditLog(
        id=str(uuid.uuid4()),
        action=action,
        actor=actor,
        entity_id=entity_id,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
```

---

## 部署架构

### 开发环境
- 单机部署
- 内存存储 / SQLite
- 无外部依赖

### 生产环境

```
                       ┌─────────────┐
                       │   LB / CDN  │
                       └──────┬──────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │ FastAPI │          │ FastAPI │          │ Streamlit│
   │ Worker 1│          │ Worker 2│          │ Dashboard│
   └────┬────┘          └────┬────┘          └─────────┘
        │                    │
        └──────────┬─────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
  ┌────▼────┐            ┌─────▼──────┐
  │ Qdrant  │            │ PostgreSQL │
  │(Vector) │            │  (Relational)│
  └─────────┘            └────────────┘
       │
  ┌────▼────┐
  │  Redis  │
  │ (Cache) │
  └─────────┘
```

---

## 总结

这是一个**设计完整、可扩展性强**的架构，虽然当前实现是演示模式，但已预留了完整的升级路径。

### 当前状态
- ✅ 核心框架完成
- ✅ 架构设计清晰
- ✅ 预留扩展接口
- ✅ 文档与演示完备

### 下一步（可选）
1. 集成真实的 LLM
2. 添加向量数据库
3. 接入真实数据源
4. 部署到生产环境
5. 持续监控与迭代
