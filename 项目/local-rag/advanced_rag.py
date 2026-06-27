import os
import re
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from logger import logger
from config import config


@dataclass
class Document:
    """文档数据类"""
    content: str
    source: str
    metadata: Dict[str, Any] = None
    chunk_id: int = 0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TextSplitter:
    """文本分割器"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        logger.info(f"初始化文本分割器: chunk_size={self.chunk_size}, chunk_overlap={self.chunk_overlap}")
    
    def split_text(self, text: str, source: str) -> List[Document]:
        """
        将文本分割成多个文档块
        
        Args:
            text: 原始文本
            source: 文档来源
            
        Returns:
            Document 列表
        """
        if not text or not text.strip():
            logger.warning(f"空文本: {source}")
            return []
        
        chunks = []
        # 简单的文本分割：按固定大小分割，不要修改原文内容
        start = 0
        text_length = len(text)
        chunk_id = 0
        
        while start < text_length:
            # 计算当前块的结束位置
            end = min(start + self.chunk_size, text_length)
            
            # 保存这个块
            chunk_content = text[start:end]
            chunks.append(Document(
                content=chunk_content,
                source=source,
                chunk_id=chunk_id,
                metadata={'created_at': datetime.now().isoformat()}
            ))
            chunk_id += 1
            
            # 移动到下一个块，考虑重叠
            start += self.chunk_size - self.chunk_overlap
        
        logger.debug(f"文本分割完成: {len(chunks)} 个片段")
        return chunks


class SimpleRetriever:
    """简易检索器（基于关键词匹配）"""
    
    def __init__(self):
        self.documents: List[Document] = []
        logger.info("初始化简易检索器")
    
    def add_documents(self, documents: List[Document]):
        """添加文档到检索器"""
        if not documents:
            return
        
        self.documents.extend(documents)
        logger.info(f"添加了 {len(documents)} 个文档到检索器，总计: {len(self.documents)}")
    
    def retrieve(self, query: str, top_k: int = None) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回的文档数量
            
        Returns:
            相关文档列表
        """
        if not self.documents:
            logger.warning("检索器中没有文档")
            return []
        
        top_k = top_k or config.TOP_K
        query_lower = query.lower()
        
        # 提取查询关键词
        query_words = re.findall(r'[\w\u4e00-\u9fff]+', query_lower)
        
        scored_docs = []
        for doc in self.documents:
            content_lower = doc.content.lower()
            score = 0
            
            # 完整查询匹配
            if query_lower in content_lower:
                score += 100
            
            # 关键词匹配
            matched_count = 0
            for word in query_words:
                if word and len(word) >= 2:
                    if word in content_lower:
                        score += 20
                        matched_count += 1
            
            # 标题匹配（如果包含）
            if '标题' in content_lower or 'title' in content_lower:
                score += 5
            
            if score > 0:
                scored_docs.append((-score, -matched_count, doc))
        
        # 排序
        scored_docs.sort()
        results = [doc for (neg_score, neg_count, doc) in scored_docs[:top_k]]
        
        # 如果没有找到匹配，返回前 K 个文档
        if not results and self.documents:
            results = self.documents[:top_k]
        
        logger.info(f"检索完成: 找到 {len(results)} 个相关文档")
        return results


class DocumentLoader:
    """文档加载器"""
    
    def __init__(self, knowledge_base_dir: str = None):
        self.knowledge_base_dir = knowledge_base_dir or config.KNOWLEDGE_BASE_DIR
        logger.info(f"初始化文档加载器: {self.knowledge_base_dir}")
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """加载文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            splitter = TextSplitter()
            return splitter.split_text(content, file_path)
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {e}")
            return []
    
    def load_directory(self) -> List[Document]:
        """加载整个知识库目录"""
        all_docs = []
        
        if not os.path.exists(self.knowledge_base_dir):
            logger.error(f"目录不存在: {self.knowledge_base_dir}")
            return all_docs
        
        for filename in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, filename)
            
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())
                
                if ext == '.txt':
                    logger.info(f"加载文件: {filename}")
                    docs = self.load_text_file(file_path)
                    all_docs.extend(docs)
                else:
                    logger.debug(f"跳过不支持的文件: {filename}")
        
        logger.info(f"目录加载完成: 总计 {len(all_docs)} 个文档片段")
        return all_docs


class RAGSystem:
    """完整的 RAG 系统"""
    
    def __init__(self):
        self.loader = DocumentLoader()
        self.retriever = SimpleRetriever()
        self.is_initialized = False
        logger.info("初始化 RAG 系统")
    
    def initialize(self) -> bool:
        """初始化系统"""
        logger.info("开始初始化 RAG 系统...")
        
        # 加载文档
        docs = self.loader.load_directory()
        if not docs:
            logger.error("没有加载到任何文档")
            return False
        
        # 建立索引
        self.retriever.add_documents(docs)
        self.is_initialized = True
        
        logger.info("RAG 系统初始化完成！")
        return True
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        查询系统
        
        Args:
            question: 用户问题
            
        Returns:
            查询结果
        """
        logger.info(f"收到查询: {question}")
        
        if not self.is_initialized:
            return {
                'success': False,
                'question': question,
                'answer': '系统未初始化，请先调用 initialize()',
                'sources': [],
                'documents': []
            }
        
        # 检索相关文档
        docs = self.retriever.retrieve(question)
        
        if not docs:
            return {
                'success': True,
                'question': question,
                'answer': '抱歉，没有找到相关内容。您可以尝试调整问题或添加更多文档。',
                'sources': [],
                'documents': []
            }
        
        # 构建回答
        context = "\n\n".join([
            f"【文档 {i+1}】\n{doc.content}" 
            for i, doc in enumerate(docs)
        ])
        
        answer = f"根据知识库中的信息，为您找到以下相关内容：\n\n{context}"
        
        sources = list(set([doc.source for doc in docs]))
        
        result = {
            'success': True,
            'question': question,
            'answer': answer,
            'sources': sources,
            'documents': docs
        }
        
        logger.info(f"查询完成: 找到 {len(docs)} 个相关文档")
        return result


def main():
    """主函数"""
    print("="*80)
    print("📚 本地知识库问答系统（进阶版）")
    print("="*80)
    
    rag = RAGSystem()
    
    if not rag.initialize():
        print("\n❌ 初始化失败！请检查 knowledge_base 文件夹中是否有文档。")
        return
    
    print("\n" + "="*80)
    print("✅ 系统已就绪！")
    print("="*80)
    print("\n📝 使用说明：")
    print("  - 输入问题进行查询")
    print("  - 输入 'quit' 或 'exit' 退出")
    print("  - 输入 'help' 查看帮助")
    
    while True:
        try:
            question = input("\n💬 请输入您的问题: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            if question.lower() in ['help', 'h']:
                print("\n📖 帮助信息：")
                print("  - 直接输入问题进行查询")
                print("  - quit/exit/q: 退出程序")
                print("  - help/h: 显示帮助信息")
                continue
            
            result = rag.query(question)
            
            if result['success']:
                print("\n" + "="*80)
                print("🤖 回答：")
                print("="*80)
                print(result['answer'])
                print("="*80)
                
                if result['sources']:
                    print(f"\n📄 参考来源：")
                    for source in result['sources']:
                        print(f"  - {os.path.basename(source)}")
            else:
                print(f"\n❌ 错误：{result['answer']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            logger.error(f"发生错误: {e}")
            print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
