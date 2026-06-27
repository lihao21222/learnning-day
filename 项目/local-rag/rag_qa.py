from typing import List, Optional
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM


class RAGQuestionAnswerer:
    def __init__(self, retriever):
        self.retriever = retriever
        self.qa_chain = None
        self._initialize_chain()

    def _initialize_chain(self):
        prompt_template = """请根据以下上下文回答问题。如果答案不在上下文中，请说"根据提供的资料，我无法回答这个问题"。

上下文:
{context}

问题: {question}

回答:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=512,
                temperature=0.1,
                top_p=0.95,
                repetition_penalty=1.15,
                device_map="auto"
            )
            
            llm = HuggingFacePipeline(pipeline=pipe)
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            print("RAG问答链初始化成功")
        except Exception as e:
            print(f"初始化模型时出错: {e}")
            print("使用简易模式...")
            self.qa_chain = None

    def answer(self, question: str) -> dict:
        if self.qa_chain:
            result = self.qa_chain({"query": question})
            return {
                "question": question,
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        else:
            return self._simple_answer(question)

    def _simple_answer(self, question: str) -> dict:
        docs = self.retriever.get_relevant_documents(question)
        context = "\n".join([doc.page_content for doc in docs])
        
        answer = f"根据检索到的信息：\n\n{context}\n\n（请安装完整版模型以获得更好的回答体验）"
        
        return {
            "question": question,
            "answer": answer,
            "source_documents": docs
        }

    def display_result(self, result: dict):
        print("\n" + "="*50)
        print(f"问题: {result['question']}")
        print("="*50)
        print(f"回答:\n{result['answer']}")
        print("\n" + "-"*50)
        print("参考来源:")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"\n[{i}] {doc.metadata.get('source', '未知来源')}")
            print(f"内容: {doc.page_content[:100]}...")
        print("="*50 + "\n")
