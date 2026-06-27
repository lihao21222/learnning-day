"""SupplyGuard Multi-Agent 系统"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

from models import (
    Supplier, RiskFinding, RiskReport, RiskLevel, RiskStatus,
    RiskEvent, AuditLog, SupplyChainGraph
)
from config import RISK_RULES, AGENT_CONFIG, SYSTEM_CONFIG
from knowledge_base import KnowledgeBase


@dataclass
class AgentState:
    """Agent 状态"""
    current_agent: str
    step: int
    data: Dict[str, Any]
    findings: List[RiskFinding]
    risk_score: float = 0.0


class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    @abstractmethod
    def execute(self, state: AgentState, knowledge_base: KnowledgeBase) -> AgentState:
        """执行 Agent 任务"""
        pass


class DataCollectionAgent(BaseAgent):
    """数据收集 Agent"""
    
    def __init__(self):
        super().__init__("数据收集 Agent", "负责从多个数据源收集供应商相关信息")
    
    def execute(self, state: AgentState, knowledge_base: KnowledgeBase) -> AgentState:
        print(f"[Agent] {self.name} 正在收集数据...")
        
        supplier_id = state.data.get("supplier_id")
        supplier = knowledge_base.get_supplier(supplier_id)
        
        if not supplier:
            state.data["error"] = f"供应商 {supplier_id} 不存在"
            return state
        
        # 收集数据：优先找 source == supplier_id 的文档
        supplier_info = []
        for doc in knowledge_base.documents:
            if doc.source == supplier_id:
                supplier_info.append(doc)
        
        # 如果没找到，再搜索名称
        if not supplier_info:
            supplier_info = knowledge_base.search_knowledge(supplier.name)
        
        supplier_data = {
            "supplier": supplier,
            "supplier_info": supplier_info,
            "industry_dynamics": knowledge_base.search_knowledge(supplier.industry, category="行业动态"),
            "risk_rules": knowledge_base.get_risk_rules()
        }
        
        state.data["collected_data"] = supplier_data
        print(f"[Agent] {self.name} 数据收集完成，找到 {len(supplier_info)} 个文档")
        
        return state


class RiskAnalysisAgent(BaseAgent):
    """风险分析 Agent"""
    
    def __init__(self):
        super().__init__("风险分析 Agent", "基于收集到的数据进行风险分析")
    
    def execute(self, state: AgentState, knowledge_base: KnowledgeBase) -> AgentState:
        print(f"[Agent] {self.name} 正在分析风险...")
        
        collected_data = state.data.get("collected_data", {})
        
        # 从供应商信息中分析风险
        findings = []
        supplier_docs = collected_data.get("supplier_info", [])
        
        for doc in supplier_docs:
            # 分析文档中的风险关键词
            doc_findings = knowledge_base.analyze_risk_keywords(doc.content)
            findings.extend(doc_findings)
        
        # 去重并按置信度排序
        unique_findings = {}
        for finding in findings:
            if finding.risk_type not in unique_findings:
                unique_findings[finding.risk_type] = finding
            else:
                # 合并证据
                existing = unique_findings[finding.risk_type]
                existing.evidence = list(set(existing.evidence + finding.evidence))
                existing.confidence = max(existing.confidence, finding.confidence)
        
        state.findings = list(unique_findings.values())
        
        # 计算初步风险分数
        risk_score = self._calculate_risk_score(state.findings)
        state.risk_score = risk_score
        
        print(f"[Agent] {self.name} 发现 {len(state.findings)} 个风险点，初步风险分数: {risk_score:.1f}")
        
        return state
    
    def _calculate_risk_score(self, findings: List[RiskFinding]) -> float:
        """计算风险分数"""
        if not findings:
            return 0.0
        
        total_score = 0.0
        for finding in findings:
            # 根据风险等级和置信度计算分数
            level_weight = {
                RiskLevel.LOW: 1.0,
                RiskLevel.MEDIUM: 2.0,
                RiskLevel.HIGH: 3.5,
                RiskLevel.CRITICAL: 5.0
            }
            weight = level_weight.get(finding.risk_level, 1.0)
            total_score += weight * finding.confidence / 100 * 20
        
        return min(100, total_score)


class CrossValidationAgent(BaseAgent):
    """交叉验证 Agent"""
    
    def __init__(self):
        super().__init__("交叉验证 Agent", "从多个来源验证风险信息的准确性")
    
    def execute(self, state: AgentState, knowledge_base: KnowledgeBase) -> AgentState:
        print(f"[Agent] {self.name} 正在交叉验证...")
        
        findings = state.findings
        validated_findings = []
        
        for finding in findings:
            # 模拟验证过程
            # 在真实系统中，这里会从多个独立数据源验证
            finding.verified = True  # 简化处理，标记为已验证
            
            # 为每个验证结果增加审计记录
            audit_log = AuditLog(
                log_id=str(uuid.uuid4()),
                action="交叉验证",
                actor=self.name,
                timestamp=datetime.now(),
                details={
                    "risk_type": finding.risk_type,
                    "evidence": finding.evidence,
                    "result": "已验证"
                }
            )
            
            validated_findings.append(finding)
        
        state.findings = validated_findings
        
        print(f"[Agent] {self.name} 完成 {len(validated_findings)} 个风险点验证")
        
        return state


class ReportGenerationAgent(BaseAgent):
    """报告生成 Agent"""
    
    def __init__(self):
        super().__init__("报告生成 Agent", "生成结构化的风险评估报告")
    
    def execute(self, state: AgentState, knowledge_base: KnowledgeBase) -> AgentState:
        print(f"[Agent] {self.name} 正在生成报告...")
        
        supplier = state.data["collected_data"]["supplier"]
        
        # 计算最终风险等级
        risk_score = state.risk_score
        risk_level = self._determine_risk_level(risk_score)
        
        # 生成建议
        recommendations = self._generate_recommendations(state.findings, risk_level)
        
        # 生成报告
        report = RiskReport(
            report_id=str(uuid.uuid4()),
            supplier_id=supplier.supplier_id,
            supplier_name=supplier.name,
            overall_risk_score=risk_score,
            overall_risk_level=risk_level,
            risk_findings=state.findings,
            recommendations=recommendations,
            generated_at=datetime.now()
        )
        
        state.data["report"] = report
        
        print(f"[Agent] {self.name} 报告生成完成，整体风险等级: {risk_level.value}")
        
        return state
    
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """根据分数确定风险等级"""
        thresholds = SYSTEM_CONFIG["RISK_THRESHOLD"]
        if score >= thresholds["CRITICAL"]:
            return RiskLevel.CRITICAL
        elif score >= thresholds["HIGH"]:
            return RiskLevel.HIGH
        elif score >= thresholds["MEDIUM"]:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def _generate_recommendations(self, findings: List[RiskFinding], 
                                     risk_level: RiskLevel) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("建议启动风险应急预案")
            recommendations.append("考虑寻找替代供应商")
        
        if risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("增加供应商拜访频率")
            recommendations.append("加强质量抽检")
        
        # 根据具体风险点给出建议
        for finding in findings:
            if finding.risk_type == "财务风险":
                recommendations.append("加强付款条件谈判，缩短账期")
            if finding.risk_type == "质量风险":
                recommendations.append("对关键物料进行全检")
            if finding.risk_type == "供应链中断风险":
                recommendations.append("增加安全库存")
        
        recommendations.append("持续监控供应商风险状况")
        
        return recommendations


class MultiAgentOrchestrator:
    """Multi-Agent 编排器 - 模拟 LangGraph 的编排"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        
        # 初始化 Agents
        self.agents = [
            DataCollectionAgent(),
            RiskAnalysisAgent(),
            CrossValidationAgent(),
            ReportGenerationAgent()
        ]
        
        # 工作流定义（固定顺序）
        self.workflow = [
            "data_collection",
            "risk_analysis",
            "cross_validation",
            "report_generation"
        ]
    
    def run_workflow(self, supplier_id: str) -> Dict[str, Any]:
        """运行完整工作流"""
        
        print("=" * 80)
        print("SupplyGuard: 启动供应链风险评估工作流")
        print("=" * 80)
        
        # 初始化状态
        state = AgentState(
            current_agent="初始化",
            step=0,
            data={"supplier_id": supplier_id},
            findings=[]
        )
        
        # 执行工作流
        for i, agent in enumerate(self.agents):
            state.current_agent = agent.name
            state.step = i + 1
            state = agent.execute(state, self.knowledge_base)
        
        print("=" * 80)
        print("SupplyGuard: 风险评估工作流执行完成")
        print("=" * 80)
        
        return {
            "success": True,
            "report": state.data.get("report"),
            "findings": state.findings,
            "risk_score": state.risk_score
        }
