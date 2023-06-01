import telebot
import billfile
from config import *


# Создание клавиатуры 
def menuKey(c_id):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Сигнали', callback_data=f'update_signal={c_id}'),
        telebot.types.InlineKeyboardButton('Сусіди', callback_data=f'neighbours_key={c_id}'),
        telebot.types.InlineKeyboardButton('Пароль', callback_data=f'pppoe_pass={c_id}'),
        telebot.types.InlineKeyboardButton("\U0001F6E0", callback_data=f'advancekey={c_id}')
    )
    return keyboard

def selectClientKey(d):
    keyboard = telebot.types.InlineKeyboardMarkup()
    l=list(d.keys())
    ni = 0
    for i in range(0, len(l), 2):  # перебираем элементы списка по 5 штук
        row = []  # создаем пустой список для кнопок текущей строки
        for j in range(i, min(i+2, len(l))):  # перебираем элементы строки (не более 5 штук)
            row.append(telebot.types.InlineKeyboardButton(text=str(d[l[j]]), callback_data=f'get_client={str(l[j])}'))
        keyboard.row(*row)  # добавляем кнопки текущей строки в клавиатуру
        ni += 1
        if ni>=15:
            break

    return keyboard

def neighboursKey(c_id):
    l = billfile.neighbours(c_id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(l), 5):  # перебираем элементы списка по 5 штук
        row = []  # создаем пустой список для кнопок текущей строки
        for j in range(i, min(i+5, len(l))):  # перебираем элементы строки (не более 5 штук)
            cl = billfile.main_dict[l[j]["ID"]]
            tochka = ''
            if not 'PON' in cl['OLT']:
                tochka = '●'
            row.append(telebot.types.InlineKeyboardButton(text=str(l[j]['Address'])+tochka, callback_data=f'get_client={str(l[j]["ID"])}'))
        keyboard.row(*row)  # добавляем кнопки текущей строки в клавиатуру

    return keyboard


def advanceKey(c_id, mid):
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    keyboard.row(
        telebot.types.InlineKeyboardButton('LAN порт', callback_data=f'lan={mid}'),
        #telebot.types.InlineKeyboardButton('MAC таблиця', callback_data=f'mactable={mid}'),
        telebot.types.InlineKeyboardButton('IP адреса', callback_data=f'getip={mid}'),
        telebot.types.InlineKeyboardButton('Рух коштів', callback_data=f'gobalans={mid}')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Зняти з паузи', callback_data=f'clientrun={mid}'),
        telebot.types.InlineKeyboardButton('На паузу', callback_data=f'clientstop={mid}'),
        
    )
    if c_id in ADMINS:
        keyboard.row(
            telebot.types.InlineKeyboardButton('⟲ ONU', callback_data=f'rebootonu={mid}'),
            telebot.types.InlineKeyboardButton('⟲ Mikrotik', callback_data=f'rebootrouter={mid}'),
            telebot.types.InlineKeyboardButton('✖ ONU', callback_data=f'deleteonu={mid}'),
            telebot.types.InlineKeyboardButton('★ WiFi', callback_data=f'wifipass={mid}'),
        )
    return keyboard

def citiesKey(lit):
    keyboard = telebot.types.InlineKeyboardMarkup()
    l = billfile.getCities(lit)
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(l), 4):  # перебираем элементы списка по 5 штук
        row = []  # создаем пустой список для кнопок текущей строки
        for j in range(i, min(i+4, len(l))):  # перебираем элементы строки (не более 5 штук)
            if lit == '':
                row.append(telebot.types.InlineKeyboardButton(text=str(l[j]), callback_data=f'map={str(l[j])}'))
            else:
                row.append(telebot.types.InlineKeyboardButton(text=str(l[j]), callback_data=f'get_street={l[j]}'))
        keyboard.row(*row)  # добавляем кнопки текущей строки в клавиатуру

    return keyboard


def streetKey(lit):
    keyboard = telebot.types.InlineKeyboardMarkup()
    l = billfile.getSitiAll()
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(l), 4):  # перебираем элементы списка по 5 штук
        row = []  # создаем пустой список для кнопок текущей строки
        for j in range(i, min(i+4, len(l))):  # перебираем элементы строки (не более 5 штук)
            if lit == '':
                row.append(telebot.types.InlineKeyboardButton(text=str(l[j]), callback_data=f'map={str(l[j])}'))
            else:
                row.append(telebot.types.InlineKeyboardButton(text=str(l[j]), callback_data=f'get_street={l[j]}'))
        keyboard.row(*row)  # добавляем кнопки текущей строки в клавиатуру

    return keyboard
