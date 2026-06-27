"""
SupplyGuard API Server (FastAPI)
提供 RESTful API 接口，支持供应链风险评估
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import logging

# 导入项目模块
from config import RiskLevel
from models import Supplier, RiskReport, RiskFinding, AuditLog
from knowledge_base import KnowledgeBase
from agents import MultiAgentOrchestrator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("supplyguard-api")

# 初始化 FastAPI
app = FastAPI(
    title="SupplyGuard API",
    description="供应链风控 Agent 平台 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化系统组件（单例）
kb = KnowledgeBase()
orchestrator = MultiAgentOrchestrator(kb)

# ============================================
# Pydantic 模型定义
# ============================================

class SupplierCreate(BaseModel):
    """供应商创建模型"""
    name: str
    industry: str
    country: str
    metadata: Optional[Dict[str, Any]] = None


class RiskAssessmentRequest(BaseModel):
    """风险评估请求模型"""
    supplier_id: str


class RiskAssessmentResponse(BaseModel):
    """风险评估响应模型"""
    success: bool
    report_id: Optional[str] = None
    supplier_id: str
    supplier_name: str
    overall_risk_score: float
    overall_risk_level: str
    risk_findings: List[Dict[str, Any]]
    recommendations: List[str]
    generated_at: str
    message: Optional[str] = None


# ============================================
# 健康检查与系统信息
# ============================================

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "SupplyGuard API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# ============================================
# 供应商管理接口
# ============================================

@app.get("/api/suppliers", tags=["Suppliers"])
async def get_all_suppliers():
    """获取所有供应商列表"""
    suppliers = kb.get_all_suppliers()
    return {
        "count": len(suppliers),
        "data": [
            {
                "supplier_id": s.supplier_id,
                "name": s.name,
                "industry": s.industry,
                "country": s.country,
                "risk_score": s.risk_score,
                "risk_level": s.risk_level.value
            }
            for s in suppliers
        ]
    }


@app.get("/api/suppliers/{supplier_id}", tags=["Suppliers"])
async def get_supplier(supplier_id: str):
    """获取单个供应商详情"""
    supplier = kb.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    return {
        "supplier_id": supplier.supplier_id,
        "name": supplier.name,
        "industry": supplier.industry,
        "country": supplier.country,
        "risk_score": supplier.risk_score,
        "risk_level": supplier.risk_level.value,
        "last_updated": supplier.last_updated.isoformat()
    }


@app.post("/api/suppliers", tags=["Suppliers"])
async def create_supplier(supplier_data: SupplierCreate):
    """创建新供应商"""
    supplier_id = f"SUP-{len(kb.suppliers) + 1:03d}"
    
    new_supplier = Supplier(
        supplier_id=supplier_id,
        name=supplier_data.name,
        industry=supplier_data.industry,
        country=supplier_data.country,
        risk_score=0.0,
        risk_level=RiskLevel.LOW,
        metadata=supplier_data.metadata or {}
    )
    
    kb.suppliers[supplier_id] = new_supplier
    logger.info(f"Created new supplier: {supplier_id} - {new_supplier.name}")
    
    return {
        "success": True,
        "supplier_id": supplier_id,
        "message": "供应商创建成功"
    }


# ============================================
# 风险评估接口
# ============================================

@app.post("/api/assess", tags=["Risk Assessment"], response_model=RiskAssessmentResponse)
async def assess_supplier_risk(request: RiskAssessmentRequest):
    """执行供应商风险评估"""
    logger.info(f"Received risk assessment request for supplier: {request.supplier_id}")
    
    try:
        result = orchestrator.run_workflow(request.supplier_id)
        
        if not result["success"] or "report" not in result:
            raise HTTPException(status_code=500, detail="风险评估执行失败")
        
        report = result["report"]
        
        return RiskAssessmentResponse(
            success=True,
            report_id=report.report_id,
            supplier_id=report.supplier_id,
            supplier_name=report.supplier_name,
            overall_risk_score=report.overall_risk_score,
            overall_risk_level=report.overall_risk_level.value,
            risk_findings=[
                {
                    "finding_id": f.finding_id,
                    "risk_type": f.risk_type,
                    "description": f.description,
                    "confidence": f.confidence,
                    "risk_level": f.risk_level.value,
                    "evidence": f.evidence
                }
                for f in report.risk_findings
            ],
            recommendations=report.recommendations,
            generated_at=report.generated_at.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Risk assessment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 知识库接口
# ============================================

@app.get("/api/knowledge/search", tags=["Knowledge Base"])
async def search_knowledge(query: str, category: Optional[str] = None):
    """搜索知识库"""
    docs = kb.search_knowledge(query, category)
    return {
        "count": len(docs),
        "data": [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                "category": doc.category,
                "source": doc.source
            }
            for doc in docs
        ]
    }


@app.get("/api/knowledge/rules", tags=["Knowledge Base"])
async def get_risk_rules():
    """获取风险规则列表"""
    rules = kb.get_risk_rules()
    return {
        "count": len(rules),
        "data": [
            {
                "name": r.name,
                "description": r.description,
                "weight": r.weight,
                "risk_level": r.risk_level.value,
                "keywords": r.keywords
            }
            for r in rules
        ]
    }


# ============================================
# 启动入口
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("="*80)
    print("SupplyGuard API Server")
    print("="*80)
    print(f"Docs: http://localhost:8000/docs")
    print("="*80)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
