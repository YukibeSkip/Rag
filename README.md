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
## ☝ Antes de empezar
Antes hay que levantar Ollama en docker:
-docker network create ollama_network

-docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama --net=ollama_network ollama/ollama

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

###  Dividir el texto en fragmentos (chunks)
El texto extraído de la página se divide en fragmentos más pequeños para facilitar su procesamiento, utilizando el `RecursiveCharacterTextSplitter`. Cada fragmento tiene un tamaño de hasta 1200 caracteres y se superpone un 10% (100 caracteres) entre ellos.


### Crear embeddings usando HuggingFaceEmbeddings
Se utiliza el modelo `sentence-transformers/all-MiniLM-L6-v2` de Hugging Face para crear representaciones vectoriales (embeddings) de los fragmentos de texto. Estas representaciones permiten buscar y comparar fragmentos de texto de manera eficiente.

### Crear documentos con los fragmentos
Cada fragmento de texto se convierte en un documento de la clase `Document de Langchain`. Esta clase es utilizada para almacenar el contenido de texto y las representaciones de los embeddings.

### Crear un vectorstore con Chroma
Utilizando el vectorstore `Chroma`, se almacenan los documentos y sus embeddings. Esto permite realizar búsquedas eficientes basadas en similitud de vectores.

###  Definir el modelo LLM de Ollama
Se configura un modelo de lenguaje de Ollama, denominado `llama3.2`. Este modelo se utilizará para generar respuestas a las preguntas formuladas sobre el contenido del artículo.

### Crear un template de prompt para QA
Se define una plantilla de prompt para la consulta, en la que se proporciona el contexto (el texto relevante) y la pregunta a responder.

### Crear el `retriever` para la búsqueda en el vectorstore
El `retriever` se utiliza para buscar documentos en el vectorstore. En este caso, se busca el documento más relevante a partir de la similitud de los embeddings. Se configuran los parámetros de búsqueda para recuperar los 3 fragmentos más relevantes `(k=3)`.

### Realizar la consulta y obtener la respuesta
Se realiza una consulta sobre el contenido del artículo, en este caso preguntando por los períodos de sobreventa y sobrecompra (usando una pregunta específica). El retriever obtiene los fragmentos más relevantes y genera una respuesta.







