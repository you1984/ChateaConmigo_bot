import openai
import telegram
import nltk
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Inicializa el bot de Telegram
updater = Updater("5887157767:AAE7lgtroWxMNAeXYWrppUvPjoF5JYck7dY", use_context=True)
dispatcher = updater.dispatcher

# Inicializa la conexión a GPT-3
openai.api_key = "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"

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
      top_p=0.9,
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

# Establece el manejador de mensajes para que se ejecute cuando el bot reciba un mensaje
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
dispatcher.add_handler(message_handler)

# Inicia el bucle de espera de mensajes
updater.start_polling()

updater.idle()