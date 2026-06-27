from rag_pro import RAGSystemPro
import time


def demo_pro():
    print("="*80)
    print("📚 本地知识库问答系统（专业版演示）")
    print("="*80)
    
    rag = RAGSystemPro()
    
    print("\n正在初始化系统...")
    if not rag.initialize():
        print("\n❌ 初始化失败！")
        return
    
    print("\n✅ 系统初始化完成！")
    print(f"\n支持的格式: {', '.join(rag.loader.get_supported_formats())}")
    
    questions = [
        "物流包装的主要功能是什么？",
        "Python 的特点是什么？",
    ]
    
    print("\n" + "="*80)
    print("开始演示问答")
    print("="*80)
    
    for i, question in enumerate(questions, 1):
        print(f"\n\n{'─'*80}")
        print(f"[问题 {i}]: {question}")
        print(f"{'─'*80}")
        
        time.sleep(0.5)
        result = rag.query(question)
        
        if result['success']:
            print("\n[回答]:")
            print(result['answer'])
            
            if result['sources']:
                print(f"\n[来源]:")
                for source in result['sources']:
                    print(f"   - {source}")
        else:
            print(f"\n[错误] {result['answer']}")
    
    print("\n\n" + "="*80)
    print("演示完成！")
    print("="*80)
    print("\n提示:")
    print("  - 运行 'python rag_pro.py' 进行交互式问答")
    print("  - 支持的格式: .txt, .pdf, .docx")
    print("="*80)


if __name__ == "__main__":
    demo_pro()
