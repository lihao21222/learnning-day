from simple_rag import SimpleRAG


def run_demo():
    print("="*70)
    print("本地知识库问答系统 - 演示")
    print("="*70)
    
    # 初始化系统
    rag = SimpleRAG()
    
    if not rag.initialize():
        print("初始化失败！")
        return
    
    # 示例问题
    questions = [
        "物流包装的主要功能是什么？",
        "绿色包装的原则有哪些？",
        "物流包装标准化有什么好处？"
    ]
    
    print("\n" + "="*70)
    print("开始演示问答...")
    print("="*70)
    
    for i, question in enumerate(questions, 1):
        print(f"\n【问题 {i}】{question}")
        print("-"*70)
        
        result = rag.query(question)
        
        print("【回答】")
        print(result['answer'])
        print("-"*70)
        
        if result['sources']:
            print(f"【参考来源】{', '.join(result['sources'])}")
    
    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)
    print("\n提示：")
    print("1. 要添加自己的文档，请将 .txt 文件放入 knowledge_base 文件夹")
    print("2. 要交互式运行，请执行: python simple_rag.py")
    print("="*70)


if __name__ == "__main__":
    run_demo()
