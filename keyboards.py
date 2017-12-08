from telebot import types

usertypeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
usertypeSelect.row('Ученик', 'Преподаватель')

placeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
placeSelect.row('Авиапарк', 'Офис QIWI')
placeSelect.row('Павловская гимназия')

purposeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
purposeSelect.row('Записаться')
purposeSelect.row('Ознакомиться с расписанием')

phoneKeyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
phoneKeyboard.add(button_phone)

courseSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
courseSelect.row('Програмирование','Робототехника','Анимация')
courseSelect.row('Создание игр на Unity', '"Я – звезда YouTube"')

helpBoard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
helpBoard.row('\help')

hideBoard = types.ReplyKeyboardRemove()
