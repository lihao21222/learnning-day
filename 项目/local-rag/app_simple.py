import os
import streamlit as st
from typing import List, Dict, Any
from dataclasses import dataclass
import time


@dataclass
class Document:
    content: str
    source: str
    metadata: Dict[str, Any] = None


class KnowledgeBaseSystem:
    """简单的知识库系统"""
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def add_text(self, text: str, source: str = "manual_input"):
        """添加文本"""
        self.documents.append(Document(
            content=text,
            source=source,
            metadata={'source': source}
        ))
    
    def add_file(self, file_content: str, filename: str):
        """添加文件内容"""
        self.documents.append(Document(
            content=file_content,
            source=filename,
            metadata={'file_name': filename}
        ))
    
    def clear(self):
        """清空知识库"""
        self.documents = []
    
    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """简单的搜索"""
        if not self.documents:
            return []
        
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            content_lower = doc.content.lower()
            score = 0
            
            # 完整匹配
            if query_lower in content_lower:
                score += 100
            
            # 关键词匹配
            words = query_lower.split()
            for word in words:
                if word and len(word) >= 2:
                    if word in content_lower:
                        score += 10
            
            if score > 0:
                results.append((-score, doc))
        
        results.sort()
        return [doc for (score, doc) in results[:top_k]]
    
    def query(self, question: str) -> Dict[str, Any]:
        """查询"""
        docs = self.search(question)
        
        if not docs:
            if self.documents:
                # 没有找到，返回前几个文档
                docs = self.documents[:2]
                context = "\n\n".join([
                    f"【{doc.metadata.get('file_name', '文档')}】\n{doc.content[:600]}..."
                    for doc in docs
                ])
                answer = f"没有找到完全匹配的内容，但找到了一些相关文档：\n\n{context}"
                sources = list(set([doc.metadata.get('file_name', doc.source) for doc in docs]))
            else:
                answer = "知识库是空的，请先添加文档！"
                sources = []
                docs = []
        else:
            context = "\n\n".join([
                f"【{doc.metadata.get('file_name', '文档')}】\n{doc.content[:500]}..."
                for doc in docs
            ])
            answer = f"根据知识库，为您找到以下信息：\n\n{context}"
            sources = list(set([doc.metadata.get('file_name', doc.source) for doc in docs]))
        
        return {
            'answer': answer,
            'sources': sources,
            'documents': docs
        }


def init_app():
    """初始化应用"""
    if 'kb' not in st.session_state:
        st.session_state.kb = KnowledgeBaseSystem()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'files' not in st.session_state:
        st.session_state.files = []


def load_sample_data():
    """加载示例数据"""
    sample_text = """物流包装介绍

物流包装是指在物流过程中，为了保护商品、方便储运、促进销售，按一定技术方法而采用的容器、材料及辅助物等的总体名称。

物流包装的主要功能
1. 保护功能：防止物品在运输、储存过程中不受损坏
2. 方便功能：便于装卸、搬运、保管、运输
3. 销售功能：促进商品销售
4. 信息功能：传递商品信息

绿色包装与可持续发展
绿色包装是指对生态环境和人体健康无害，能循环复用和再生利用，可促进国民经济持续发展的包装。

绿色包装的原则：
- 减量化（Reduce）：减少包装材料的使用量
- 重复使用（Reuse）：包装容器可以重复使用
- 回收利用（Recycle）：包装材料可以回收再利用
- 可降解（Degradable）：包装材料可以自然降解

物流包装标准化
物流包装标准化是指对包装的规格、尺寸、标志、技术要求等制定统一标准，以提高物流效率，降低物流成本。

标准化的好处：
- 提高装卸搬运效率
- 降低包装成本
- 便于储存和运输
- 促进国际贸易
"""
    st.session_state.kb.add_text(sample_text, "物流包装介绍.txt")
    st.session_state.files.append("物流包装介绍.txt")
    st.success("已加载示例数据！")


def main():
    st.set_page_config(
        page_title="知识库问答系统",
        page_icon="📚",
        layout="wide"
    )
    
    init_app()
    
    # 侧边栏
    with st.sidebar:
        st.title("📚 知识库管理")
        
        # 示例数据
        if st.button("加载示例数据", type="primary"):
            load_sample_data()
            st.rerun()
        
        st.divider()
        
        # 文件上传
        st.header("📄 上传文档")
        uploaded_file = st.file_uploader(
            "支持 TXT 格式",
            type=['txt'],
            help="上传文本文件到知识库"
        )
        
        if uploaded_file:
            try:
                content = uploaded_file.getvalue().decode('utf-8')
                st.session_state.kb.add_file(content, uploaded_file.name)
                st.session_state.files.append(uploaded_file.name)
                st.success(f"✅ 已添加: {uploaded_file.name}")
            except Exception as e:
                st.error(f"加载失败: {e}")
        
        st.divider()
        
        # 手动输入
        st.header("✏️ 手动输入")
        manual_text = st.text_area(
            "直接输入文本内容",
            height=150,
            placeholder="在此输入您想要添加的知识..."
        )
        if st.button("添加文本"):
            if manual_text.strip():
                st.session_state.kb.add_text(manual_text, "手动输入")
                st.session_state.files.append("手动输入")
                st.success("✅ 已添加！")
                st.rerun()
        
        st.divider()
        
        # 已添加的内容
        if st.session_state.files:
            st.header("📋 知识库内容")
            for i, filename in enumerate(st.session_state.files, 1):
                st.text(f"{i}. {filename}")
            
            if st.button("清空知识库"):
                st.session_state.kb.clear()
                st.session_state.files = []
                st.session_state.messages = []
                st.success("已清空！")
                st.rerun()
        
        st.divider()
        st.markdown("""
        ### 🎯 使用说明
        1. 点击"加载示例数据"或上传文件
        2. 在右侧输入问题
        3. 查看回答和参考来源
        """)
    
    # 主界面
    st.title("🤖 本地知识库问答系统")
    
    st.markdown("""
    欢迎使用基于 RAG 技术的本地知识库问答系统！
    
    **特点**：
    - 📄 支持上传本地文档
    - 🔍 智能检索相关内容
    - 💬 自然语言问答
    - 🔒 数据完全本地化
    """)
    
    st.divider()
    
    # 对话区域
    st.subheader("💬 开始对话")
    
    # 显示历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("正在检索..."):
                time.sleep(0.5)
                result = st.session_state.kb.query(prompt)
                
                st.markdown(result['answer'])
                
                if result['sources']:
                    st.markdown(f"**📄 参考来源**: {', '.join(result['sources'])}")
        
        st.session_state.messages.append({"role": "assistant", "content": result['answer']})


if __name__ == "__main__":
    main()
