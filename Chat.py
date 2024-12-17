
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

vector_store = Chroma(
    collection_name="some_facts",
    embedding_function=embeddings,
    persist_directory="./chroma_some_facts"
)

retriever = vector_store.as_retriever()

question = "Can I steal a bank?"
docs = vector_store.similarity_search(question)
len(docs)
docs[0]

template = """"Answer the question based only on the following context: {context}
                Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

ollama_llm = "llama3.2"
model_local = ChatOllama(model=ollama_llm)

chain = ({"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model_local
        | StrOutputParser())

chain.invoke("Can I steal a bank?")
