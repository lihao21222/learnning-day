from advanced_rag import RAGSystem
import time


def run_demo():
    print("="*80)
    print("[知识库] 本地知识库问答系统（进阶版）- 演示")
    print("="*80)
    
    # 初始化系统
    rag = RAGSystem()
    
    print("\n[等待] 正在初始化系统...")
    if not rag.initialize():
        print("\n[错误] 初始化失败！")
        return
    
    print("\n[成功] 系统初始化完成！")
    
    # 示例问题
    questions = [
        "物流包装的主要功能是什么？",
        "绿色包装的原则有哪些？",
        "物流包装标准化有什么好处？",
    ]
    
    print("\n" + "="*80)
    print("[演示] 开始演示问答")
    print("="*80)
    
    for i, question in enumerate(questions, 1):
        print(f"\n\n{'─'*80}")
        print(f"[问题 {i}]: {question}")
        print(f"{'─'*80}")
        
        time.sleep(0.5)  # 稍微延迟，让演示更自然
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
    print("[完成] 演示完成！")
    print("="*80)
    print("\n[提示] 下一步:")
    print("  1. 运行 'python advanced_rag.py' 进行交互式问答")
    print("  2. 在 knowledge_base 文件夹中添加您自己的文档")
    print("  3. 查看 面试展示指南.md 了解如何在面试中展示")
    print("="*80)


if __name__ == "__main__":
    run_demo()
