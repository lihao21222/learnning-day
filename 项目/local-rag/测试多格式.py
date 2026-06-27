from document_loader_pro import DocumentLoaderPro


def test_loader():
    print("="*80)
    print("测试文档加载器（多种格式）")
    print("="*80)
    
    loader = DocumentLoaderPro()
    print(f"\n支持的格式: {loader.get_supported_formats()}")
    
    print("\n正在加载目录...")
    docs = loader.load_directory()
    
    if not docs:
        print("\n没有加载到任何文档！")
        return
    
    print("\n" + "="*80)
    print("加载结果统计")
    print("="*80)
    
    format_count = {}
    for doc in docs:
        fmt = doc.file_type
        format_count[fmt] = format_count.get(fmt, 0) + 1
    
    for fmt, cnt in format_count.items():
        print(f"  {fmt}: {cnt} 个文档")
    
    print(f"\n总计: {len(docs)} 个文档")
    
    print("\n" + "="*80)
    print("文档内容预览（前3个）")
    print("="*80)
    
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- 文档 {i+1} ({doc.file_type}) ---")
        print(f"来源: {doc.source}")
        print(f"元数据: {doc.metadata}")
        if len(doc.content) > 200:
            print(f"内容: {doc.content[:200]}...")
        else:
            print(f"内容: {doc.content}")
    
    print("\n" + "="*80)
    print("测试完成！")
    print("="*80)


if __name__ == "__main__":
    test_loader()
