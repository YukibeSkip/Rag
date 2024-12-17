import requests
from bs4 import BeautifulSoup
from langchain_huggingface import HuggingFaceEmbeddings  # Actualización para HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
import os

# Establecer USER_AGENT (como sugerido por el mensaje de advertencia)
os.environ["USER_AGENT"] = "mi_usuario"  # Cambia "mi_usuario" por un identificador adecuado

# URL del artículo
url = "https://pythonology.eu/using-pandas_ta-to-generate-technical-indicators-and-signals/"

# Obtener el contenido de la página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
datos = soup.get_text()

# Dividir el texto en fragmentos (chunks)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200, chunk_overlap=100, add_start_index=True
)

# Dividir el texto en fragmentos más pequeños
chunks = text_splitter.split_text(datos)
print(f"Number of chunks: {len(chunks)}")

# Crear embeddings del texto usando HuggingFaceEmbeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Crear una lista de documentos a partir de los fragmentos
documents = [Document(page_content=chunk) for chunk in chunks]

# Corregir la creación del vectorstore utilizando Chroma y embeddings
vectorstore = Chroma.from_documents(
    documents=documents,  # Documentos a agregar
    embedding=embedding_model  # Pasamos la instancia del modelo de embeddings
)
print("Documents added to the vector store.")

# Definir el modelo LLM de Ollama
llm = OllamaLLM(model="llama3.2", server_url="http://localhost:11434")

# Crear el prompt template para el QA
prompt = ChatPromptTemplate.from_template(
    template="Use the context below to answer the user's question:\n\n{context}\n\nQuestion: {question}\nAnswer:"
)

# Crear el retriever a partir del vectorstore
retriever = vectorstore.as_retriever()

# Crear la cadena de QA (RetrievalQA)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

# Realizar una consulta
question = "what are the oversold and overbought periods?"
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
response = retriever.invoke(question)
print("Response:", response)
