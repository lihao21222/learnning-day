import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    DirectoryLoader
)


class DocumentLoader:
    def __init__(self, knowledge_base_dir: str = "knowledge_base"):
        self.knowledge_base_dir = knowledge_base_dir

    def load_text_file(self, file_path: str) -> List[Document]:
        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()

    def load_pdf_file(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()

    def load_docx_file(self, file_path: str) -> List[Document]:
        loader = Docx2txtLoader(file_path)
        return loader.load()

    def load_single_file(self, file_path: str) -> List[Document]:
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == ".txt":
            return self.load_text_file(file_path)
        elif ext == ".pdf":
            return self.load_pdf_file(file_path)
        elif ext == ".docx":
            return self.load_docx_file(file_path)
        else:
            print(f"不支持的文件格式: {ext}")
            return []

    def load_directory(self) -> List[Document]:
        all_documents = []
        
        if not os.path.exists(self.knowledge_base_dir):
            print(f"目录不存在: {self.knowledge_base_dir}")
            return all_documents
        
        for filename in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, filename)
            if os.path.isfile(file_path):
                print(f"正在加载: {filename}")
                docs = self.load_single_file(file_path)
                all_documents.extend(docs)
        
        print(f"总共加载了 {len(all_documents)} 个文档片段")
        return all_documents

    def load_with_pattern(self, glob_pattern: str = "**/*") -> List[Document]:
        loader = DirectoryLoader(
            self.knowledge_base_dir,
            glob=glob_pattern,
            use_multithreading=True,
            show_progress=True
        )
        return loader.load()
