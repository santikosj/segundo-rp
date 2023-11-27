import telebot
import random


bot = telebot.TeleBot("6716252736:AAESihDvzczovRU_H2lXRGhAwEQWHn2mnbg")


conversaciones = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy un bot psicólogo. ¿Cómo estás hoy?")
    conversaciones[message.chat.id] = {'pregunta': True, 'categoria': None, 'respuestas': []}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id in conversaciones and conversaciones[chat_id]['pregunta']:
        ask_feeling_question(chat_id, message.text)
        conversaciones[chat_id]['pregunta'] = False
    else:
        handle_feeling_answers(chat_id, message.text)

def ask_feeling_question(chat_id, respuesta_usuario):
    preguntas_triste = [
        "¿Puedes identificar alguna razón específica por la que te sientes triste?",
        "¿Hay algo que puedas hacer para mejorar tu estado de ánimo?",
        "¿Te gustaría hablar más sobre lo que te está entristeciendo?"
    ]

    preguntas_enojado = [
        "¿Qué fue lo que te hizo enojar?",
        "¿Cómo manejas generalmente la ira?",
        "¿Hay algo que pueda hacer para ayudarte a calmarte?"
    ]

    preguntas_desilusionado = [
        "¿Cuál fue la situación que te llevó a sentirte desilusionado?",
        "¿Hay expectativas específicas que no se cumplieron?",
        "¿Cómo crees que podrías superar esta desilusión?"
    ]

    preguntas_solo = [
        "¿Cómo te sientes estando solo?",
        "¿Hay actividades que disfrutas hacer por ti mismo?",
        "¿Te gustaría explorar maneras de conectar con otras personas?"
    ]

    preguntas_estresado = [
        "¿Puedes identificar la fuente principal de tu estrés?",
        "¿Cómo sueles lidiar con situaciones estresantes?",
        "¿Hay formas en las que puedo ayudarte a reducir tu estrés?"
    ]

    # Analizar la respuesta del usuario y clasificarla
    if "triste" in respuesta_usuario.lower():
        preguntas = preguntas_triste
        categoria = "triste"
    elif "enojado" in respuesta_usuario.lower():
        preguntas = preguntas_enojado
        categoria = "enojado"
    elif "desilusionado" in respuesta_usuario.lower():
        preguntas = preguntas_desilusionado
        categoria = "desilusionado"
    elif "solo" in respuesta_usuario.lower():
        preguntas = preguntas_solo
        categoria = "solo"
    elif "estresado" in respuesta_usuario.lower():
        preguntas = preguntas_estresado
        categoria = "estresado"
    else:
        preguntas = ["¿Cómo te sientes en general?"]
        categoria = None

    conversaciones[chat_id]['categoria'] = categoria

    for pregunta in preguntas:
        bot.send_message(chat_id, pregunta)

    conversaciones[chat_id]['pregunta'] = True


def handle_feeling_answers(chat_id, respuesta_usuario):
    if chat_id in conversaciones and conversaciones[chat_id]['categoria']:
        conversaciones[chat_id]['respuestas'].append(respuesta_usuario)

        if len(conversaciones[chat_id]['respuestas']) == 3:
            conclusion = generate_conclusion(conversaciones[chat_id]['categoria'], conversaciones[chat_id]['respuestas'])
            bot.send_message(chat_id, conclusion)
            conversaciones[chat_id] = {'pregunta': True, 'categoria': None, 'respuestas': []}

def generate_conclusion(categoria, respuestas):
    if categoria == "triste":
        conclusiones = [
            "Lamento que te sientas triste. Considera hablar con amigos o familiares para obtener apoyo emocional.",
            "La tristeza es una emoción natural. Si persiste, podría ser útil hablar con un profesional de la salud mental.",
            "Recuerda que no estás solo en esto. Busca actividades que te den alegría para contrarrestar la tristeza."
        ]
    elif categoria == "enojado":
        conclusiones = [
            "El enojo es una emoción fuerte. Intenta identificar la causa principal y considera formas constructivas de expresarlo.",
            "Practicar la respiración profunda puede ayudar a calmar la ira. También es útil hablar sobre lo que te molestó.",
            "Recuerda que está bien sentir enojo, pero es importante manejarlo de manera saludable para tu bienestar."
        ]
    elif categoria == "desilusionado":
        conclusiones = [
            "La desilusión puede ser desafiante. Reflexiona sobre expectativas realistas y busca nuevas metas.",
            "A veces, las cosas no salen como esperamos. Aprende de la experiencia y busca oportunidades de crecimiento.",
            "Considera hablar con amigos o seres queridos sobre cómo te sientes para obtener diferentes perspectivas."
        ]
    elif categoria == "solo":
        conclusiones = [
            "La soledad puede ser difícil. Intenta conectarte con amigos o familiares, incluso si es a través de videollamadas.",
            "Explora actividades que disfrutes y que te permitan estar en compañía, como unirte a grupos o clases.",
            "Recuerda que la soledad es una experiencia común, y a veces, dar el primer paso para socializar puede marcar la diferencia."
        ]
    elif categoria == "estresado":
        conclusiones = [
            "La gestión del estrés es clave para el bienestar. Considera técnicas como el mindfulness o el ejercicio para reducir el estrés.",
            "Hacer pequeños cambios en tu rutina diaria puede tener un impacto positivo en la reducción del estrés.",
            "Si el estrés persiste, considera buscar apoyo profesional para desarrollar estrategias efectivas de manejo del estrés."
        ]
    else:
        conclusiones = ["Revisa tus respuestas y considera buscar apoyo adicional si es necesario."]

    return random.choice(conclusiones)


bot.polling()
