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

## 🤖🖥️ RagInterfaz:

###  📚Importación de librerías
`requests`: Para hacer solicitudes HTTP a la página de Wikipedia.

`beautifulsoup4`: Para parsear el contenido HTML de la página de Wikipedia.

`langchain_huggingface`: Para generar embeddings a partir de modelos de HuggingFace.

`langchain`: Para procesamiento de texto, creación de vectores y manipulación de LLMs.

`langchain_ollama`: Para usar el modelo LLM de Ollama.

`gradio`: Para crear la interfaz gráfica de usuario.

`chroma`: Para almacenamiento y recuperación eficiente de vectores de texto.

Instalar con pip: pip install requests beautifulsoup4 langchain gradio langchain_huggingface langchain_ollama chromadb

### 💀📃 Extracción de contenido de Wikipedia
El código comienza con la solicitud HTTP para obtener el contenido de una página de Wikipedia específica (en este caso, sobre "Hades"). La página se parsea usando BeautifulSoup para extraer el texto del artículo.

### 📖✏ División del texto en fragmentos
El texto de la página se divide en fragmentos más pequeños (chunks) para que sea procesado eficientemente. Esto se hace utilizando `RecursiveCharacterTextSplitter` de LangChain, que permite dividir el texto de acuerdo a un tamaño de fragmento especificado.

### 👨‍💻⛲ Generación de embeddings
Usamos el modelo de embeddings de HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`) para generar representaciones vectoriales de los fragmentos de texto. Estos embeddings facilitan la búsqueda y recuperación de información relevante cuando se hace una pregunta.

### 📃📃 Creación de un VectorStore
Se utiliza Chroma, una biblioteca para almacenamiento de vectores, para guardar los documentos procesados y sus embeddings. Esto permite realizar búsquedas eficientes para obtener la información relevante cuando el usuario hace una pregunta.

### ⚙🔥🦙 Configurar el modelo de lenguaje de Ollama
El modelo LLM de Ollama se configura para generar respuestas a las preguntas del usuario utilizando el contenido recuperado.

### 🤖💀 Definición del prompt y creación de la cadena de Q&A
Usamos `ChatPromptTemplate` para definir un prompt que guíe al modelo en la generación de respuestas basadas en el contexto del artículo. Luego, creamos una cadena de Q&A utilizando `RetrievalQA` de LangChain

### 🖥️🐓 Interfaz de usuario con Gradio
Finalmente, creamos una interfaz de usuario utilizando Gradio, donde los usuarios pueden ingresar preguntas y recibir respuestas generadas por el modelo LLM.

### ⚙️💀 Ejecución
Para ejecutar el proyecto, simplemente corre el script de Python. Se abrirá una interfaz web de Gradio donde podrás hacer preguntas sobre el artículo de Wikipedia.

### 👁️‼️ Tener en cuenta:
El servidor de Ollama debe estar en ejecución en `localhost:11434`. Asegúrate de que el servidor esté configurado y en funcionamiento antes de ejecutar el código.

Es necesario contar con acceso a internet para descargar el contenido de Wikipedia y los modelos de HuggingFace.

## 🍃🤖 RagMongo:

###  📚Importación de librerías
`pymongo`: Para conectarse y trabajar con MongoDB Atlas.

`langchain_huggingface`: Para generar embeddings de texto utilizando modelos de HuggingFace.

`mongo-atlas-vector-search`: Para habilitar las capacidades de búsqueda vectorial en MongoDB Atlas.

Instalar con pip: pip install pymongo langchain_huggingface mongo-atlas-vector-search

### 🍃🔌 Conexión a MongoDB Atlas
El código establece una conexión a una base de datos MongoDB Atlas utilizando la URL de conexión proporcionada. Se utiliza el cliente de `MongoClient` de pymongo para conectarse a MongoDB.
 
### ⚙️🍃 Configuración de la base de datos y colección
Se establece la base de datos y la colección de MongoDB donde se almacenarán los documentos y sus embeddings. Los valores de `DB_NAME` y `COLLECTION_NAME` pueden ser personalizados.

### 🤗⛲ Inicialización de los embeddings de HuggingFace
Se inicializa un modelo de embeddings de HuggingFace usando `sentence-transformers/all-MiniLM-L6-v2`. Este modelo transforma el texto en representaciones vectoriales que permiten la búsqueda semántica en la base de datos.

### ⚙️📚Configuración de la búsqueda vectorial en MongoDB Atlas
El código configura MongoDB Atlas para realizar búsquedas vectoriales utilizando el índice de búsqueda en el vector. Se especifica que se utilizará la función de similitud coseno para medir la relevancia entre los vectores.

### 🔎🕵️ Uso del sistema de búsqueda
Una vez configurado, puedes cargar documentos en la colección y usar la búsqueda vectorial para encontrar documentos relevantes basados en la similitud de texto. La base de datos almacenará tanto los documentos originales como sus representaciones vectoriales para optimizar las búsquedas.

**El resto del codigo es igual que el documento de Rag y RAGespañol**

