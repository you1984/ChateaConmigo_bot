import openai
import telegram
import nltk
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import config

# Inicializa el bot de Telegram
updater = Updater("5887157767:AAE7lgtroWxMNAeXYWrppUvPjoF5JYck7dY", use_context=True)
dispatcher = updater.dispatcher

# Inicializa la conexión a GPT-3
openai.api_key = config.openai_api_key

# Obtiene el nombre de usuario del bot
bot_info = updater.bot.get_me()
bot_username = bot_info.username

def start(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat
  # Envía un mensaje de bienvenida y una descripción de lo que es capaz de hacer el bot al chat
  chat.send_message("Hola! Soy un bot de Telegram creado para ayudarte a encontrar información sobre eventos históricos, el tiempo y más. Estoy aquí para ayudarte a encontrar respuestas a tus preguntas y hacer tus días más fáciles. ¿En qué te puedo ayudar hoy?")

# Agrega un manejador de comandos para el comando "/start"
start_handler = CommandHandler("start", start)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(start_handler)

def ayuda(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat
  # Envía un mensaje de ayuda al chat
  chat.send_message("Soy un bot de Telegram creado para ayudarte a encontrar información sobre eventos históricos, el tiempo y más. Puedes enviarme preguntas sobre cualquiera de estos temas y trataré de ayudarte a encontrar una respuesta.")

# Agrega un manejador de comandos para el comando "/ayuda"
ayuda_handler = CommandHandler("ayuda", ayuda)
dispatcher.add_handler(ayuda_handler)

def saludo(update, context):
  # Obtiene el chat (grupo) en el que se envió el mensaje
  chat = update.message.chat
  # Envía un mensaje de saludo al chat
  chat.send_message("Hola! Soy un bot de Telegram creado para ayudarte a encontrar información sobre eventos históricos, el tiempo y más. ¿En qué te puedo ayudar hoy?")

# Agrega un manejador de comandos para el comando "/saludo"
saludo_handler = CommandHandler("saludo", saludo)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(saludo_handler)

def noticias(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat

  # Especifica la URL de la API de noticias
  url = "http://api.mediastack.com/v1/"

  # Especifica los parámetros de la consulta
  params = {
    "apiKey": "0d5738778722b980f9623a314702a054",
    "country": "es",
    "pageSize": 5
  }

  # Realiza la consulta a la API de noticias
  response = requests.get(url, params=params)
  # Carga la respuesta en formato JSON
  data = response.json()

  # Recorre la lista de noticias
  for i, noticia in enumerate(data["articles"]):
    # Envía el título y la descripción de la noticia al chat
    chat.send_message("Noticia #{}: {}\n{}".format(i+1, noticia["title"], noticia["description"]))

# Agrega un manejador de comandos para el comando "/noticias"
noticias_handler = CommandHandler("noticias", noticias)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(noticias_handler)

def traducir(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat

  # Verifica si se proporcionó el texto a traducir
  if len(context.args) == 0:
    chat.send_message("Por favor proporciona el texto que deseas traducir.")
    return

  # Obtiene el texto a traducir
  texto = " ".join(context.args)

  # Especifica la URL de la API de traducción
  url = "https://api.mymemory.translated.net/"
  # Realiza la consulta a la API de traducción
  response = requests.get(url, params=params)
  # Carga la respuesta en formato JSON
  data = response.json()

  # Obtiene la traducción del texto
  traduccion = data["responseData"]["translatedText"]

  # Envía la traducción al chat
  chat.send_message("Traducción: {}".format(traduccion))

# Agrega un manejador de comandos para el comando "/traducir"
traducir_handler = CommandHandler("traducir", traducir)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(traducir_handler)

def tareas(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat

  # Verifica si se proporcionó una acción (agregar, eliminar o mostrar)
  if len(context.args) == 0:
    chat.send_message("Por favor proporciona una acción (agregar, eliminar o mostrar) y la tarea correspondiente.")
    return

  # Obtiene la acción y la tarea
  accion = context.args[0]
  tarea = " ".join(context.args[1:])

  # Verifica si la acción es "agregar"
  if accion == "agregar":
    # Agrega la tarea a la lista de tareas
    tareas.append(tarea)
    chat.send_message("Tarea agregada a la lista.")
  # Verifica si la acción es "eliminar"
  elif accion == "eliminar":
    # Elimina la tarea de la lista de tareas
    tareas.remove(tarea)
    chat.send_message("Tarea eliminada de la lista.")
  # Verifica si la acción es "mostrar"
  elif accion == "mostrar":
    # Muestra la lista de tareas
    chat.send_message("Tareas:\n{}".format("\n".join(tareas)))
  # Si la acción es inválida, muestra un mensaje de error
  else:
    chat.send_message("Acción inválida. Por favor proporciona una acción válida (agregar, eliminar o mostrar) y la tarea correspondiente.")

# Agrega un manejador de comandos para el comando "/tareas"
tareas_handler = CommandHandler("tareas", tareas)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(tareas_handler)

# Inicializa la lista de tareas
tareas = []

def classify_question(question):
  # Tokeniza la pregunta
  tokens = nltk.word_tokenize(question)
  
  # Etiqueta las partes del discurso de cada token
  pos_tags = nltk.pos_tag(tokens)
  
  # Identifica la categoría de la pregunta a partir de las etiquetas de partes del discurso
  if any(tag in pos_tags for tag in ["NN", "NNP", "NNS", "NNPS"]):
    return "HISTORY"
  elif any(tag in pos_tags for tag in ["VB", "VBG", "VBN", "VBP", "VBZ"]):
    return "WEATHER"
  else:
    return "OTHER"

def generar_imagen(update, context):
  # Obtiene el chat (grupo) en el que se envió el comando
  chat = update.message.chat

  # Verifica si se proporcionó el texto para generar la imagen
  if len(context.args) == 0:
    chat.send_message("Por favor proporciona el texto para generar la imagen.")
    return

  # Obtiene el texto para generar la imagen
  texto = " ".join(context.args)

  # Utiliza DALL-E para generar una imagen a partir del texto
  response = openai.Image.create(
    model="image-alpha-001",
    prompt=texto
  )

  # Obtiene la URL de la imagen generada
  imagen_url = response["data"][0]["url"]

  # Descarga la imagen a un archivo temporal
  response = requests.get(imagen_url)
  with open("temp.jpg", "wb") as f:
    f.write(response.content)

  # Envía la imagen al chat
  chat.send_photo(open("temp.jpg", "rb"))

# Agrega un manejador de comandos para el comando "/generar_imagen"
generar_imagen_handler = CommandHandler("imagen", generar_imagen)
# Agrega el manejador de comandos al controlador de mensajes
dispatcher.add_handler(generar_imagen_handler)

def handle_message(update, context):
  # Obtiene el texto del mensaje enviado por el usuario
  user_text = update.message.text
  
  # Clasifica la pregunta utilizando la función classify_question
  category = classify_question(user_text)
  
  # Utiliza una fuente de información diferente dependiendo de la categoría de la pregunta
  if category == "HISTORY":
    # Consulta una base de datos de eventos históricos para obtener una respuesta
    response_text = "Según nuestra base de datos, el evento histórico que mencionas ocurrió el día tal en tal lugar."
  elif category == "WEATHER":
    # Consulta un servicio meteorológico en línea para obtener una respuesta
    response_text = "El pronóstico del tiempo para la ubicación que mencionas indica que hoy tendrás sol y temperaturas máximas de 23 grados."
  else:
    # Utiliza GPT-3 para generar una respuesta a partir del texto del usuario
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=user_text,
      max_tokens=1024,
      top_p=1,
      n=1,
      stop=None,
      temperature=0.5,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    # Proporciona un contexto más específico para GPT-3 al enviar la solicitud de predicción
    prompt = "Pregunta 1: ¿Cuál es tu nombre?\n\nRespuesta 1: Mi nombre es GPT-3.\n\nPregunta 2: ¿De dónde eres?\n\nRespuesta 2: Soy un modelo de lenguaje desarrollado por OpenAI.\n\nPregunta: " + user_text + "\n\nRespuesta:\n"

    # Envía la solicitud de predicción a GPT-3
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      top_p=1,
      n=1,
      stop=None,
      temperature=0.5,
      frequency_penalty=0,
      presence_penalty=0
    )

    # Obtiene la respuesta generada por GPT-3
    gpt3_response = response["choices"][0]["text"]

    # Elimina la parte del prompt de la respuesta
    response_text = gpt3_response.replace(prompt, "")

    # Envía la respuesta a través del bot de Telegram
    context.bot.send_message(chat_id=update.effective_chat.id, text=gpt3_response)

# Agrega un manejador de mensajes para mensajes que mencionan al bot con el @
other_message_handler = MessageHandler(Filters.text & (~Filters.command) & (Filters.regex(f"@{bot_username}")), handle_message)
dispatcher.add_handler(other_message_handler)

# Inicia el bucle de espera de mensajes
updater.start_polling()
updater.idle()