"""
SupplyGuard 数据库抽象层
使用 SQLAlchemy ORM，支持 SQLite（开发）和 PostgreSQL（生产）
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from dataclasses import asdict

try:
    from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON, Boolean, Index
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.exc import SQLAlchemyError
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False


# 定义枚举
class RiskLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskStatusEnum(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    CONFIRMED = "confirmed"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    CLOSED = "closed"


if SQLALCHEMY_AVAILABLE:
    # 如果 SQLAlchemy 可用，定义 ORM 模型
    Base = declarative_base()
    
    class SupplierDB(Base):
        """供应商数据表"""
        __tablename__ = "suppliers"
        
        id = Column(String, primary_key=True, index=True)
        name = Column(String, index=True, nullable=False)
        industry = Column(String, index=True)
        country = Column(String)
        risk_score = Column(Float, default=0.0)
        risk_level = Column(String, default="low")  # 存字符串，避免枚举依赖
        metadata = Column(JSON, default=dict)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        __table_args__ = (
            Index("idx_supplier_risk_level", "risk_level"),
            Index("idx_supplier_industry", "industry"),
        )
    
    class RiskFindingDB(Base):
        """风险发现数据表"""
        __tablename__ = "risk_findings"
        
        id = Column(String, primary_key=True)
        supplier_id = Column(String, index=True, nullable=False)
        risk_type = Column(String, index=True, nullable=False)
        description = Column(Text)
        confidence = Column(Float)
        risk_level = Column(String, index=True)
        evidence = Column(JSON, default=list)
        verified = Column(Boolean, default=False)
        status = Column(String, default="pending")
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class RiskReportDB(Base):
        """风险报告数据表"""
        __tablename__ = "risk_reports"
        
        id = Column(String, primary_key=True)
        supplier_id = Column(String, index=True, nullable=False)
        supplier_name = Column(String)
        overall_risk_score = Column(Float)
        overall_risk_level = Column(String)
        recommendations = Column(JSON, default=list)
        findings_summary = Column(JSON, default=dict)
        human_reviewed = Column(Boolean, default=False)
        human_review_note = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow)
    
    class AuditLogDB(Base):
        """审计日志数据表"""
        __tablename__ = "audit_logs"
        
        id = Column(String, primary_key=True)
        action = Column(String, index=True, nullable=False)
        actor = Column(String, index=True)
        entity_type = Column(String)
        entity_id = Column(String)
        details = Column(JSON, default=dict)
        timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class Database:
    """
    数据库管理器
    支持：
    - 内存模式（默认，演示用）
    - SQLite（开发）
    - PostgreSQL（生产）
    """
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url
        self.use_sqlalchemy = SQLALCHEMY_AVAILABLE and database_url is not None
        
        if self.use_sqlalchemy:
            self.engine = create_engine(database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self._init_tables()
        else:
            # 内存数据存储（演示模式）
            self.suppliers: Dict[str, Dict] = {}
            self.reports: Dict[str, Dict] = {}
            self.findings: Dict[str, Dict] = {}
            self.audit_logs: List[Dict] = []
    
    def _init_tables(self) -> None:
        """初始化数据库表"""
        if self.use_sqlalchemy:
            try:
                Base.metadata.create_all(bind=self.engine)
            except Exception as e:
                print(f"Error creating tables: {e}")
    
    def get_session(self) -> Optional[Session]:
        """获取数据库会话（SQLAlchemy 模式）"""
        if self.use_sqlalchemy:
            return self.SessionLocal()
        return None
    
    # ========== 供应商操作 ==========
    
    def save_supplier(self, supplier_data: Dict[str, Any]) -> bool:
        """保存供应商"""
        if self.use_sqlalchemy:
            db = self.get_session()
            try:
                db_supplier = SupplierDB(**supplier_data)
                existing = db.query(SupplierDB).filter(SupplierDB.id == supplier_data.get("id")).first()
                if existing:
                    for k, v in supplier_data.items():
                        if k != "id":
                            setattr(existing, k, v)
                else:
                    db.add(db_supplier)
                db.commit()
                return True
            except SQLAlchemyError as e:
                print(f"Database error: {e}")
                db.rollback()
                return False
            finally:
                db.close()
        else:
            # 内存模式
            self.suppliers[supplier_data.get("id")] = supplier_data
            return True
    
    def get_supplier(self, supplier_id: str) -> Optional[Dict]:
        """获取供应商"""
        if self.use_sqlalchemy:
            db = self.get_session()
            try:
                supplier = db.query(SupplierDB).filter(SupplierDB.id == supplier_id).first()
                if supplier:
                    return {c.name: getattr(supplier, c.name) for c in supplier.__table__.columns}
                return None
            finally:
                db.close()
        else:
            return self.suppliers.get(supplier_id)
    
    # ========== 报告操作 ==========
    
    def save_report(self, report_data: Dict[str, Any]) -> bool:
        """保存风险报告"""
        if self.use_sqlalchemy:
            db = self.get_session()
            try:
                db_report = RiskReportDB(**report_data)
                db.add(db_report)
                db.commit()
                return True
            except SQLAlchemyError as e:
                print(f"Database error: {e}")
                db.rollback()
                return False
            finally:
                db.close()
        else:
            self.reports[report_data.get("id")] = report_data
            return True
    
    # ========== 审计日志 ==========
    
    def log_audit(self, action: str, actor: str, entity_type: Optional[str] = None,
                  entity_id: Optional[str] = None, details: Optional[Dict] = None) -> None:
        """记录审计日志"""
        log_entry = {
            "id": f"audit-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            "action": action,
            "actor": actor,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "details": details or {},
            "timestamp": datetime.utcnow()
        }
        
        if self.use_sqlalchemy:
            db = self.get_session()
            try:
                db_log = AuditLogDB(**log_entry)
                db.add(db_log)
                db.commit()
            except SQLAlchemyError as e:
                print(f"Audit log error: {e}")
                db.rollback()
            finally:
                db.close()
        else:
            self.audit_logs.append(log_entry)


# 全局数据库实例（初始化为内存模式）
db: Optional[Database] = None


def init_db(database_url: Optional[str] = None) -> Database:
    """初始化数据库"""
    global db
    if db is None:
        db = Database(database_url)
    return db


def get_db() -> Database:
    """获取数据库实例"""
    global db
    if db is None:
        db = Database()
    return db
