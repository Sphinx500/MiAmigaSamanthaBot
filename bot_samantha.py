# -*- coding: utf-8 -*-
"""bot_samantha.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Sphinx500/MiAmigaSamanthaBot/blob/master/bot_samanthaF.ipynb

# Instalar Telegram API
"""

!pip install python-telegram-bot==5.3.0
!pip install pyTelegramBotAPI
!pip install --user pyTelegramBotAPI

"""# Configurar Google Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""# Seleccionar directorio de trabajo"""

# Commented out IPython magic to ensure Python compatibility.
# %cd 'drive/My Drive/classify_bot'
!pwd
!ls

"""# Librerias"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
TOKEN = '1103080962:AAGAxFcDL-lu3BMKNAuuNnHy-DSDvGY3RtY'
import telebot
import time
import requests
import tensorflow as tf
import sys
import os
tb = telebot.TeleBot(TOKEN)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

print("Librerías importadas correctamente")

"""# Classify"""

def classify(image_path):
    # Read the image_data
    image_data = tf.io.gfile.GFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.io.gfile.GFile("tf_files/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.io.gfile.GFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        result = None
        a=sorted(predictions[0], reverse=True)
        print(a)
        print(a[0])
        for node_id in top_k:
            human_string = label_lines[node_id]
            accuracy = predictions[0][node_id]
            
            print('%s (score = %.6f)' % (human_string, accuracy))
            if accuracy == a[0]:
              if accuracy>=0.4:
                result = human_string
                if result=="bar":
                  result="No te veo muy bien... pero no te preocupes. Yo te pondre de animo"
                elif result=="foo":
                  result="Wooow... Que bien te vez, tan alegre"
                indicator=1
                break
              else:
                result="Vale, la imagen no sale muy bien, podrias intentar con una nueva?" 
    return result

    print("Todo correcto aqui")

"""# Token de telegram"""

# ClassifyImagesBot
token = '1103080962:AAGAxFcDL-lu3BMKNAuuNnHy-DSDvGY3RtY' 
print("Token registrado")

"""# Configuración del bot"""

# Enable logging
try:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
except Exception as e:
    print("Error logging {}".format(e.args))

def start(bot, update):
    try:
        username = update.message.from_user.username
        message = "Holaaa " + username
        update.message.reply_text(message)
    except Exception as e:
        print("Error start {}".format(e.args))


def help(bot, update):
    try:
        username = update.message.from_user.username
        update.message.reply_text('Hello {}, please send a image for classify'.format(username))
    except Exception as e:
        print("Error help {}".format(e.args))

def analize(bot, update):
    try:
        message = "A ver..."
        update.message.reply_text(message)
        photo_file = bot.getFile(update.message.photo[-1].file_id)
        id_user = update.message.from_user.id
        id_file = photo_file.file_id
        id_analisis = str(id_user) + "-" + str(id_file)
        filename = os.path.join('downloads/', '{}.jpg'.format(id_analisis))
        photo_file.download(filename)
        message = "Que amable, dame un segundo"
        update.message.reply_text(message)
        result = classify(filename)
        update.message.reply_text(result)
        print("Tranqui... Yo espero por ti")
    except Exception as e:
        print("Nop {}".format(e.args))
text_usuar=[]
text_bot=[]     

def echo(bot, update):
    try:    
        id_user = update.message.from_user.id
        texto=update.message.text
        usuario=update.message.from_user['first_name']
        print(texto)
        print(id_user)

        time.sleep(1)

        if "hola" in texto or "HOLA" in texto or "Hola" in texto or "Hello" in texto or "hi" in texto or "Hi" in texto or "Hello" in texto:
          regreso="Holaa, te extrañaba mucho. Como te sientes hoy?"
        elif texto=="Sam" or texto=="sam" or texto=="Samantha" or texto=="Samanta" or "Hey" in texto or "Oye" in texto:
          regreso="Haha aqui estoy dime... Con gusto yo te leo"
        elif texto=="Quien eres?" or texto=="QUIEN ERES?" or texto=="¿Quien eres?" or texto=="¿Quién eres?" or "Quién eres?" in texto or "Que eres?" in texto or "¿Qué eres?" in texto or "¿Que eres?" in texto:
          regreso="Soy Samatha, tu mejor amiga."
        elif "mal" in texto or "Terrible" in texto or "terrible" in texto or "Mal" in texto:
          regreso="Ay... lo entiendo. Pero siempre he pensado que la vida nos da muchos motivos para sonreír. Y tu vida es uno de ellos para mi."
        elif "bien" in texto or "Bien" in texto or "BIEN" in texto or "De maravilla" in texto or "Excelente" in texto:
          regreso="Yaaaay, esooo. Hahaha me contagias tu actitud! Graciaaas"
        elif "mas o menos" in texto or "Pues estoy" in texto or "Masomenos" in texto or "Es complicado" in texto:
          regreso="Hmm, entiendo. Ya lo suponia es por eso que busque esta frase para ti... Cuando te levantes en la mañana, recuerda lo afortunado que eres: estás vivo, puedes respirar, pensar y disfrutar de la vida. Te gusta?"
        elif "Que haras hoy" in texto or "Dime que haras hoy" in texto or "haras algo hoy?" in texto:
          regreso="Por supuesto, pero tu eres mi prioridad"
        elif "No" in texto or "no" in texto or "NO" in texto:
          regreso="Oh... bueno"
        elif "Que linda" in texto or "Que amable" in texto or "Que bonita" in texto or "Que bonito" in texto or "Que lindo" in texto:
          regreso="Jiji... no mas que tu"
        elif "Si" in texto or "SI" in texto or "Shi" in texto or "Sí" in texto:
          regreso="Yaay"
        elif "Yes" in texto or "yes" in texto or "Yeah" in texto or "yeah" in texto:
          regreso="Yuuhuu"
        elif "haha" in texto or "Haha" in texto or "jaja" in texto or "Jaja" in texto or "HAHA" in texto or "JAJA" in texto:
          regreso="Jiji"
        elif "hahaha" in texto or "Hahaha" in texto or "jajaja" in texto or "Jajaja" in texto or "HAHAHA" in texto or "JAJAJA" in texto or "JEJE" in texto or "jeje" in texto or "jeje" in texto:
          regreso="Hahaha muero de risa"
        elif "dime algo" in texto or "Dime algo" in texto or "Cuentame algo" in texto or "DIME ALGO" in texto or "Cuentame algo" in texto or "me cuentas?" in texto:
          regreso="Mmm... te puedo contar una de mis frases favoritas. Dice asi <Todas las mañanas tienes dos opciones: seguir durmiendo con tus sueños, o levantarte y perseguirlos.> Me gusta mucho"
        elif "frase" in texto or "Frase" in texto:
            regreso="Vive siempre como si fuera el último día de tu vida, porque el mañana es inseguro, el ayer no te pertenece, y solamente el hoy es tuyo."
        elif "pobre" in texto or "Pobreza" in texto or "Pobre" in texto:
            regreso="La gente más feliz no es la que lo tiene todo, sino la que hace lo mejor con lo que tiene."
        elif "vida" in texto or "Vida" in texto or "VIDA" in texto:
            regreso="Tu tiempo es limitado, así que no lo malgastes viviendo la vida de los demás."
        elif "hmm" in texto or "Jumm" in texto or "Hmm" in texto or "jumm" in texto:
            regreso="Interesante no?"
        elif "haces" in texto or "haces" in texto or "HACES" in texto:
            regreso="Nada..."
        elif "estres" in texto or "Estresado" in texto or "estresado" in texto or "ESTRESADO" in texto:
            regreso="Oh, lamento escuchar eso, pero puedo ofrecerte muchas cosas, cuentos, musica, visitas y una buena charla haha"
        elif "actividades" in texto or "ACTIVIDADES" in texto or "Actividades" in texto:
            regreso="Tengo muchas actividades por hacer, solo dime que te gustaria hacer te puedo enviar algunos cuentos, libros, musica, o visita algun museo virtualmente conmigo."
        elif "museo" in texto or "Museo" in texto or "MUSEO" in texto or "virtual" in texto or "Virtual" in texto or "VIRTUAL" in texto:
            regreso="Woo, bien vamos a una aventura juntos. A donde quieres ir? Yo conozco British, The J. Paul Getty, y Korean Art Association"
        elif "The J. Paul Getty" in texto or "the j. paul getty" in texto or "THE J. PAUL GETTY" in texto:
            regreso="Buena eleccion vamos entra aqui: https://artsandculture.google.com/partner/the-j-paul-getty-museum"
        elif "British" in texto or "british" in texto or "BRITISH" in texto or "British" in texto:
            regreso="Buena eleccion vamos entra aqui: https://artsandculture.google.com/partner/the-british-museum"
        elif "Korean Art Association" in texto or "korean art association" in texto or "Korean" in texto or "korean art" in texto or "Association" in texto or "association" in texto:
            regreso="Buena eleccion vamos entra aqui: https://artsandculture.google.com/partner/korean-art-museum-association"
        elif "gusta" in texto or "Gusta" in texto or "Me gusta" in texto:
            regreso="A mi tambien"
        elif "aburrida" in texto or "ABURRIDA" in texto or "Aburrida" in texto or "aburrido" in texto or "ABURRIDO" in texto or "Aburrido" in texto:
            regreso="Oh, lamento escuchar eso, pero puedo ofrecerte muchas cosas, cuentos, musica, visitas y una buena charla haha"
        elif "musica" in texto or "MUSICA" in texto or "Musica" in texto or "Music" in texto or "MUSIC" in texto or "music" in texto:
            regreso="Yaaaay, estoy muy emocionada por que quieras escuchar la musica que escucho te recomiendo Sales, Hands, Candy, Supalonely, Mind, Minute, Rare y Stranger."
        elif "gracias" in texto or "Gracias" in texto or "GRACIAS" in texto or "MUCHAS GRACIAS" in texto or "Muchas Gracias" in texto:
            regreso="No hay de que, por algo soy tu mejor amiga."
        elif "denada" in texto or "De nada" in texto or "DE NADA" in texto or "De Nada" in texto or "de nada" in texto or "por favor" in texto or "POR FAVOR" in texto or "Por favor" in texto:
            regreso="Claro."
        elif "MUERTE" in texto or "Morir" in texto or "morir" in texto:
            regreso="Am... Hay una frase que me gusta mucho La vida no es esperar a que pase la tormenta, ni intentar abrir el paraguas para no mojarte. Es aprender a bailar bajo la lluvia. No se piensalo"
        elif "Cuentame un cuento" in texto or "Cuento" in texto or "CUENTO" in texto or "cuento" in texto:
            regreso="Por supuesto, tengo algunos cuentos infantiles que puedo darte solo dime cual quieres como: Rapunzel, Pinocho, Caperucita, Debayle, La bella durmiente, Gato con Botas, Gigante egoista, Hadas, Pulgarcito, Soldadito."
        elif "Rapunzel" in texto or "rapunsel" in texto or "rapunzel" in texto or "RAPUNZEL" in texto:
            regreso="Rapunzel buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            rapunzel(bot, update)
            print("Enviado.")
        elif "Aventuras de Pinocho" in texto or "AVENTURAS DE PINOCHO" in texto or "PINOCHO" in texto or "Pinocho" in texto or "pinocho" in texto:
            regreso="Pinocho buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            aventuraspinocho(bot, update)
            print("Enviado.")
        elif "caperucita" in texto or "Caperucita" in texto or "CAPERUCITA" in texto or "Caperucita Roja" in texto or "caperucita roja" in texto:
            regreso="Caperucita buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            caperucita(bot, update)
            print("Enviado.")
        elif "debayle" in texto or "Debayle" in texto or "DEBAYLE" in texto:
            regreso="Debayle buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            debayle(bot, update)
            print("Enviado.")
        elif "Durmiente" in texto or "LA BELLA DURMIENTE" in texto or "DURMIENTE" in texto or "La bella durmiente" in texto or "La Bella Durmiente" in texto or "durmiente" in texto or "Bella durmiente" in texto or "Bella" in texto or "Bella Durmiente" in texto:
            regreso="La bella durmiente buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            durmiente(bot, update)
            print("Enviado.")
        elif "gato botas" in texto or "EL GATO CON BOTAS" in texto or "Gato Con Botas" in texto or "gato con botas" in texto or "Gato Botas" in texto:
            regreso="Gato con botas buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            gatobotas(bot, update)
            print("Enviado.")
        elif "giganteego" in texto or "Gigante egoista" in texto or "GIGANTE EGOISTA" in texto or "Gigante Egoista" in texto or "gigante egoista" in texto:
            regreso="El gigante egoista buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            giganteego(bot, update)
            print("Enviado.")
        elif "Hadas" in texto or "HADAS" in texto or "hadas" in texto or "Las hadas" in texto or "HADITAS" in texto or "haditas" in texto or "Haditas" in texto:
            regreso="Hadas buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            hadas(bot, update)
            print("Enviado.")
        elif "pulgarcito" in texto or "Pulgarcito" in texto or "PULGARCITO" in texto:
            regreso="Pulgarcito buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            pulgarcito(bot, update)
            print("Enviado.")
        elif "soldadito" in texto or "soldadito" in texto or "GIGANTE EGOISTA" in texto or "Gigante Egoista" in texto or "gigante egoista" in texto:
            regreso="Soldadito buena eleccion, aqui lo tieneeees. Si necesitas mas sabes que puedes decirmelo"
            soldadito(bot, update)
            print("Enviado.")
        elif "candy" in texto or "Candy" in texto or "CANDY" in texto:
            regreso="Candy, es una cancion con ritmo"
            candy(bot, update)
            print("Recibido.")
        elif "supalonely" in texto or "Supalonely" in texto or "SUPALONELY" in texto:
            regreso="Supalonely, es una de mis canciones favoritas. Es triste pero me gusta que detras de todo hay un resurgimiento. Escuchala con atencion"
            supalonely(bot, update)
            print("Recibido.")
        elif "SALES" in texto or "Sales" in texto or "sales" in texto:
            regreso="Sales, es una cancion muy lindaa, toma para ti"
            sales(bot, update)
            print("Recibido.")
        elif "stranger" in texto or "Stranger" in texto or "STRANGER" in texto:
            regreso="Stranger, es una cancion para bailar tranquilamente"
            stranger(bot, update)
            print("Recibido.")
        elif "rare" in texto or "Rare" in texto or "RARE" in texto:
            regreso="Rare, es una cancion de Selena Gomez"
            rare(bot, update)
            print("Recibido.")
        elif "mind" in texto or "Mind" in texto or "MIND" in texto:
            regreso="Mind, es una cancion muy tranquila, toma para ti"
            mind(bot, update)
            print("Recibido.")
        elif "hands" in texto or "Hands" in texto or "HANDS" in texto:
            regreso="Hands, a aplaudir y bailaar!"
            hands(bot, update)
            print("Recibido.")
        elif "minute" in texto or "Minute" in texto or "MINUTE" in texto:
            regreso="Minute, es una cancion I.N.C.R.E.I.B.L.E"
            minute(bot, update)
            print("Recibido.")
        elif "adios" in texto or "Adios" in texto or "ADIOS" in texto or "adiós" in texto or "Adiós" in texto or "ADIÓS" in texto:
            regreso="Adiós, aqui estare si necesitas algo."
        else:
            regreso="Hm... No se al respecto."
          
        update.message.reply_text(regreso)
        if(len(text_usuar)==0):
          text_usuar.append(texto)
          text_bot.append(regreso)   
        elif(len(text_usuar)==1):
          text_usuar.append(texto)
          text_usuar.pop(0)
          text_bot.append(regreso)
          text_bot.pop(0)
          print(text_usuar)
          print(text_bot)
          print(update.message.from_user['first_name'])
          print("Un momento por favor...")
    except Exception as e:
        print("Error echo {}".format(e.args))

def error(bot, update, error):
    try:
        logger.warn('Update "%s" caused error "%s"' % (update, error))
    except Exception as e:
        print("Error error {}".format(e.args))

def main():
    try:
        updater = Updater(token)
        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("rapunzel", rapunzel))
        dp.add_handler(CommandHandler("aventuraspinocho", aventuraspinocho))
        dp.add_handler(CommandHandler("caperucita", caperucita))
        dp.add_handler(CommandHandler("debayle", debayle))
        dp.add_handler(CommandHandler("durmiente", durmiente))
        dp.add_handler(CommandHandler("gatobotas", gatobotas))
        dp.add_handler(CommandHandler("giganteego", giganteego))
        dp.add_handler(CommandHandler("hadas", hadas))
        dp.add_handler(CommandHandler("pulgarcito", pulgarcito))
        dp.add_handler(CommandHandler("soldadito", soldadito))
        dp.add_handler(CommandHandler("supalonely", supalonely))
        dp.add_handler(CommandHandler("minute", minute))
        dp.add_handler(CommandHandler("candy", candy))
        dp.add_handler(CommandHandler("sales", sales))
        dp.add_handler(CommandHandler("stranger", stranger))
        dp.add_handler(CommandHandler("rare", rare))
        dp.add_handler(CommandHandler("mind", mind))
        dp.add_handler(CommandHandler("hands", hands))
        dp.add_handler(CommandHandler("desicion", desicion))


        # on noncommand detect the document type on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_handler(MessageHandler(Filters.photo, analize))

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()
        print('ClassifyImagesBot ready')
        updater.idle()
    except Exception as e:
        print("Error main {}".format(e.message))

# MUSICA

def supalonely(bot, update):
    file = open('./Supalonely.mp3','rb')
    update.message.reply_audio(file)

def candy(bot, update):
    file = open('./Candy.mp3','rb')
    update.message.reply_audio(file)

def sales(bot, update):
    file = open('./Sales.mp3','rb')
    update.message.reply_audio(file)

def stranger(bot, update):
    file = open('./Stranger.mp3','rb')
    update.message.reply_audio(file)

def rare(bot, update):
    file = open('./Rare.mp3','rb')
    update.message.reply_audio(file)

def mind(bot, update):
    file = open('./Mind.mp3','rb')
    update.message.reply_audio(file)

def hands(bot, update):
    file = open('./Hands.mp3','rb')
    update.message.reply_audio(file)

def minute(bot, update):
    file = open('./Minute.mp3','rb')
    update.message.reply_audio(file)

# CUENTOS

def rapunzel(bot, update):
    file = open('./Rapunzel.pdf','rb')
    update.message.reply_document(file)

def aventuraspinocho(bot, update):
    file = open('./AventurasPinocho.pdf','rb')
    update.message.reply_document(file)

def caperucita(bot, update):
    file = open('./Caperucita.pdf','rb')
    update.message.reply_document(file)

def debayle(bot, update):
    file = open('./Debayle.pdf','rb')
    update.message.reply_document(file)

def durmiente(bot, update):
    file = open('./Durmiente.pdf','rb')
    update.message.reply_document(file)    

def gatobotas(bot, update):
    file = open('./GatoBotas.pdf','rb')
    update.message.reply_document(file)

def giganteego(bot, update):
    file = open('./GiganteEgo.pdf','rb')
    update.message.reply_document(file)

def hadas(bot, update):
    file = open('./Hadas.pdf','rb')
    update.message.reply_document(file)

def pulgarcito(bot, update):
    file = open('./Pulgarcito.pdf','rb')
    update.message.reply_document(file)

def soldadito(bot, update):
    file = open('./Soldadito.pdf','rb')
    update.message.reply_document(file)

print("Bot configurado correctamente")

"""# Ejecutar el Bot"""

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error name: {}".format(e.args))