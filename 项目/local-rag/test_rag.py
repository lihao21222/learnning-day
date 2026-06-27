from document_loader import DocumentLoader
from vector_store import VectorStoreManager


def test_system():
    print("="*50)
    print("测试本地知识库问答系统")
    print("="*50)
    
    loader = DocumentLoader()
    vector_manager = VectorStoreManager()
    
    print("\n1. 加载文档...")
    documents = loader.load_directory()
    
    if not documents:
        print("没有找到文档")
        return
    
    print(f"\n成功加载 {len(documents)} 个文档")
    
    print("\n2. 创建向量数据库...")
    vectorstore = vector_manager.create_vectorstore(documents)
    
    print("\n3. 测试检索功能...")
    test_queries = [
        "物流包装的主要功能是什么？",
        "绿色包装的原则有哪些？",
        "物流包装标准化有什么好处？"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        docs = vector_manager.similarity_search(query, k=2)
        print("检索到的相关内容:")
        for i, doc in enumerate(docs, 1):
            print(f"  [{i}] {doc.page_content[:80]}...")
    
    print("\n" + "="*50)
    print("测试完成！向量数据库已保存到 vector_db 文件夹")
    print("现在可以运行 python main.py 进行完整问答")
    print("="*50)


if __name__ == "__main__":
    test_system()
