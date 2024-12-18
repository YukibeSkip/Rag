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
### 📚Importación de librerías
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

###  🔎Establecer el USER_AGENT
Se establece una variable de entorno `USER_AGENT` para simular un navegador específico al hacer solicitudes HTTP. Esto puede ayudar a evitar bloqueos por parte del servidor.
>>os.environ["USER_AGENT"] = "mi_usuario"

### 📖Obtener el contenido de la página web
-Se realiza una solicitud `GET` a la URL proporcionada, descargando el contenido HTML de la página.

-Luego, se utiliza BeautifulSoup para analizar y extraer todo el texto de la página.

### 📖✏Dividir el texto en fragmentos (chunks)
El texto extraído de la página se divide en fragmentos más pequeños para facilitar su procesamiento, utilizando el `RecursiveCharacterTextSplitter`. Cada fragmento tiene un tamaño de hasta 1200 caracteres y se superpone un 10% (100 caracteres) entre ellos.

### 📚🤗Crear embeddings usando HuggingFaceEmbeddings
Se utiliza el modelo `sentence-transformers/all-MiniLM-L6-v2` de Hugging Face para crear representaciones vectoriales (embeddings) de los fragmentos de texto. Estas representaciones permiten buscar y comparar fragmentos de texto de manera eficiente.

### ✏📓Crear documentos con los fragmentos
Cada fragmento de texto se convierte en un documento de la clase `Document de Langchain`. Esta clase es utilizada para almacenar el contenido de texto y las representaciones de los embeddings.

### 🎞Crear un vectorstore con Chroma
Utilizando el vectorstore `Chroma`, se almacenan los documentos y sus embeddings. Esto permite realizar búsquedas eficientes basadas en similitud de vectores.

### 🦙🔥 Definir el modelo LLM de Ollama
Se configura un modelo de lenguaje de Ollama, denominado `llama3.2`. Este modelo se utilizará para generar respuestas a las preguntas formuladas sobre el contenido del artículo.

### 📚Crear un template de prompt para QA
Se define una plantilla de prompt para la consulta, en la que se proporciona el contexto (el texto relevante) y la pregunta a responder.

### 🕵️‍♀️Crear el `retriever` para la búsqueda en el vectorstore
El `retriever` se utiliza para buscar documentos en el vectorstore. En este caso, se busca el documento más relevante a partir de la similitud de los embeddings. Se configuran los parámetros de búsqueda para recuperar los 3 fragmentos más relevantes `(k=3)`.

### ☝🤓Realizar la consulta y obtener la respuesta
Se realiza una consulta sobre el contenido del artículo, en este caso preguntando por los períodos de sobreventa y sobrecompra (usando una pregunta específica). El retriever obtiene los fragmentos más relevantes y genera una respuesta.


## 🤖🎲 Rag en español:
###  📚Importación de librerías
`requests`: Aunque no se utiliza en este código, es una librería que permite hacer solicitudes HTTP.

`PyPDF2`: Utilizada para leer y extraer texto de archivos PDF.

`langchain_huggingface`: Para utilizar embeddings de Hugging Face y convertir texto en vectores.

`langchain.text_splitter`: Para dividir el texto en fragmentos más pequeños y manejables.

`langchain_ollama.llms`: Para utilizar un modelo de lenguaje de Ollama (en este caso, "llama3.2").

`langchain_chroma`: Para almacenar y recuperar vectores de texto eficientemente.

`langchain.schema`: Para crear documentos de texto que se procesan en Langchain.

`langchain.prompts`: Para generar plantillas de preguntas y respuestas.

`langchain.chains`: Para construir una cadena de consulta y respuesta (RetrievalQA).

`os`: Para manejar configuraciones del sistema operativo, como directorios.

### 📓🎲Leer y extraer texto del archivo PDF
El código abre un archivo PDF ubicado en la ruta `pdf_path` y extrae el texto de cada una de sus páginas utilizando `PyPDF2`. El texto extraído se guarda en una variable `text`.

### 📖✏Dividir el texto en fragmentos (chunks)
El texto extraído del PDF se divide en fragmentos más pequeños utilizando `RecursiveCharacterTextSplitter`. Cada fragmento tiene un tamaño máximo de 500 caracteres y se superpone un 10% (50 caracteres) con el fragmento anterior.

### ⚙🔥🦙 Configurar el modelo de lenguaje de Ollama
Se crea una instancia del modelo de lenguaje `llama3.2` de Ollama, que se utilizará para generar respuestas basadas en el contexto de los fragmentos de texto.

### 📚🤗 Cargar el modelo de embeddings de HuggingFace
Se carga el modelo de embeddings `sentence-transformers/all-MiniLM-L6-v2` de Hugging Face para convertir el texto de cada fragmento en una representación vectorial (embedding). Los embeddings son representaciones numéricas del texto que permiten realizar búsquedas eficientes.

### 🎞Inicializar el vectorstore con Chroma
Se crea un vectorstore (almacen de vectores) utilizando la librería `Chroma`. Este almacén guarda las representaciones vectoriales de los fragmentos de texto, lo que facilita la búsqueda y recuperación eficiente basada en similitud de vectores

### 📚Crear documentos de Langchain a partir de los fragmentos
Los fragmentos de texto se convierten en documentos de la clase `Document` de Langchain. Esta clase es utilizada para almacenar tanto el contenido de texto como sus representaciones de embeddings.

### 🤜📚 Agregar los documentos al vectorstore
Se agregan los documentos (y sus embeddings) al vectorstore `Chroma`, lo que permite que luego se realicen búsquedas en estos documentos utilizando similitudes de embeddings.

### ☝🤓 Crear una plantilla de prompt para preguntas y respuestas
Se crea una plantilla de prompt para la consulta utilizando la clase `PromptTemplate`. La plantilla tiene un marcador de posición para el contexto (el fragmento de texto relevante) y otro para la pregunta del usuario.

### 🕵️‍♀️Crear un retriever para buscar en el vectorstore
Se crea un `retriever` a partir del vectorstore `Chroma`. El `retriever` es responsable de realizar búsquedas basadas en la similitud de los embeddings, y en este caso, se configura para buscar los 3 fragmentos más relevantes para cada consulta.

### ☝🤓🧝‍♀️Realizar la consulta y obtener la respuesta
Se define una pregunta de ejemplo `("¿Cuánto viven los elfos?")` y se pasa al retriever para buscar los fragmentos más relevantes. Después, se obtiene la respuesta usando el modelo LLM y se imprime el resultado.

