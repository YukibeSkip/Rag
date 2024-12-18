# 🤖Sistema RAG🤖
## 🔌 De que va el proyecto ?
El proyecto desarrolla diferentes sistemas rags:
-Uno que se comunica con una pagina web
-Y otro que se comunica con un pdf en español

### 🩸💾 Requisitos:
-install build-essential

-install langchain langchain_ollama

-install chromadb sentence-transformers langchain_huggingface langchain_chroma

-install gradio

-install bs4

# 📢Descripción de los scripts:

## 📃🤖 RAG:
### Importación de librerías
`requests`: Para obtener el contenido HTML de una página web.

`BeautifulSoup`: Para analizar y extraer texto de la página HTML.

`langchain_huggingface`: Para usar embeddings de Hugging Face para convertir el texto en vectores.

`langchain.text_splitter`: Para dividir el texto en fragmentos más pequeños (chunks) adecuados para el procesamiento.

`langchain_community.embeddings`: Para usar embeddings alternativos (en este caso, OllamaEmbeddings).

`langchain_chroma`: Para almacenar y buscar vectores de texto.

`langchain_ollama`.llms: Para usar un modelo de lenguaje de Ollama (en este caso, "llama3.2").

`langchain.schema`: Para definir documentos de texto.

`langchain.prompts`: Para crear plantillas de preguntas y respuestas (QA).

`langchain.chains`: Para construir la cadena de consulta y respuesta (RetrievalQA).

`os`: Para configurar variables de entorno, en este caso, para el agente de usuario (USER_AGENT).

###  Establecer el USER_AGENT
Se establece una variable de entorno `USER_AGENT` para simular un navegador específico al hacer solicitudes HTTP. Esto puede ayudar a evitar bloqueos por parte del servidor.
>>os.environ["USER_AGENT"] = "mi_usuario"

### Obtener el contenido de la página web
-Se realiza una solicitud `GET` a la URL proporcionada, descargando el contenido HTML de la página.

-Luego, se utiliza BeautifulSoup para analizar y extraer todo el texto de la página.






