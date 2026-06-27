"""SupplyGuard Web 界面"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from knowledge_base import KnowledgeBase
from agents import MultiAgentOrchestrator
from config import RiskLevel
from models import RiskReport


# ========== 页面配置 ==========
st.set_page_config(
    page_title="SupplyGuard - 供应链风控平台",
    page_icon="🛡️",
    layout="wide"
)


# ========== 初始化 ==========
@st.cache_resource
def get_knowledge_base():
    return KnowledgeBase()


@st.cache_resource
def get_orchestrator(kb):
    return MultiAgentOrchestrator(kb)


kb = get_knowledge_base()
orchestrator = get_orchestrator(kb)


# ========== 侧边栏 ==========
st.sidebar.title("🛡️ SupplyGuard")
st.sidebar.markdown("---")

# 页面导航
page = st.sidebar.radio(
    "功能模块",
    ["🏠 仪表板", "🔍 供应商风险评估", "📚 知识库", "📊 风险报告", "⚙️ 配置"]
)


# ========== 页面 1: 仪表板 ==========
if page == "🏠 仪表板":
    st.title("供应链风险监控仪表板")
    st.markdown("---")
    
    # 获取所有供应商
    suppliers = kb.get_all_suppliers()
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "供应商总数",
            len(suppliers),
            "+0"
        )
    
    # 统计各风险等级供应商数量
    risk_count = {
        RiskLevel.LOW: 0,
        RiskLevel.MEDIUM: 0,
        RiskLevel.HIGH: 0,
        RiskLevel.CRITICAL: 0
    }
    
    for supplier in suppliers:
        risk_count[supplier.risk_level] += 1
    
    with col2:
        st.metric(
            "低风险供应商",
            risk_count[RiskLevel.LOW],
            "稳定"
        )
    
    with col3:
        medium_high = risk_count[RiskLevel.MEDIUM] + risk_count[RiskLevel.HIGH]
        st.metric(
            "中高风险供应商",
            medium_high,
            "需要关注"
        )
    
    with col4:
        st.metric(
            "严重风险供应商",
            risk_count[RiskLevel.CRITICAL],
            "⚠️ 紧急"
        )
    
    st.markdown("---")
    
    # 图表区域
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("供应商风险分布")
        
        risk_data = pd.DataFrame({
            "风险等级": ["低", "中", "高", "严重"],
            "数量": [
                risk_count[RiskLevel.LOW],
                risk_count[RiskLevel.MEDIUM],
                risk_count[RiskLevel.HIGH],
                risk_count[RiskLevel.CRITICAL]
            ],
            "颜色": ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
        })
        
        fig = px.bar(
            risk_data,
            x="风险等级",
            y="数量",
            color="颜色",
            color_discrete_map=dict(zip(risk_data["颜色"], risk_data["颜色"])),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.subheader("供应商行业分布")
        
        industry_data = {}
        for supplier in suppliers:
            industry_data[supplier.industry] = industry_data.get(supplier.industry, 0) + 1
        
        fig = px.pie(
            values=list(industry_data.values()),
            names=list(industry_data.keys()),
            title="行业分布",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 供应商列表
    st.subheader("供应商列表")
    
    supplier_df = pd.DataFrame([
        {
            "供应商ID": s.supplier_id,
            "供应商名称": s.name,
            "行业": s.industry,
            "国家": s.country,
            "风险分数": s.risk_score,
            "风险等级": s.risk_level.value,
            "最后更新": s.last_updated.strftime("%Y-%m-%d")
        }
        for s in suppliers
    ])
    
    st.dataframe(supplier_df, use_container_width=True)


# ========== 页面 2: 供应商风险评估 ==========
elif page == "🔍 供应商风险评估":
    st.title("供应商风险评估")
    st.markdown("---")
    
    # 选择供应商
    suppliers = kb.get_all_suppliers()
    supplier_options = {f"{s.supplier_id} - {s.name}": s for s in suppliers}
    
    selected_option = st.selectbox(
        "选择要评估的供应商",
        list(supplier_options.keys())
    )
    
    if selected_option:
        selected_supplier = supplier_options[selected_option]
        
        st.markdown("### 供应商信息")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.info(f"**供应商ID**: {selected_supplier.supplier_id}")
        with info_col2:
            st.info(f"**行业**: {selected_supplier.industry}")
        with info_col3:
            st.info(f"**国家**: {selected_supplier.country}")
        
        st.markdown("---")
        
        # 执行评估
        if st.button("🔍 启动风险评估", type="primary"):
            with st.spinner("正在执行风险评估..."):
                result = orchestrator.run_workflow(selected_supplier.supplier_id)
                
                if result["success"] and "report" in result:
                    report = result["report"]
                    
                    st.success("✅ 风险评估完成！")
                    st.markdown("---")
                    
                    # 显示结果
                    display_risk_report(report)
                    
                    # 保存到 session state
                    st.session_state[f"report_{selected_supplier.supplier_id}"] = report


# ========== 页面 3: 知识库 ==========
elif page == "📚 知识库":
    st.title("供应链知识库")
    st.markdown("---")
    
    # 搜索
    search_query = st.text_input("🔍 搜索知识库", placeholder="输入关键词搜索...")
    
    if search_query:
        results = kb.search_knowledge(search_query)
        
        if results:
            st.success(f"找到 {len(results)} 个相关文档")
            
            for doc in results:
                with st.expander(f"📄 {doc.title} ({doc.category})"):
                    st.markdown(doc.content)
                    st.caption(f"来源: {doc.source} | 创建时间: {doc.created_at.strftime('%Y-%m-%d')}")
        else:
            st.info("未找到相关文档")
    else:
        # 显示所有文档
        categories = list(set(doc.category for doc in kb.documents))
        
        selected_category = st.selectbox(
            "选择知识分类",
            ["全部"] + categories
        )
        
        docs_to_show = kb.documents
        if selected_category != "全部":
            docs_to_show = [doc for doc in kb.documents if doc.category == selected_category]
        
        for doc in docs_to_show:
            with st.expander(f"📄 {doc.title} ({doc.category})"):
                st.markdown(doc.content)
                st.caption(f"来源: {doc.source} | 创建时间: {doc.created_at.strftime('%Y-%m-%d')}")


# ========== 页面 4: 风险报告 ==========
elif page == "📊 风险报告":
    st.title("风险报告")
    st.markdown("---")
    
    # 查看已保存的报告
    if "reports" not in st.session_state:
        st.session_state.reports = []
    
    # 显示报告列表
    suppliers = kb.get_all_suppliers()
    
    if suppliers:
        report_supplier = st.selectbox(
            "选择供应商查看报告",
            [s.name for s in suppliers]
        )
        
        selected_supplier = next((s for s in suppliers if s.name == report_supplier), None)
        
        if selected_supplier:
            report_key = f"report_{selected_supplier.supplier_id}"
            
            if report_key in st.session_state:
                report = st.session_state[report_key]
                display_risk_report(report)
            else:
                st.info("还没有该供应商的风险报告，请先在'供应商风险评估'页面执行评估")


# ========== 页面 5: 配置 ==========
elif page == "⚙️ 配置":
    st.title("系统配置")
    st.markdown("---")
    
    st.subheader("风险规则配置")
    
    from config import RISK_RULES
    
    for rule in RISK_RULES:
        with st.expander(f"📋 {rule.name} (权重: {rule.weight})"):
            st.write(f"**描述**: {rule.description}")
            st.write(f"**风险等级**: {rule.risk_level.value}")
            st.write(f"**关键词**: {', '.join(rule.keywords)}")
    
    st.markdown("---")
    
    st.subheader("系统设置")
    
    st.checkbox("启用人工干预 (Human-in-the-Loop)", value=True)
    st.checkbox("记录审计日志", value=True)
    
    st.slider("风险告警阈值", 0, 100, 60)


# ========== 辅助函数: 显示风险报告 ==========
def display_risk_report(report: RiskReport):
    """显示风险报告"""
    
    st.subheader("📊 风险评估报告")
    
    # 整体风险分数和等级
    col1, col2 = st.columns(2)
    
    with col1:
        # 仪表盘
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=report.overall_risk_score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "风险分数"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": get_risk_color(report.overall_risk_level)},
                "steps": [
                    {"range": [0, 20], "color": "#2ecc71"},
                    {"range": [20, 40], "color": "#f1c40f"},
                    {"range": [40, 60], "color": "#e67e22"},
                    {"range": [60, 80], "color": "#e74c3c"},
                    {"range": [80, 100], "color": "#c0392b"},
                ]
            }
        ))
        
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 风险等级
        color = get_risk_color(report.overall_risk_level)
        st.markdown(
            f"<h2 style='text-align: center; color: {color}'>{report.overall_risk_level.value}风险</h2>",
            unsafe_allow_html=True
        )
        
        st.markdown(f"**报告ID**: {report.report_id}")
        st.markdown(f"**供应商**: {report.supplier_name}")
        st.markdown(f"**生成时间**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    
    # 风险发现
    st.subheader("🔍 风险发现")
    
    if report.risk_findings:
        findings_data = []
        for finding in report.risk_findings:
            findings_data.append({
                "风险类型": finding.risk_type,
                "风险等级": finding.risk_level.value,
                "置信度": f"{finding.confidence:.0f}%",
                "证据": ", ".join(finding.evidence),
                "描述": finding.description
            })
        
        findings_df = pd.DataFrame(findings_data)
        st.dataframe(findings_df, use_container_width=True)
    else:
        st.info("未发现风险点")
    
    st.markdown("---")
    
    # 建议
    st.subheader("💡 建议措施")
    
    if report.recommendations:
        for i, rec in enumerate(report.recommendations, 1):
            st.markdown(f"{i}. {rec}")
    else:
        st.info("暂无建议")


def get_risk_color(risk_level: RiskLevel) -> str:
    """获取风险等级对应的颜色"""
    color_map = {
        RiskLevel.LOW: "#2ecc71",
        RiskLevel.MEDIUM: "#f1c40f",
        RiskLevel.HIGH: "#e67e22",
        RiskLevel.CRITICAL: "#e74c3c"
    }
    return color_map.get(risk_level, "#95a5a6")
