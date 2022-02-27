from ctypes import pointer
from ctypes.wintypes import POINT, POINTL
from distutils import command
from gettext import gettext
from webbrowser import get
from xml.etree.ElementInclude import include
import requests
from bs4 import BeautifulSoup
import re
import telebot, wikipedia, re
from telebot import types # для указание типов
from bs4 import BeautifulSoup 



token=('5079681907:AAHIdslm92acYBkQGiIBpZevWt4W0quIOVA')
bot = telebot.TeleBot('5079681907:AAHIdslm92acYBkQGiIBpZevWt4W0quIOVA')
bot = telebot.TeleBot(token)
wikipedia.set_lang("ru")




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn2 = types.KeyboardButton("/расписание")
    btn3 = types.KeyboardButton("/звонки")
    
    markup.add( btn2, btn3)
    
    bot.send_message(message.chat.id, text=" ".format(message.from_user), reply_markup=markup)
    













































def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:10000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2



    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'Пиши понятно,быдло'







# Функция, обрабатывающая команду /расписание
@bot.message_handler(commands=["расписание"])
def start(m, res=False):
 response = requests.get("https://omacademy.ru/rasp/dirp9-3.html") 
 soup = BeautifulSoup(response.content, 'html.parser') 

 table = soup.find("table", class_="rasp")
 output = []
 for row in table.findAll("tr"):
     new_row = []
     for cell in row.findAll(["td", "th"]):
         for sup in cell.findAll('sup'):
             sup.extract()
         for collapsible in cell.findAll(
                 class_="mw-collapsible-content"):
             collapsible.extract()
         new_row.append(cell.get_text().strip())
     output.append(new_row)

 i = len(output)
 
 

 if i==4:
    text = f" {output[1]}\n\n" \
          f" {output[2]}\n\n" \
               f" {output[3]}\n\n" \

   
    bot.send_message(m.chat.id,text)
                    

 elif i== 5 :
     
     text = f" {output[1]}\n\n" \
          f" {output[2]}\n\n" \
               f" {output[3]}\n\n" \
                   f" {output[4]}\n\n" \


     print(output)


     bot.send_message(m.chat.id,text)

 elif i== 3 :
     
     text = f" {output[1]}\n\n" \
          f" {output[2]}\n\n" \



     print(output)


     bot.send_message(m.chat.id,text)

# Звонки
@bot.message_handler(commands=["звонки"])
def start(m, res=False):
    song = f" 1 Пара 8:00 - 9:40 \n Отдых 8:45 - 8:55  \n\n" \
    f" 2 Пара 9:50 - 11:30 \n Отдых 10:35 - 10:45 \n\n"\
    f" 3 Пара 11:50 - 13:30 \n Отдых 12:35 - 12:45 \n\n"\
    f" 4 Пара 13:50 - 15:30 \n Отдых 14:35 - 14:45 \n\n"\
    f" 5 Пара 15:40 - 17:20 \n Отдых 16:25 - 16:35 \n\n"\
    f" 6 Пара 17:40 - 19:20 \n Отдых 18:25 - 18:35 \n\n"\
    f" 7 Пара 19:30 - 21:00 "
    bot.send_message(m.chat.id,song)



# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))
# Запускаем бота
bot.polling(none_stop=True, interval=0)

