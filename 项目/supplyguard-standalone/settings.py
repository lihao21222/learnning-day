"""
SupplyGuard 配置管理
支持从环境变量和 .env 文件加载配置
"""
from typing import Optional, Dict, Any, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置模型"""
    
    # 基础配置
    APP_NAME: str = Field(default="SupplyGuard", description="应用名称")
    APP_VERSION: str = Field(default="1.0.0", description="应用版本")
    ENVIRONMENT: str = Field(default="development", description="运行环境: development, production")
    DEBUG: bool = Field(default=True, description="调试模式")
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    LOG_DIR: str = Field(default="./logs", description="日志目录")
    
    # API 配置
    API_HOST: str = Field(default="0.0.0.0", description="API 监听地址")
    API_PORT: int = Field(default=8000, description="API 监听端口")
    CORS_ORIGINS: str = Field(default="*", description="CORS 允许的来源，逗号分隔")
    
    # 数据库配置（可选）
    DATABASE_URL: Optional[str] = Field(default=None, description="数据库连接字符串")
    DATABASE_POOL_SIZE: int = Field(default=5, description="数据库连接池大小")
    
    # 缓存配置（可选）
    REDIS_URL: Optional[str] = Field(default=None, description="Redis 连接字符串")
    
    # LLM 配置（可选，用于项目升级）
    LLM_PROVIDER: Optional[str] = Field(default=None, description="LLM 提供商: ollama, openai")
    OLLAMA_HOST: Optional[str] = Field(default=None, description="Ollama 服务地址")
    OLLAMA_MODEL: Optional[str] = Field(default="llama3", description="Ollama 模型名称")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")
    
    # 向量数据库配置（可选，用于项目升级）
    VECTOR_STORE_TYPE: Optional[str] = Field(default=None, description="向量数据库类型: qdrant, chroma")
    QDRANT_URL: Optional[str] = Field(default="http://localhost:6333", description="Qdrant 地址")
    CHROMA_DB_PATH: Optional[str] = Field(default="./data/chroma_db", description="Chroma 数据路径")
    
    # 文件存储
    UPLOAD_DIR: str = Field(default="./data/uploads", description="上传文件目录")
    KNOWLEDGE_BASE_DIR: str = Field(default="./data/knowledge_base", description="知识库目录")
    REPORT_DIR: str = Field(default="./data/reports", description="报告目录")
    
    # 风险评估配置
    RISK_THRESHOLD_LOW: int = Field(default=20, description="低风险阈值")
    RISK_THRESHOLD_MEDIUM: int = Field(default=40, description="中风险阈值")
    RISK_THRESHOLD_HIGH: int = Field(default=60, description="高风险阈值")
    RISK_THRESHOLD_CRITICAL: int = Field(default=80, description="严重风险阈值")
    
    # Human-in-the-loop 配置
    ENABLE_HUMAN_REVIEW: bool = Field(default=True, description="启用人工审核")
    HUMAN_REVIEW_THRESHOLD: int = Field(default=40, description="需要人工审核的风险分数阈值")
    
    # 审计配置
    ENABLE_AUDIT_TRAIL: bool = Field(default=True, description="启用审计追踪")
    AUDIT_RETENTION_DAYS: int = Field(default=90, description="审计日志保留天数")
    
    # 评分参数
    DEFAULT_CHUNK_SIZE: int = Field(default=500, description="文档切分块大小")
    DEFAULT_CHUNK_OVERLAP: int = Field(default=50, description="文档块重叠大小")
    DEFAULT_TOP_K: int = Field(default=3, description="检索返回文档数")
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            return "INFO"
        return v.upper()
    
    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str) and v.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",") if origin.strip()]
    
    def get_cors_origins_list(self) -> List[str]:
        """获取 CORS 允许的来源列表"""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        elif isinstance(self.CORS_ORIGINS, str):
            if self.CORS_ORIGINS == "*":
                return ["*"]
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["*"]
    
    def ensure_dirs(self) -> None:
        """确保必要的目录存在"""
        for dir_path in [self.LOG_DIR, self.UPLOAD_DIR, self.KNOWLEDGE_BASE_DIR, self.REPORT_DIR]:
            os.makedirs(dir_path, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    settings = Settings()
    settings.ensure_dirs()
    return settings


# 导出配置
settings = get_settings()
