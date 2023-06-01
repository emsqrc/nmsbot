import nms
import ssh
import billfile
import datetime
from config import *
import time
import pytz
import re

mactoname = dict()

def extract_mac_addresses(text):
    mac_pattern = r'[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}'  # Регулярное выражение для поиска MAC-адресов
    mac_addresses = re.findall(mac_pattern, text)  # Поиск всех совпадений
    return mac_addresses

def readmacbase():
    global mactoname
    with open('ouic.txt', 'r', encoding='utf8') as f:
        for i in f:
            l = i.split('=')
            if len(l)==2:
                mactoname[l[0].lower()] = l[1]

def getNameForMac(macs:str):
    r = macs
    mac = extract_mac_addresses(macs)
    for i in mac:
        m = i.replace('.','').replace(':','').lower()
        m3 = m[:6]
        mn = mactoname.get(m3,'noname').strip()
        n = ' '.join(mn.split(' ')[:1])
        if not f'{i.lower()} {n.lower()}' in r.lower():
            r = r.replace(i,f'{i}   {n}')
    r = r.replace('defconf','')
    return r

def unix_time_to_string(unix_time):
    unix_time = int(unix_time)
    timezone = 'UTC'
    # Преобразование Unix времени в объект datetime
    dt = datetime.datetime.fromtimestamp(unix_time, pytz.timezone(timezone))
    # Форматирование даты и времени в строку
    formatted_string = dt.strftime('%d-%m-%Y %H:%M:%S')
    return formatted_string

def get_elapsed_time(unix_time):
    unix_time = int(unix_time)
    current_time = time.time()
    elapsed_time = current_time - unix_time
    
    # Разбиваем количество секунд на дни, часы, минуты и секунды
    days = elapsed_time // (24 * 3600)
    elapsed_time %= (24 * 3600)
    hours = elapsed_time // 3600
    elapsed_time %= 3600
    minutes = elapsed_time // 60
    elapsed_time %= 60
    seconds = elapsed_time
    
    # Формируем строку с прошедшим временем
    time_string = f"{int(days)}d {int(hours)}:{int(minutes)}:{int(seconds)}"
    
    return time_string


def printLog(*arg):
    print(*arg)
    with open('log.txt','a') as f:
        for i in arg:
            f.write(f'{i} ')
        f.write('\n')


def strDataTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def clientStateToStr(client_data):
    state = ''
    if client_data['Online'] == '1':
        state = 'Онлайн'
    else:
        state = 'Оффлайн'
    if int(time.time())<int(client_data['Stop']):
        if client_data['Run'] == '1':
            state = state + ' ▶️'
        else:
            state = state + ' ⏸️'
    else:
        state = state + ' ⏹️'
    return state

def formatRequest(c_id):
    r = ''
    try:
        client_data = billfile.main_dict[c_id]
        state = clientStateToStr(client_data)
        r = f'*{client_data["ID"]}*   _{state}_\n{client_data["Name"]}\n{client_data["Phone"]}\n{client_data["Address"]}\n{client_data["Speed"]}\n{client_data["Balance"]} грн.'
        if 'PON' in client_data["OLT"]:
            if client_data["MAC"] !='':
                if 'EPON' in client_data["OLT"]:
                    ep = nms.getInfoForMac(client_data["MAC"], False)
                else:
                    ep = nms.getInfoForMac(client_data["MAC"], True)
                r+='\n'+'\n'.join(ep)
                r+=f'\n{client_data["MAC"]}'
        else:
            bs = ssh.getBsInfo(client_data["IP"])
            r += f'\n{bs.get("radio-name", "")}\nСигнал: {bs.get("signal-strength", "")}\n{bs.get("rx-rate", "")}\nCCQ: {bs.get("tx-ccq", "")} {bs.get("rx-ccq", "")}\nАптайм: {bs.get("uptime", "")}'
        return r
    except:
        return r+"\nПомилка"

def updateSignal(c_id):
    r = ''
    try:
        client_data = billfile.main_dict[c_id]
        if 'PON' in client_data["OLT"]:
            if 'EPON' in client_data["OLT"]:
                ep = nms.getInfoForMac(client_data["MAC"], False)
                ep = ep[2:4]
            else:
                ep = nms.getInfoForMac(client_data["MAC"], True)
                ep = ep[1:2]
            r+='\n'+'\n'.join(ep)
        else:
            bs = ssh.getBsInfo(client_data["IP"])
            r+=f'{bs["signal-strength"]}\n{bs["rx-rate"]}\nCCQ: {bs["tx-ccq"]} {bs["rx-ccq"]}'
        return r
    except:
        return r+"\nПомилка"
    
def checkUser(id):
    if id in WORKERNAME.keys():
        return True
    else:
        return False
    


