from contextlib import asynccontextmanager
from fastapi import FastAPI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Load and split documents
    loader = TextLoader("knowledge_base.txt")
    splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(loader.load())

    # 2. Generate local embeddings (runs locally on your device)
    local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Save chunks to local vector store
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=local_embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. Initialize Local LLM via Ollama (Make sure you pulled the model first: `ollama pull llama3`)
    # llm = ChatOllama(model="llama3", 
    #                 temperature=0,
    #                 base_url="http://127.0.0.1:11434")

    # 5. Prompt and structure formulation
    # template = """Answer the query using only the provided context material:
    # Context: {context}
    # Query: {question}
    # Answer:"""
    # prompt = ChatPromptTemplate.from_template(template)

    # def format_docs(docs):
    #     return "\n\n".join(doc.page_content for doc in docs)

    # # 6. Chain execution
    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # 7. Query
    # print(rag_chain.invoke("What does the document state about system requirements?"))
    # print(rag_chain.invoke("Serial1 uses what? TX pin is GPI number?"))

    yield {"retriever": retriever}