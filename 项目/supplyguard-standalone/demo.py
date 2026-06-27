"""SupplyGuard 命令行演示"""
from knowledge_base import KnowledgeBase
from agents import MultiAgentOrchestrator
from config import RiskLevel


def print_header(title: str):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_risk_report(report):
    print_header("风险评估报告")
    
    print(f"\n供应商: {report.supplier_name} ({report.supplier_id})")
    print(f"风险分数: {report.overall_risk_score:.1f}")
    print(f"风险等级: {report.overall_risk_level.value}")
    print(f"报告生成时间: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "-"*80)
    print("风险发现:")
    print("-"*80)
    
    if report.risk_findings:
        for i, finding in enumerate(report.risk_findings, 1):
            print(f"\n{i}. {finding.risk_type}")
            print(f"   风险等级: {finding.risk_level.value}")
            print(f"   置信度: {finding.confidence:.0f}%")
            print(f"   证据: {', '.join(finding.evidence)}")
    else:
        print("   未发现风险点")
    
    print("\n" + "-"*80)
    print("建议措施:")
    print("-"*80)
    
    if report.recommendations:
        for i, rec in enumerate(report.recommendations, 1):
            print(f"\n{i}. {rec}")
    else:
        print("   暂无建议")


def main():
    print_header("SupplyGuard - 供应链风控 Agent 平台")
    
    # 初始化系统
    kb = KnowledgeBase()
    orchestrator = MultiAgentOrchestrator(kb)
    
    # 获取所有供应商
    suppliers = kb.get_all_suppliers()
    
    print(f"\n已加载 {len(suppliers)} 个供应商:")
    for i, supplier in enumerate(suppliers, 1):
        print(f"  {i}. {supplier.name} ({supplier.supplier_id}) - {supplier.industry}")
    
    # 演示：评估一个供应商
    print("\n" + "="*80)
    print("演示：评估供应商 SUP-003 (盛科新材料)")
    print("="*80)
    
    result = orchestrator.run_workflow("SUP-003")
    
    if result["success"] and "report" in result:
        print_risk_report(result["report"])
    
    print("\n" + "="*80)
    print("演示：评估供应商 SUP-002 (泰华电子)")
    print("="*80)
    
    result = orchestrator.run_workflow("SUP-002")
    
    if result["success"] and "report" in result:
        print_risk_report(result["report"])
    
    print("\n" + "="*80)
    print("演示完成！")
    print("="*80)
    print("\n您可以:")
    print("1. 运行 'streamlit run app.py' 启动 Web 界面")
    print("2. 修改 data/knowledge_base/ 下的文档扩展知识库")


if __name__ == "__main__":
    main()
