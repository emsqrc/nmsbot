
import telebot
from config import *
from backend import *
from keybord import *
from mem import *
import kassa
import clientroom


billfile.read('')
printLog('-'*25,'loaded...','-'*25)
wmem = mem()
readmacbase()

while True:
    try:
        # Создаем экземпляр бота
        bot = telebot.TeleBot(TOKEN)
        def askUser(text,id):
            if checkUser(id):
                printLog(strDataTime(),WORKERNAME[id],text)
                d = billfile.findAll(text)
                if len(d.keys())>1:
                    m = bot.send_message(id, f'Всього збігів *{len(d.keys())}*',parse_mode= "Markdown", reply_markup=selectClientKey(d)) 
                    return
                if len(d.keys()) != 0:
                    c_id = list(d.keys())[0] 
                    str = formatRequest(c_id)
                    m = bot.send_message(id, str,parse_mode= "Markdown",reply_markup=menuKey(c_id))
                    wmem.addClient(id,c_id)
                else:
                    str = 'Не знайдено'
                    bot.send_message(id, str,parse_mode= "Markdown")
            else:
                bot.send_message(id, NOACCESSLIST,parse_mode= "Markdown")

        # Функция, обрабатывающая команду /start
        @bot.message_handler(commands=["start"])
        def start(m, res=False):
            #loggedIdWorker(m.chat.id)
            if checkUser(m.chat.id):
                bot.send_message(m.chat.id, HELLOMSG)
                printLog(strDataTime(),WORKERNAME[m.chat.id])
            else:
                printLog(strDataTime(),m.chat.id)
                bot.send_message(m.chat.id, NOACCESSLIST,parse_mode= "Markdown")
        
        # Функция, обрабатывающая команду /help
        @bot.message_handler(commands=["h"])
        def help(m, res=False):
            if checkUser(m.chat.id):
                tx = m.text
                tx = tx.replace('/h', '')
                str = "/f порт\n"
                bot.send_message(m.chat.id, str)
                printLog(strDataTime(),WORKERNAME[m.chat.id],'help')
            else:
                printLog(strDataTime(),m.chat.id)
                bot.send_message(m.chat.id, NOACCESSLIST,parse_mode= "Markdown")


        

        # Функция, обрабатывающая команду /f
        @bot.message_handler(commands=["f"])
        def forw(m, res=False):
            if checkUser(m.chat.id):
                tx = m.text
                tx = tx.replace('/f', '')
                cid = wmem.getClient(m.chat.id)
                cl = billfile.main_dict[cid]
                ip = cl['IP']
                if tx!='':
                    port = tx
                else:
                    port = '8291'
                str = f"*{cl['ID']}* {ssh.createForwardToClient(ip,port)}"
                bot.send_message(m.chat.id, str, parse_mode= "Markdown")
                printLog(strDataTime(),WORKERNAME[m.chat.id],cl['ID'],'forward')
            else:
                printLog(strDataTime(),m.chat.id)
                bot.send_message(m.chat.id, NOACCESSLIST,parse_mode= "Markdown")

        # Получение сообщений от юзера
        @bot.message_handler(content_types=["text"])
        def handle_text(message):
                askUser(message.text,message.chat.id)
                nms.closeTelnetClient()

        # Обработчик нажатий на кнопки
        @bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            l = call.data.split('=')
            if l[0] == 'update_signal':
                str = updateSignal(l[1])
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'get_client':
                askUser(l[1],call.message.chat.id)
            elif l[0] == 'neighbours_key':
                bot.send_message(call.message.chat.id,billfile.getStreet(l[1]),parse_mode= "Markdown",reply_markup=neighboursKey(l[1]))
            elif l[0] == 'pppoe_pass':
                str = billfile.getPPPoEPass(l[1])
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'map':
                str = 'Селища'
                if l[1] =='_':
                    bot.send_message(call.message.chat.id, str, reply_markup=citiesKey(''))
                else:
                    bot.send_message(call.message.chat.id, str, reply_markup=citiesKey(l[1]))
            elif l[0] == 'get_street':
                str = l[1]
                wmem.addMemorySiti(call.message.chat.id,l[1])
                bot.send_message(call.message.chat.id, str, reply_markup=streetKey(''))
            elif l[0] == 'lan':
                client_data = billfile.main_dict[l[1]]
                str = ''
                str2 = ''
                if 'PON' in client_data["OLT"]:
                    if 'EPON' in client_data["OLT"]:
                        str = nms.getChassis(client_data['MAC'],False)
                        str2 = nms.getMacTable(client_data['MAC'],False)
                    else:
                        str = nms.getChassis(client_data['MAC'],True)
                        str2 = nms.getMacTable(client_data['MAC'],True)
                else:
                    d, str2 = ssh.getLeaseAndEtherInfo(client_data['IP'])
                    if d['flag']=='R':
                        str = f"On {d.get('speed','')}"
                    else:
                        str = 'Off'
                str2 = getNameForMac(str2)
                bot.send_message(call.message.chat.id, str+'\n'+str2)
            elif l[0] == 'advancekey':
                bot.send_message(call.message.chat.id, f'Додаткові функції *{l[1]}*',parse_mode= "Markdown",reply_markup=advanceKey(call.message.chat.id, l[1]))
            elif l[0] == 'mactable':
                client_data = billfile.main_dict[l[1]]
                str = ''
                if 'PON' in client_data["OLT"]:
                    if 'EPON' in client_data["OLT"]:
                        str = nms.getMacTable(client_data['MAC'],False)
                    else:
                        str = nms.getMacTable(client_data['MAC'],True)
                else:
                    str = ssh.getLease(client_data['IP'])
                if str=='':
                    str = 'немає'
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'clientrun':
                client_data = billfile.main_dict[l[1]]
                kassa.clientRun(client_data['ID'])
                bot.send_message(call.message.chat.id, 'Знято з паузи')
            elif l[0] == 'clientstop':
                client_data = billfile.main_dict[l[1]]
                kassa.clientStop(client_data['ID'])
                bot.send_message(call.message.chat.id, 'Поставлено на паузу')
            elif l[0] == 'getip':
                client_data = billfile.main_dict[l[1]]
                str = client_data['IP']
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'gobalans':
                client_data = billfile.main_dict[l[1]]
                user = client_data['ID']
                bot.send_message(call.message.chat.id, 'Завантаження...')
                psw = kassa.getpppoePass(user)
                str = clientroom.Payment(user,psw)
                bot.send_message(call.message.chat.id, str, parse_mode= "Markdown")
            elif l[0] == 'uptime':
                client_data = billfile.main_dict[l[1]]
                str = unix_time_to_string(client_data['Uptime'])+'   '+get_elapsed_time(client_data['Uptime'])
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'wifipass':
                client_data = billfile.main_dict[l[1]]
                try:
                    str = ssh.getWifiPass(client_data['IP']).strip()
                except:
                    str = ''
                if str == '':
                    str = 'Ця функція працює тільки для mikrotik'
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'routerreboot':
                cl = billfile.main_dict[l[1]]
                try:
                    ssh.reboot(cl['IP'])
                    str = 'Перезавантаження...'
                    bot.send_message(call.message.chat.id, str)
                except:
                    str = 'Помилка'
                    bot.send_message(call.message.chat.id, str)
            elif l[0] == 'rebootonu':
                cl = billfile.main_dict[l[1]]
                try:
                    if 'EPON' in cl["OLT"]:
                        g = False
                    else:
                        g = True
                    str = nms.rebootOnu(cl['MAC'], g)
                except:
                    str = 'Помилка'
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'rebootrouter':
                cl = billfile.main_dict[l[1]]
                try:
                    if 'EPON' in cl["OLT"]:
                        g = False
                    else:
                        g = True
                    str = nms.rebootOnu(cl['MAC'], g)
                except:
                    str = 'Помилка'
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'rebootrouter':
                cl = billfile.main_dict[l[1]]
                try:
                    if 'EPON' in cl["OLT"]:
                        g = False
                    else:
                        g = True
                    str = nms.rebootOnu(cl['MAC'], g)
                except:
                    str = 'Помилка'
                bot.send_message(call.message.chat.id, str)
            elif l[0] == 'deleteonu':
                cl = billfile.main_dict[l[1]]
                try:
                    if 'EPON' in cl["OLT"]:
                        g = False
                    else:
                        g = True
                    str = nms.deleteOnu(cl['MAC'], g)
                except:
                    str = 'Помилка'
                bot.send_message(call.message.chat.id, str)
            printLog(strDataTime(),WORKERNAME[call.message.chat.id],l[0],l[1])


        # Запускаем бота
        bot.polling(none_stop=True, interval=0)
    except:
        printLog('-'*25,strDataTime(),'-'*25)

