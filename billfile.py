import regex as re
import kassa
from config import *
# Создаем пустой основной словарь
main_dict = {}


def read(s):
    global main_dict
    kassa.login()
    temp_dict = kassa.getClients(s)
    #print(temp_dict)
    for i in temp_dict.keys():
        main_dict[i] = temp_dict[i]


def find(s):
    read(s)
    if s in main_dict:
        return s
    for record in main_dict.values():
        if s.lower() in record['Name'].lower():
            return record['ID']
    for record in main_dict.values():
        if s.lower() in record['Address'].lower():
            return record['ID']
    for record in main_dict.values():
        if s.lower() in record['Phone'].lower():
            return record['ID']
    for record in main_dict.values():
        if s.lower() in record['MAC'].lower():
            return record['ID']
    return ''

def findAll(s):
    read(s)
    d = dict()
    if s in main_dict:
        d[s] = ''
        return d
    for record in main_dict.values():
        if s.lower() in record['Name'].lower():
            d[record['ID']] = record['Name']
    if len(d)>0:
        return d
    
    for record in main_dict.values():
        if s.lower() in record['Address'].lower():
            d[record['ID']] = record['Address']
    if len(d)>0:
        return d
    
    for record in main_dict.values():
        if s.lower() in record['Phone'].lower():
            d[record['ID']] = record['Phone']
    if len(d)>0:
        return d
    
    for record in main_dict.values():
        if s.lower() in record['MAC'].lower():
            d[record['ID']] = record['MAC']
    
    return d

def neighbours(c_id):
    ad = main_dict[c_id]['Address']
    ad = ad.split(',')
    ad = ad[0:-1]
    sta = ','.join(ad)
    read(sta)
    l = list()
    for i in main_dict.values():
        if (sta in i['Address']) and (main_dict[c_id]['Address']!=i['Address']):
            ai = i['Address'].split(',')[-1]
            l.append({'ID': i['ID'], 'Address': ai})
    try:
        l.sort(key=lambda x: int(x['Address']))
    except:
        l.sort(key=lambda x: x['Address'])
    return l

def getStreet(c_id):
    ad = main_dict[c_id]['Address']
    ad = ad.split(',')
    ad = ad[0:-1]
    return ','.join(ad)

def getPPPoEPass(c_id):
    kassa.login()
    return kassa.getpppoePass(c_id)

def getCities(lit):
    s = set()
    for i in main_dict.values():
        if (lit!=''):
            a = i['Address'].split(',')[0]
            if lit in a:
                s.add(a)
        elif lit in i['Address'].split(',')[0]:
            a = i['Address'].split(',')[0]
            if a == '':
                continue
            match = re.search(r'(?<=\s|^)[\p{Lu}І](?=[^\sІ])', a, re.U)
            mm = str(match.group(0))
            if mm != '':
                s.add(mm)
    return list(s)

def getStreetAll(siti):
    s = set()
    for i in main_dict.values():
        a = i['Address'].split(',')
        if (a!='') and (siti in a[0]):
            s.add(a[1])
    return list(s)

def getStreetLit(l):
    s = set()
    for i in l:
        a = i.split(',')[1]
        if a == '':
            continue
        match = re.search(r'(?<=\s|^)[\p{Lu}І](?=[^\sІ])', a, re.U)
        mm = str(match.group(0))
        if mm != '':
            s.add(mm)
    return list(s)

