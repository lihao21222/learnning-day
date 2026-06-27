"""供应链知识库模块"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
import json
from datetime import datetime

from config import RISK_RULES, RiskLevel, SYSTEM_CONFIG
from models import Supplier, RiskFinding


@dataclass
class KnowledgeDoc:
    """知识文档"""
    doc_id: str
    title: str
    content: str
    category: str  # 风险规则、供应商信息、行业动态等
    source: str
    created_at: datetime


class KnowledgeBase:
    """供应链知识库"""
    
    def __init__(self):
        self.documents: List[KnowledgeDoc] = []
        self.suppliers: Dict[str, Supplier] = {}
        self.knowledge_dir = SYSTEM_CONFIG["KNOWLEDGE_BASE_DIR"]
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        
        # 示例供应商信息
        sample_suppliers = [
            Supplier(
                supplier_id="SUP-001",
                name="鸿远精密制造有限公司",
                industry="电子制造",
                country="中国",
                risk_score=15.0,
                risk_level=RiskLevel.LOW
            ),
            Supplier(
                supplier_id="SUP-002",
                name="泰华电子元件厂",
                industry="电子元件",
                country="中国",
                risk_score=45.0,
                risk_level=RiskLevel.MEDIUM
            ),
            Supplier(
                supplier_id="SUP-003",
                name="盛科新材料股份有限公司",
                industry="化工材料",
                country="中国",
                risk_score=70.0,
                risk_level=RiskLevel.HIGH
            ),
        ]
        
        for supplier in sample_suppliers:
            self.suppliers[supplier.supplier_id] = supplier
        
        # 示例风险规则文档
        risk_rule_docs = [
            KnowledgeDoc(
                doc_id="RULE-001",
                title="财务风险识别指南",
                content="""财务风险识别要点：
                1. 连续两年亏损是高风险信号
                2. 资产负债率超过70%应警惕
                3. 现金流紧张可能导致资金链断裂
                4. 拖欠货款是早期预警信号
                5. 银行账户被冻结是严重风险""",
                category="风险规则",
                source="系统内置",
                created_at=datetime.now()
            ),
            KnowledgeDoc(
                doc_id="RULE-002",
                title="质量风险评估标准",
                content="""质量风险评估标准：
                1. 年度内质量投诉超过5次为高风险
                2. 产品被召回是严重质量事件
                3. 第三方质检不合格应重点关注
                4. 生产过程质量控制流程缺失存在隐患""",
                category="风险规则",
                source="系统内置",
                created_at=datetime.now()
            ),
            KnowledgeDoc(
                doc_id="NEWS-001",
                title="电子元件行业近期动态",
                content="""据报道，电子元件行业近期面临以下挑战：
                - 部分小型工厂因资金压力出现停产
                - 原材料价格波动较大
                - 部分地区环保政策趋严，部分工厂面临整改""",
                category="行业动态",
                source="行业报告",
                created_at=datetime.now()
            ),
        ]
        
        self.documents.extend(risk_rule_docs)
        
        # 示例供应商数据文档
        supplier_docs = [
            KnowledgeDoc(
                doc_id="SUPDOC-002",
                title="泰华电子元件厂近期信息",
                content="""泰华电子元件厂近期状况：
                - 2025年Q3财报显示利润同比下降25%
                - 有客户反映部分批次产品质量不稳定
                - 工厂正在进行环保整改，产能下降15%
                - 已连续三个月延迟交货""",
                category="供应商信息",
                source="SUP-002",
                created_at=datetime.now()
            ),
            KnowledgeDoc(
                doc_id="SUPDOC-003",
                title="盛科新材料风险警示",
                content="""盛科新材料存在以下风险：
                - 财务报表显示负债较高，资产负债率达78%
                - 因环保问题被当地环保部门多次罚款
                - 主要客户订单减少30%
                - 有供应商反映货款拖欠超过60天
                - 部分生产线已停产进行整改""",
                category="供应商信息",
                source="SUP-003",
                created_at=datetime.now()
            ),
        ]
        
        self.documents.extend(supplier_docs)
    
    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        """获取供应商信息"""
        return self.suppliers.get(supplier_id)
    
    def get_all_suppliers(self) -> List[Supplier]:
        """获取所有供应商"""
        return list(self.suppliers.values())
    
    def search_knowledge(self, query: str, category: Optional[str] = None) -> List[KnowledgeDoc]:
        """搜索知识库"""
        results = []
        query_lower = query.lower()
        
        for doc in self.documents:
            if category and doc.category != category:
                continue
            
            if query_lower in doc.title.lower() or query_lower in doc.content.lower():
                results.append(doc)
        
        return results
    
    def get_risk_rules(self):
        """获取风险规则"""
        return RISK_RULES
    
    def analyze_risk_keywords(self, text: str) -> List[RiskFinding]:
        """分析文本中的风险关键词"""
        findings = []
        
        for rule in RISK_RULES:
            matches = []
            for keyword in rule.keywords:
                if keyword in text:
                    matches.append(keyword)
            
            if matches:
                # 根据匹配关键词数量计算置信度
                confidence = min(100, len(matches) * 30 + 40)
                
                findings.append(RiskFinding(
                    finding_id=f"FIND-{len(findings)+1}",
                    risk_type=rule.name,
                    description=rule.description,
                    evidence=matches,
                    confidence=confidence,
                    risk_level=rule.risk_level
                ))
        
        return findings
    
    def add_document(self, doc: KnowledgeDoc):
        """添加文档"""
        self.documents.append(doc)
