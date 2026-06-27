import os
from typing import List, Dict, Any
from dataclasses import dataclass
import sys

from document_loader_pro import DocumentLoaderPro
from logger import setup_logger

logger = setup_logger()


@dataclass
class Document:
    content: str
    source: str
    file_type: str
    metadata: Dict[str, Any] = None


class TextSplitter:
    """文本分割器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str, source: str, file_type: str, metadata: Dict = None) -> List[Document]:
        """分割文本"""
        chunks = []
        start = 0
        text_length = len(text)
        chunk_id = 0
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk_content = text[start:end]
            chunk_metadata = dict(metadata) if metadata else {}
            chunk_metadata['chunk_id'] = chunk_id
            
            chunks.append(Document(
                content=chunk_content,
                source=source,
                file_type=file_type,
                metadata=chunk_metadata
            ))
            
            chunk_id += 1
            start += self.chunk_size - self.chunk_overlap
        
        return chunks


class SimpleRetriever:
    """简易检索器"""
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def add_documents(self, documents: List[Document]):
        self.documents.extend(documents)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        if not self.documents:
            return []
        
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc.content.lower()
            score = 0
            
            if query_lower in content_lower:
                score += 100
            
            query_words = query_lower.split()
            for word in query_words:
                if word and len(word) >= 2:
                    if word in content_lower:
                        score += 10
            
            if score > 0:
                scored_docs.append((-score, doc))
        
        scored_docs.sort()
        return [doc for (score, doc) in scored_docs[:top_k]]


class RAGSystemPro:
    """增强版 RAG 系统"""
    
    def __init__(self, knowledge_base_dir: str = 'knowledge_base'):
        self.loader = DocumentLoaderPro(knowledge_base_dir)
        self.splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
        self.retriever = SimpleRetriever()
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """初始化系统"""
        logger.info("开始初始化 RAG 系统...")
        
        raw_documents = self.loader.load_directory()
        
        if not raw_documents:
            logger.error("没有找到任何文档！")
            return False
        
        logger.info(f"加载了 {len(raw_documents)} 个原始文档")
        
        all_chunks = []
        for doc in raw_documents:
            chunks = self.splitter.split_text(
                text=doc.content,
                source=doc.source,
                file_type=doc.file_type,
                metadata=doc.metadata
            )
            all_chunks.extend(chunks)
        
        self.retriever.add_documents(all_chunks)
        logger.info(f"文档分割完成，共 {len(all_chunks)} 个块")
        
        self.is_initialized = True
        logger.info("RAG 系统初始化完成！")
        return True
    
    def query(self, question: str) -> Dict[str, Any]:
        """查询"""
        logger.info(f"收到查询: {question}")
        
        if not self.is_initialized:
            return {
                'success': False,
                'answer': '系统未初始化！',
                'sources': [],
                'documents': []
            }
        
        docs = self.retriever.retrieve(question)
        
        if not docs:
            docs = self.retriever.documents[:2]
            context = '\n\n'.join([
                f"【{d.metadata.get('file_name', d.source)}】\n{d.content[:300]}..."
                for d in docs
            ])
            answer = f"没有找到完全匹配的内容，但找到了一些相关文档：\n\n{context}"
            sources = list(set([d.metadata.get('file_name', d.source) for d in docs]))
        else:
            context = '\n\n'.join([
                f"【{d.metadata.get('file_name', d.source)}】\n{d.content[:300]}..."
                for d in docs
            ])
            answer = f"根据知识库中的信息，为您找到以下相关内容：\n\n{context}"
            sources = list(set([d.metadata.get('file_name', d.source) for d in docs]))
        
        logger.info(f"查询完成: 找到 {len(docs)} 个相关文档")
        return {
            'success': True,
            'answer': answer,
            'sources': sources,
            'documents': docs
        }


def main():
    print("="*80)
    print("📚 本地知识库问答系统（专业版 - 支持多格式）")
    print("="*80)
    
    rag = RAGSystemPro()
    
    print("\n正在初始化系统...")
    if not rag.initialize():
        print("\n❌ 初始化失败！请检查 knowledge_base 文件夹。")
        return
    
    print("\n✅ 初始化成功！")
    print(f"\n支持的格式: {', '.join(rag.loader.get_supported_formats())}")
    
    print("\n" + "="*80)
    print("开始对话（输入 'quit' 退出）")
    print("="*80)
    
    while True:
        try:
            question = input("\n💬 请输入问题: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            result = rag.query(question)
            
            if result['success']:
                print("\n" + "="*80)
                print("🤖 回答:")
                print("="*80)
                print(result['answer'])
                
                if result['sources']:
                    print(f"\n📄 参考来源: {', '.join(result['sources'])}")
            else:
                print(f"\n❌ {result['answer']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            logger.error(f"发生错误: {e}")
            print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
