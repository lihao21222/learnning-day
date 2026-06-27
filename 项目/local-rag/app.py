import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path
import streamlit as st
from dataclasses import dataclass
import time


@dataclass
class Document:
    """文档数据类"""
    content: str
    source: str
    file_type: str
    metadata: Dict[str, Any] = None


class SimpleKnowledgeBase:
    """简化版知识库系统"""
    
    def __init__(self):
        self.documents: List[Document] = []
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_document(self, doc: Document):
        """添加文档"""
        self.documents.append(doc)
    
    def clear_documents(self):
        """清空文档"""
        self.documents = []
    
    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """简单搜索"""
        if not self.documents:
            return []
        
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc.content.lower()
            score = 0
            
            # 简单评分机制
            if query_lower in content_lower:
                score += 100
            
            # 关键词匹配
            query_words = query_lower.split()
            for word in query_words:
                if word and len(word) >= 2:
                    if word in content_lower:
                        score += 10
            
            if score > 0:
                scored_docs.append((-score, doc))
        
        scored_docs.sort()
        results = [doc for (neg_score, doc) in scored_docs[:top_k]]
        
        # 如果没找到，返回前几个文档
        if not results and self.documents:
            return self.documents[:top_k]
        
        return results
    
    def query(self, question: str) -> Dict[str, Any]:
        """查询"""
        docs = self.search(question)
        
        if not docs:
            return {
                'answer': '抱歉，没有找到相关内容。您可以尝试添加更多文档或换个问题。',
                'sources': [],
                'documents': []
            }
        
        context = "\n\n".join([
            f"【{doc.metadata.get('file_name', '文档')}】\n{doc.content[:500]}..."
            for doc in docs
        ])
        
        answer = f"根据知识库中的信息，为您找到以下相关内容：\n\n{context}"
        
        sources = list(set([doc.metadata.get('file_name', doc.source) for doc in docs]))
        
        return {
            'answer': answer,
            'sources': sources,
            'documents': docs
        }


def init_session_state():
    """初始化会话状态"""
    if 'kb' not in st.session_state:
        st.session_state.kb = SimpleKnowledgeBase()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'documents' not in st.session_state:
        st.session_state.documents = []


def save_uploaded_file(uploaded_file) -> str:
    """保存上传的文件到临时目录"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


def load_text_file(file_path: str, original_name: str) -> Document:
    """加载文本文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Document(
            content=content,
            source=file_path,
            file_type='txt',
            metadata={'file_name': original_name}
        )
    except Exception as e:
        st.error(f"加载文件失败: {e}")
        return None


def load_pdf_file(file_path: str, original_name: str) -> List[Document]:
    """加载 PDF 文件"""
    try:
        import pypdf
        docs = []
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    docs.append(Document(
                        content=text,
                        source=file_path,
                        file_type='pdf',
                        metadata={
                            'file_name': original_name,
                            'page': page_num + 1,
                            'total_pages': len(reader.pages)
                        }
                    ))
        return docs
    except ImportError:
        st.error("请先安装 pypdf: pip install pypdf")
        return []
    except Exception as e:
        st.error(f"加载 PDF 失败: {e}")
        return []


def main():
    st.set_page_config(
        page_title="知识库问答系统",
        page_icon="📚",
        layout="wide"
    )
    
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.title("📚 知识库管理")
        
        # 文件上传
        st.header("📄 上传文档")
        uploaded_files = st.file_uploader(
            "支持 TXT、PDF（PDF 需要安装 pypdf）",
            type=['txt', 'pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file)
                file_ext = uploaded_file.name.split('.')[-1].lower()
                
                if file_ext == 'txt':
                    doc = load_text_file(file_path, uploaded_file.name)
                    if doc:
                        st.session_state.kb.add_document(doc)
                        st.session_state.documents.append(uploaded_file.name)
                        st.success(f"✅ 已添加: {uploaded_file.name}")
                
                elif file_ext == 'pdf':
                    docs = load_pdf_file(file_path, uploaded_file.name)
                    if docs:
                        for doc in docs:
                            st.session_state.kb.add_document(doc)
                        st.session_state.documents.append(uploaded_file.name)
                        st.success(f"✅ 已添加: {uploaded_file.name} ({len(docs)} 页)")
                
                # 清理临时文件
                try:
                    os.unlink(file_path)
                except:
                    pass
        
        # 已上传文件列表
        if st.session_state.documents:
            st.header("📋 已上传文档")
            for i, doc_name in enumerate(st.session_state.documents, 1):
                st.text(f"{i}. {doc_name}")
            
            if st.button("清空知识库", type="primary"):
                st.session_state.kb.clear_documents()
                st.session_state.documents = []
                st.session_state.messages = []
                st.success("已清空知识库")
                st.rerun()
        
        # 项目信息
        st.divider()
        st.markdown("""
        ### 🎯 关于项目
        这是一个基于 RAG 的本地知识库问答系统
        
        **技术栈**:
        - Streamlit (Web 界面)
        - Python (后端逻辑)
        
        **功能**:
        - 文档上传
        - 智能问答
        - 对话历史
        """)
    
    # 主界面
    st.title("🤖 本地知识库问答系统")
    st.markdown("---")
    
    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                time.sleep(0.5)
                
                if not st.session_state.documents:
                    response = "请先在侧边栏上传文档！"
                else:
                    result = st.session_state.kb.query(prompt)
                    response = result['answer']
                
                st.markdown(response)
                
                # 显示来源
                if 'sources' in locals() and result.get('sources'):
                    st.markdown(f"**参考来源**: {', '.join(result['sources'])}")
        
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
