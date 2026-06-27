from advanced_rag import RAGSystem

def test_new_documents():
    print("="*80)
    print("测试新添加的知识库文档")
    print("="*80)
    
    # 初始化系统
    rag = RAGSystem()
    print("\n正在初始化系统...")
    if not rag.initialize():
        print("\n初始化失败！")
        return
    
    print("\n初始化成功！")
    
    # 测试新文档的问题
    questions = [
        "Python 的特点是什么？",
        "机器学习有哪些类型？",
        "常见的算法有哪些？"
    ]
    
    print("\n" + "="*80)
    print("开始测试问答")
    print("="*80)
    
    for i, question in enumerate(questions, 1):
        print(f"\n\n{'─'*80}")
        print(f"[问题 {i}]: {question}")
        print(f"{'─'*80}")
        
        result = rag.query(question)
        
        if result['success']:
            print("\n[回答]:")
            print(result['answer'])
            
            if result['sources']:
                print(f"\n[来源]:")
                for source in result['sources']:
                    print(f"   - {source.split('/')[-1].split('\\\\')[-1]}")
        else:
            print(f"\n[错误] {result['answer']}")
    
    print("\n\n" + "="*80)
    print("测试完成！")
    print("="*80)

if __name__ == "__main__":
    test_new_documents()
