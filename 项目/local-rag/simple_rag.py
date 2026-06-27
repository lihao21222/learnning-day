import os
from typing import List, Dict
from dataclasses import dataclass
import re


@dataclass
class Document:
    content: str
    source: str
    metadata: Dict = None


class SimpleVectorStore:
    def __init__(self):
        self.documents: List[Document] = []
    
    def add_document(self, doc: Document):
        self.documents.append(doc)
    
    def search(self, query: str, top_k: int = 3) -> List[Document]:
        if not self.documents:
            return []
        
        query_lower = query.lower()
        scored_docs = []
        
        # 提取查询关键词
        query_words = re.findall(r'[\w\u4e00-\u9fff]+', query_lower)
        
        for doc in self.documents:
            content_lower = doc.content.lower()
            score = 0
            
            # 完整查询匹配
            if query_lower in content_lower:
                score += 50
            
            # 关键词匹配
            matched_count = 0
            for word in query_words:
                if word and len(word) >= 2:  # 至少2个字符
                    if word in content_lower:
                        score += 10
                        matched_count += 1
            
            # 部分关键词匹配
            if matched_count > 0:
                scored_docs.append((-score, -matched_count, doc))
        
        # 排序（先按分数，再按匹配数量）
        scored_docs.sort()
        results = [doc for (neg_score, neg_count, doc) in scored_docs[:top_k]]
        
        # 如果没有找到，返回所有文档
        if not results and self.documents:
            return self.documents[:top_k]
        
        return results


class DocumentLoader:
    def __init__(self, knowledge_base_dir: str = "knowledge_base"):
        self.knowledge_base_dir = knowledge_base_dir
    
    def load_text_file(self, file_path: str) -> List[Document]:
        docs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                chunks = self._split_text(content)
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        content=chunk,
                        source=file_path,
                        metadata={'chunk_id': i}
                    )
                    docs.append(doc)
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
        return docs
    
    def _split_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        chunks = []
        sentences = re.split(r'[。！？.!?\n]', text)
        
        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "。"
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "。"
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def load_directory(self) -> List[Document]:
        all_docs = []
        
        if not os.path.exists(self.knowledge_base_dir):
            print(f"目录不存在: {self.knowledge_base_dir}")
            return all_docs
        
        for filename in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, filename)
            
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                print(f"正在加载: {filename}")
                docs = self.load_text_file(file_path)
                all_docs.extend(docs)
        
        print(f"总共加载了 {len(all_docs)} 个文档片段")
        return all_docs


class SimpleRAG:
    def __init__(self):
        self.loader = DocumentLoader()
        self.vector_store = SimpleVectorStore()
        self.is_initialized = False
    
    def initialize(self):
        print("正在加载文档...")
        docs = self.loader.load_directory()
        
        if not docs:
            print("没有找到文档，请将 .txt 文件放入 knowledge_base 文件夹")
            return False
        
        print("正在建立索引...")
        for doc in docs:
            self.vector_store.add_document(doc)
        
        self.is_initialized = True
        print("初始化完成！")
        return True
    
    def query(self, question: str) -> Dict:
        if not self.is_initialized:
            return {
                'question': question,
                'answer': '系统未初始化，请先调用 initialize()',
                'sources': []
            }
        
        results = self.vector_store.search(question, top_k=2)
        
        if not results:
            return {
                'question': question,
                'answer': '抱歉，没有找到相关内容。',
                'sources': []
            }
        
        # 构建回答
        context = "\n\n".join([f"相关信息 {i+1}:\n{doc.content}" for i, doc in enumerate(results)])
        
        answer = f"根据知识库，为您找到以下相关信息：\n\n{context}"
        
        sources = list(set([doc.source for doc in results]))
        
        return {
            'question': question,
            'answer': answer,
            'sources': sources,
            'results': results
        }


def main():
    print("="*70)
    print("简易本地知识库问答系统")
    print("="*70)
    
    rag = SimpleRAG()
    
    if not rag.initialize():
        return
    
    print("\n" + "="*70)
    print("系统已就绪！输入问题进行查询，输入 'quit' 退出")
    print("="*70)
    
    while True:
        question = input("\n请输入您的问题: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("再见！")
            break
        
        if not question:
            continue
        
        result = rag.query(question)
        
        print("\n" + "="*70)
        print("回答:")
        print("="*70)
        print(result['answer'])
        print("="*70)
        if result['sources']:
            print(f"参考来源: {', '.join(result['sources'])}")


if __name__ == "__main__":
    main()
