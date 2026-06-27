import os
from document_loader import DocumentLoader
from vector_store import VectorStoreManager
from rag_qa import RAGQuestionAnswerer


def main():
    print("="*50)
    print("本地知识库问答系统")
    print("="*50)
    
    loader = DocumentLoader()
    vector_manager = VectorStoreManager()
    
    vectorstore = vector_manager.load_vectorstore()
    
    if not vectorstore:
        print("\n正在加载知识库文档...")
        documents = loader.load_directory()
        
        if not documents:
            print("没有找到文档，请将文档放入 knowledge_base 文件夹")
            return
        
        print("\n正在创建向量数据库...")
        vectorstore = vector_manager.create_vectorstore(documents)
    
    print("\n正在初始化问答系统...")
    retriever = vector_manager.get_retriever(k=3)
    qa_system = RAGQuestionAnswerer(retriever)
    
    print("\n" + "="*50)
    print("系统已就绪！输入 'quit' 退出")
    print("="*50 + "\n")
    
    while True:
        question = input("请输入您的问题: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("再见！")
            break
        
        if not question:
            continue
        
        result = qa_system.answer(question)
        qa_system.display_result(result)


if __name__ == "__main__":
    main()
