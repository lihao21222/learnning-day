# 项目配置文件
import os


class Config:
    """基础配置"""
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 知识库目录
    KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')
    
    # 向量数据库目录
    VECTOR_DB_DIR = os.path.join(BASE_DIR, 'vector_db')
    
    # 支持的文档格式
    SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx']
    
    # 文本分割配置
    CHUNK_SIZE = 500  # 每个块的大小（字符数）
    CHUNK_OVERLAP = 50  # 块之间的重叠大小
    
    # 检索配置
    TOP_K = 3  # 返回最相关的 K 个文档
    
    # 模型配置
    EMBEDDING_MODEL = 'shibing624/text2vec-base-chinese'  # 中文嵌入模型
    LLM_MODEL = 'Qwen/Qwen2.5-0.5B-Instruct'  # 本地 LLM 模型


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = 'INFO'


# 根据环境选择配置
config = DevelopmentConfig()
