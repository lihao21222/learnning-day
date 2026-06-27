"""SupplyGuard 数据模型"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

from config import RiskLevel


class RiskStatus(Enum):
    """风险状态"""
    PENDING = "待处理"
    REVIEWING = "审核中"
    CONFIRMED = "已确认"
    RESOLVED = "已解决"
    MITIGATED = "已缓解"
    CLOSED = "已关闭"


@dataclass
class Supplier:
    """供应商模型"""
    supplier_id: str
    name: str
    industry: str
    country: str
    risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskEvent:
    """风险事件"""
    event_id: str
    supplier_id: str
    risk_type: str
    description: str
    risk_score: float
    risk_level: RiskLevel
    timestamp: datetime
    source: str  # 信息来源
    status: RiskStatus = RiskStatus.PENDING
    verified: bool = False
    evidence: List[str] = field(default_factory=list)


@dataclass
class RiskFinding:
    """风险发现"""
    finding_id: str
    risk_type: str
    description: str
    evidence: List[str]
    confidence: float  # 置信度
    risk_level: RiskLevel


@dataclass
class AuditLog:
    """审计日志"""
    log_id: str
    action: str
    actor: str
    timestamp: datetime
    details: Dict[str, Any]


@dataclass
class RiskReport:
    """风险报告"""
    report_id: str
    supplier_id: str
    supplier_name: str
    overall_risk_score: float
    overall_risk_level: RiskLevel
    risk_findings: List[RiskFinding]
    recommendations: List[str]
    generated_at: datetime
    audit_trail: List[AuditLog] = field(default_factory=list)
    human_review: Optional[str] = None  # 人工审核意见


@dataclass
class GraphNode:
    """知识图谱节点"""
    node_id: str
    node_type: str  # supplier, product, location, industry, etc.
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    """知识图谱边"""
    edge_id: str
    from_node: str
    to_node: str
    relationship: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SupplyChainGraph:
    """供应链知识图谱"""
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    
    def add_node(self, node: GraphNode):
        self.nodes.append(node)
    
    def add_edge(self, edge: GraphEdge):
        self.edges.append(edge)
    
    def find_related_suppliers(self, supplier_id: str) -> List[str]:
        """查找与给定供应商相关的其他供应商"""
        related = []
        for edge in self.edges:
            if edge.from_node == supplier_id or edge.to_node == supplier_id:
                if edge.from_node != supplier_id:
                    related.append(edge.from_node)
                if edge.to_node != supplier_id:
                    related.append(edge.to_node)
        return list(set(related))
