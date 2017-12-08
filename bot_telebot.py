import requests
import time
import smtplib
import telebot
from telebot import types
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from keyboards import *
from defs import *

# import parser

TOKEN = '462098019:AAHi_pKoFjqnAwKalqt2HEWXwKQ7kUjJx6M'

commands = {  # command description used in the "help" command
              'start': 'Начать работу с ботом',
              'info': 'Ознакомиться с дополнительной информацией о боте',
              'help': 'Помощь по работе с ботом',
}

userStep = {}
knownUsers = []

pupil_choose = ''
enrollCourse = ''
enrollPlace = ''
enrollFio = ''
enrollPhone = ''

bot_help = 'Доступные команды:\n/start - узнать расписание либо записаться\n/info - узнать о боте'

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("Новый пользователь? Начните с команды \"/start\"")
        return 0

@bot.message_handler(commands=['start','\back'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Здравствуйте! Уточните пожалуйста, ученик Вы или преподаватель?", reply_markup = usertypeSelect)
    userStep[cid] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def usertype_select(m):
    cid = m.chat.id
    text = m.text

    bot.send_chat_action(cid, 'typing')

    if text == 'Ученик':
        bot.send_message(cid, "Замечательно, чем я могу Вам помочь?", reply_markup = purposeSelect)
        userStep[cid] = 2

    elif text == 'Преподаватель':
        bot.send_message(cid, "Добрый день, {}, рад Вас видеть!\n По какой площадке желаете посмотреть расписание?".format(m.chat.first_name), reply_markup = placeSelect)
        userStep[cid] = 3

    else:
        bot.send_message(cid, 'Я не знаю такой команды :(\n Вызовите /help для того чтобы узнать, как со мной работать') 


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def purpose_select(m):
    cid = m.chat.id
    text = m.text
    
    bot.send_chat_action(cid, 'typing')

    if text == 'Записаться':
        bot.send_message(cid, 'Выберите интересующий Вас курс', reply_markup = courseSelect)
        userStep[cid] = 4

    elif text == 'Ознакомиться с расписанием':
        bot.send_message(cid, 'Выберите интересующий Вас курс', reply_markup = courseSelect)
        userStep[cid] = 5
    
    else:
        bot.send_message(cid, 'Я не знаю такой команды :( Вызовите /help для того чтобы узнать, как со мной работать', reply_markup = hideBoard) 
        userStep[cid] = 1

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def teacher_select(m):
    cid = m.chat.id
    text = m.text
    
    bot.send_chat_action(cid, 'typing')

    if text in ('Авиапарк', 'Павловская гимназия', 'Офис QIWI'):
        teacherSchedule = teacher_scheduler(text)
        bot.send_message(cid, teacherSchedule)
    else:
        bot.send_message(cid, 'Я не знаю такой команды :( Вызовите /help для того чтобы узнать, как со мной работать', reply_markup = hideBoard) 


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def enroll_course_select(m):
    cid = m.chat.id
    text = m.text
    
    bot.send_chat_action(cid, 'typing')

    if text in ('Создание игр на Unity', 'Програмирование', '"Я – звезда YouTube"', 'Робототехника', 'Анимация'):
        global enrollCourse
        enrollCourse = text
        
        i = check_places(text)
    
        if i.count('\n') == 0:
            enrollKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            enrollKeyboard.row(i)

            bot.send_message(cid, 'Выбранный курс проходит на площадке ' + i)
            bot.send_message(cid, '\nЧтобы продолжить, подтвердите нажатием кнопки.\nДля возврата в стартовое меню нажмите /start', reply_markup = enrollKeyboard)

        elif i.count('\n') == 1:
            enrollKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            enrollKeyboard.row(i.split("\n")[0])
            enrollKeyboard.row(i.split("\n")[1])
            bot.send_message(cid, 'Выбранный курс проходит на двух площадках:\n ' + i)
            bot.send_message(cid, 'Выберите наиболее удобную для Вас', reply_markup = enrollKeyboard)
    
        userStep[cid] = 8
    else:
        bot.send_message(cid, 'Я не знаю такой команды :( Вызовите /help для того чтобы узнать, как со мной работать', reply_markup = helpBoard) 

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 5)
def view_course_select(m):
    cid = m.chat.id
    text = m.text
    
    global pupil_choose
    pupil_choose = text
    
    bot.send_chat_action(cid, 'typing')

    i = check_places(text)
    
    if text in ('Создание игр на Unity', 'Програмирование', '"Я – звезда YouTube"', 'Робототехника', 'Анимация'):
        
        if i.count('\n') == 0:
            enrollPkeyboard0 = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            enrollPkeyboard0.row(i)
            bot.send_message(cid, 'Выбранный курс проходит на площадке ' + i + '\nПодтвердите, пожалуйста, выбор', reply_markup = enrollPkeyboard0)

        elif i.count('\n') == 1:
            enrollPkeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            enrollPkeyboard.row(i.split("\n")[0])
            enrollPkeyboard.row(i.split("\n")[1])
            bot.send_message(cid, 'Выбранный курс проходит на двух площадках:\n ' + i)
            bot.send_message(cid, '\nВыберите наиболее удобную для Вас', reply_markup = enrollPkeyboard)
    
        userStep[cid] = 7

    else:
        bot.send_message(cid, 'Я не знаю такой команды :( Вызовите /help для того чтобы узнать, как со мной работать', reply_markup = hideBoard) 
   
    #bot.send_message(cid, 'Если вы определились с курсом и площадкой, напишите сообщение следующей формы:\nХочу записаться на курс НАЗВАНИЕ_КУРСА, ТЕЛЕФОН')
    
    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 7)
def view_place_select(m):
    cid = m.chat.id
    text = m.text
    
    out = pupil_scheduler(text, pupil_choose)
    bot.send_message(cid, out)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 8)
def auth(m):
    cid = m.chat.id
    text = m.text
    
    global enrollPlace
    enrollPlace = text

    bot.send_message(cid, "Замечательно! Теперь введите Ваше ФИО (в полной форме)")
    userStep[cid] = 9


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 9)
def fio(m):
    cid = m.chat.id
    text = m.text
    
    global enrollFio
    enrollFio = text

    bot.send_message(cid, "Мы почти закончили, " + text.split()[1] + " " + text.split()[2] + ". Последний шаг - введите свой номер телефона (вручную либо  кнопкой)", reply_markup = phoneKeyboard)
    userStep[cid] = 10
    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 10)
def sending(m):
    cid = m.chat.id
    text = m.text
    
    global enrollPhone
    enrollPhone = text
    
    mail_msg = MIMEMultipart()
    mail_msg['From'] = "daslef93@gmail.com"
    mail_msg['To'] = "noisemanx@gmail.com"
    mail_msg['Subject'] = 'Запись на курсы'
    
    body = 'Курс:\t{}\nПлощадка:\t{}\nФИО:\t{}\nТелефон:\t{}\n'.format(enrollCourse, enrollPlace, enrollFio, enrollPhone)
    mail_msg.attach(MIMEText(body, 'plain'))
    mail_text = mail_msg.as_string()

    smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpObj.login('daslef93@gmail.com','zamane59')
    smtpObj.sendmail("daslef93@gmail.com","noisemanx@gmail.com", mail_text)
    smtpObj.quit()
    
    userStep[cid] = 1
    bot.send_message(cid, "Поздравляем, Ваша заявка была отправлена!\nОжидайте, уже в самое ближайшее время с Вами свяжется наш сотрудник")

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)
    
    
@bot.message_handler(commands=['info'])
def command_info(m):
    cid = m.chat.id
    bot.send_message(cid, 'Бот-Расписаниевед версии 0.2, создан Алексеем', reply_markup = hideBoard)
    
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "Я не понимаю, что значит \"" + m.text + "\".\nРекомендую ознакомиться с /help", reply_markup = hideBoard)

bot.polling(none_stop = True)