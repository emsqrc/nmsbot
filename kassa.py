import re
import requests
from config import *

SECRETKEY = ''

session = requests.Session()

headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://my.novanet.in.ua/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def login():
    url = 'https://my.novanet.in.ua/kassa/index.php'
    login_data = {
        'chaiserlogin': KASSALOGIN,
        'chaiserpassword': KASSAPASS,
        'remember': 'remember',
        'submit': 'Увійти'
    }
    r = session.post(url, data=login_data, headers=headers)
    global SECRETKEY
    if SECRETKEY == '':
        l = str(r.text).split('\n')
        for i in l:
            if 'api.php?action=CASHIER_ACTIVITY&secret=' in i:
                secret = re.search(r'secret=(\d+)', str(i)).group(1)
                SECRETKEY = secret
                break
    url = f"https://my.novanet.in.ua/kassa/api.php?action=SEND_OUT_COMMAND&value=USER_COLUMNS_{SECRETKEY}&value2=" + U
    r = session.post(url, headers=headers)
    
def getClients(c):
    url = 'https://my.novanet.in.ua/kassa/api.php?action=finduser2&value='+str(c)
    r = session.get(url, headers=headers)
    l = str(r.text).replace("`","'").split('-*-')
    d = dict()
    for i in l:
        ll = i.split('||')
        if len(ll)>2:
            #print(ll)
            d[ll[1]] = {'dbID': ll[0], 'ID': ll[1],'Speed': ll[2],'Balance': ll[3],'IP': ll[4],'Name': ll[6], 'Phone': ll[7], 'Mode': ll[8], 'Run': ll[9], 'Online': ll[10], 'Down': ll[22],'Up': ll[23], 'Uptime': ll[24], 'Address': ll[27], 'OLT': ll[29], 'Model': ll[30], 'Port': ll[31], 'MAC': ll[32], 'Stop':ll[37], 'Plata': ll[41]}
    return d    
'''
login()
getClients('10035')
'''

def getpppoePass(c):
    url = 'https://my.novanet.in.ua/kassa/settarif.php?client='+str(c)
    r = session.get(url, headers=headers)
    p = ''
    # Печатаем текст и адрес каждой ссылки
    l = r.text.split('\n')
    for link in l:
        s = str(link)
        if 'AccountsBase.push(new AccountInfo(' in s:
            p = s.split(',')[1].replace("'",'')
            break
    return p
    


def clientStop(cid):
    url = 'https://my.novanet.in.ua/kassa/onoffclient.php?off=1&client='+str(cid)
    r = session.get(url,headers=headers)

def clientRun(cid):
    url = 'https://my.novanet.in.ua/kassa/onoffclient.php?off=0&client='+str(cid)
    r = session.get(url,headers=headers)

