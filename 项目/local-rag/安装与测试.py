import sys


def check_dependencies():
    print("="*80)
    print("检查依赖库")
    print("="*80)
    
    status = {}
    
    # 检查基础依赖
    try:
        import os
        import dataclasses
        import typing
        print("[OK] 基础依赖: OK")
        status['basic'] = True
    except Exception as e:
        print(f"[ER] 基础依赖: {e}")
        status['basic'] = False
    
    # 检查 pypdf
    try:
        import pypdf
        print("[OK] pypdf (PDF支持): OK")
        status['pypdf'] = True
    except ImportError:
        print("[WARN]  pypdf (PDF支持): 未安装")
        print("       安装命令: pip install pypdf")
        status['pypdf'] = False
    
    # 检查 python-docx
    try:
        import docx
        print("[OK] python-docx (Word支持): OK")
        status['docx'] = True
    except ImportError:
        print("[WARN]  python-docx (Word支持): 未安装")
        print("       安装命令: pip install python-docx")
        status['docx'] = False
    
    # 检查 streamlit
    try:
        import streamlit
        print("[OK] streamlit (Web界面): OK")
        status['streamlit'] = True
    except ImportError:
        print("[WARN]  streamlit (Web界面): 未安装")
        print("       安装命令: pip install streamlit")
        status['streamlit'] = False
    
    print("\n" + "="*80)
    print("依赖检查完成！")
    print("="*80)
    
    return status


def print_install_guide():
    print("\n" + "="*80)
    print("安装指南")
    print("="*80)
    
    print("\n最小安装（仅 TXT）：")
    print("  无需额外安装")
    
    print("\n标准安装（TXT + PDF + Word）：")
    print("  pip install pypdf python-docx")
    
    print("\n完整安装（包含 Web 界面）：")
    print("  pip install streamlit pypdf python-docx")
    
    print("\n" + "="*80)


def main():
    status = check_dependencies()
    
    print_install_guide()
    
    # 询问是否安装
    need_install = False
    if not status['pypdf'] or not status['docx'] or not status['streamlit']:
        answer = input("\n是否自动安装缺失的依赖？(y/n): ").strip().lower()
        if answer == 'y':
            need_install = True
    
    if need_install:
        import subprocess
        packages = []
        if not status['pypdf']:
            packages.append('pypdf')
        if not status['docx']:
            packages.append('python-docx')
        if not status['streamlit']:
            packages.append('streamlit')
        
        if packages:
            print(f"\n正在安装: {' '.join(packages)}")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
                print("\n✅ 安装完成！")
            except Exception as e:
                print(f"\n❌ 安装失败: {e}")
    
    print("\n" + "="*80)
    print("快速开始：")
    print("="*80)
    print("  1. 运行专业版演示:")
    print("     python demo_pro.py")
    print("\n  2. 运行专业版交互式:")
    print("     python rag_pro.py")
    print("\n  3. 运行 Web 界面:")
    print("     streamlit run app_simple.py")
    print("="*80)


if __name__ == "__main__":
    main()
