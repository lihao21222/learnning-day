"""SupplyGuard 配置文件"""
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "严重"


@dataclass
class RiskRule:
    """风险规则"""
    name: str
    description: str
    weight: float  # 权重
    keywords: List[str]
    risk_level: RiskLevel


# ========== 风险规则配置 ==========
RISK_RULES: List[RiskRule] = [
    RiskRule(
        name="财务风险",
        description="供应商出现财务问题，如亏损、负债高",
        weight=0.25,
        keywords=["亏损", "负债", "债务", "破产", "资金链", "流动性", "财务恶化"],
        risk_level=RiskLevel.HIGH
    ),
    RiskRule(
        name="质量风险",
        description="产品质量问题，如不合格、召回",
        weight=0.20,
        keywords=["质量", "不合格", "召回", "缺陷", "质检", "品控"],
        risk_level=RiskLevel.HIGH
    ),
    RiskRule(
        name="供应链中断风险",
        description="供应中断、产能不足",
        weight=0.20,
        keywords=["停产", "断供", "缺货", "产能不足", "停工", "罢工"],
        risk_level=RiskLevel.CRITICAL
    ),
    RiskRule(
        name="合规风险",
        description="合规问题，如环保、劳动",
        weight=0.15,
        keywords=["环保", "污染", "罚款", "合规", "劳动法", "诉讼"],
        risk_level=RiskLevel.MEDIUM
    ),
    RiskRule(
        name="地缘政治风险",
        description="地缘政治、贸易摩擦",
        weight=0.10,
        keywords=["关税", "制裁", "贸易战", "地缘政治", "出口限制"],
        risk_level=RiskLevel.MEDIUM
    ),
    RiskRule(
        name="供应商关系风险",
        description="合作关系、信用问题",
        weight=0.10,
        keywords=["逾期", "信用", "拖欠", "合同纠纷", "毁约"],
        risk_level=RiskLevel.MEDIUM
    ),
]


# ========== 供应商评估维度 ==========
SUPPLIER_DIMENSIONS = [
    "财务状况",
    "生产能力",
    "质量管理",
    "技术能力",
    "交付能力",
    "成本竞争力",
    "合规状况",
    "可持续发展"
]


# ========== Agent 配置 ==========
AGENT_CONFIG = {
    "data_agent": {
        "name": "数据收集 Agent",
        "role": "负责从多个数据源收集供应商相关信息"
    },
    "analysis_agent": {
        "name": "风险分析 Agent",
        "role": "基于收集到的数据进行风险分析"
    },
    "validate_agent": {
        "name": "交叉验证 Agent",
        "role": "从多个来源验证风险信息的准确性"
    },
    "report_agent": {
        "name": "报告生成 Agent",
        "role": "生成结构化的风险评估报告"
    }
}


# ========== 系统配置 ==========
SYSTEM_CONFIG = {
    "KNOWLEDGE_BASE_DIR": "data/knowledge_base",
    "SUPPLIER_DATA_DIR": "data/suppliers",
    "REPORT_DIR": "data/reports",
    "LOG_DIR": "logs",
    
    "RISK_THRESHOLD": {
        "LOW": 20,
        "MEDIUM": 40,
        "HIGH": 60,
        "CRITICAL": 80
    },
    
    "HUMAN_IN_THE_LOOP": True,  # 是否启用人工干预
    "AUDIT_TRAIL": True  # 是否记录审计日志
}
