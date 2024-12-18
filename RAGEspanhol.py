import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings  # Cargar el modelo de embeddings de HuggingFace
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Usar el splitter adecuado
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.prompts import PromptTemplate

# Cargar el PDF y extraer el texto
pdf_path = "/home/bigdata/Exercicios_Git/Rag/D&D5Manual.pdf"

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

# Usar RecursiveCharacterTextSplitter para dividir el texto de manera eficiente
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)  # Definir el tamaño del fragmento y la superposición
chunks = text_splitter.split_text(text)

print(f"Number of chunks: {len(chunks)}")

# Cargar el modelo LLM de Ollama
llm = OllamaLLM(model="llama3.2", server_url="http://localhost:11434")

# Cargar el modelo de embeddings de HuggingFace
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicializar el vectorstore (almacen de vectores) con Chroma
vectorstore = Chroma(persist_directory="./vectorstore", embedding_function=embedding_model)

# Crear documentos de Langchain con los fragmentos
documents = [Document(page_content=chunk) for chunk in chunks]

# Agregar documentos al vectorstore
vectorstore.add_documents(documents)
print("Documents added to the vector store.")

# Crear el prompt para la pregunta
prompt_template = """
Usa el contexto a continuación para responder la pregunta del usuario:

{context}

Pregunta: {question}

Respuesta:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Crear el retriever a partir del vectorstore
retriever = vectorstore.as_retriever()

# Hacer una pregunta de ejemplo
question = "¿Cuánto viven los elfos?"

# Obtener la respuesta usando el chain de QA
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
response = retriever.invoke(question)
# Imprimir la respuesta
print("Respuesta:", response)
