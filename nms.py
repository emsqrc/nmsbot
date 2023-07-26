import requests
import json
from config import *

session = requests.Session() # Создаем экземпляр сессии
def login():
    url = 'http://10.0.0.15:8888/login'
    payload = {
        'userName': NMSLOGIN,
        'password': NMSPASS,
        'commandName': 'loginForm'
    }
    r = session.post(url, data=payload)  # Отправляем POST-запрос
    #print(r.status_code)  # Проверяем статус-код ответа

def encode_mac(mac):
    mac = mac.replace(' ','')
    mac_address = mac
    # удаление точек из мак-адреса
    mac_address = mac_address.replace(".", "")
    # добавление "+" после каждых двух символов
    mac_address = "+".join([mac_address[i:i+2] for i in range(0, len(mac_address), 2)])
    return mac_address

def encode_mac_gpon(mac):
    mac = mac.replace(' ','')
    mac_address = mac
    # удаление точек из мак-адреса
    mac_address = mac_address.replace(':','%3A')
    return mac_address

def closeTelnetClient():
    url = 'http://10.0.0.15:8888/config/telnet/closeTelnetClient'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = session.post(url, headers=headers)

def get_moid_epon(mac):
    # Запрос
    url = f'http://10.0.0.15:8888/topoManagement/getDeviceListByArea?sEcho=2&iColumns=11&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=20&mDataProp_0=moid&mDataProp_1=&mDataProp_2=mac&mDataProp_3=&mDataProp_4=&mDataProp_5=&mDataProp_6=type&mDataProp_7=belongOlt&mDataProp_8=belongPon&mDataProp_9=loid&mDataProp_10=&name=&cMoId=-1&cMoClass=-2&searchtext=undefined&cAreaId=-2&areaId=&type=EponONUDevice&IPType=precision&Ip=&nameType=precision&deviceMoName=&disType=fuzzy&displayname=&macType=fuzzy&mac={encode_mac(mac)}&loidType=precision&loid=&flag=true&status=&deviceModel=&deviceModelType=&vendorId=&vendorIdType=&modelId=&modelIdType=&_=1682019896419'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        # Обработка успешного ответа
        data = response.text
        #print('========',data,'===========')
        parsed_data = json.loads(data)
        moid = parsed_data["aaData"][0]["moid"]
        name = parsed_data["aaData"][0]["name"]
        classname = parsed_data["aaData"][0]["classname"]
        dispname = parsed_data["aaData"][0]['displayname']
        status = parsed_data["aaData"][0]['status']
        ctime = parsed_data["aaData"][0]['statusChangeTime']
        return moid, name, classname, dispname, status, ctime
    else:
        # Обработка ошибки
        return ""
    
def get_moid_gpon(mac):
    # Запрос
    url = f'http://10.0.0.15:8888/topoManagement/getDeviceListByArea?sEcho=2&iColumns=11&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=20&mDataProp_0=moid&mDataProp_1=&mDataProp_2=mac&mDataProp_3=&mDataProp_4=&mDataProp_5=&mDataProp_6=type&mDataProp_7=belongOlt&mDataProp_8=belongPon&mDataProp_9=loid&mDataProp_10=&name=&cMoId=-1&cMoClass=-2&searchtext=undefined&cAreaId=-2&areaId=&type=GponONUDevice&IPType=precision&Ip=&nameType=precision&deviceMoName=&disType=fuzzy&displayname=&macType=fuzzy&mac={encode_mac_gpon(mac)}&loidType=precision&loid=&flag=true&status=&deviceModel=&deviceModelType=&vendorId=&vendorIdType=&modelId=&modelIdType=&_=1682075969277'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        # Обработка успешного ответа
        data = response.text
        #print('========',data,'===========')
        parsed_data = json.loads(data)
        moid = parsed_data["aaData"][0]["moid"]
        name = parsed_data["aaData"][0]["name"]
        classname = parsed_data["aaData"][0]["classname"]
        dispname = parsed_data["aaData"][0]['displayname']
        status = parsed_data["aaData"][0]['status']
        ctime = parsed_data["aaData"][0]['statusChangeTime']
        return moid, name, classname, dispname, status, ctime
    else:
        # Обработка ошибки
        return ""
    
def get_info(data):
    url = "http://10.0.0.15:8888/topoManagement/getOnuBasicInfo"
    params = {
        "moid": data[0],
        "moname": data[1],
        "classname": data[2]
    }
    
    response = session.post(url, data=params)
    if response.status_code == 200:
        datastr = response.text
        my_dict = json.loads(datastr)
        return my_dict
    else:
        print("Ошибка выполнения запроса: ", response.status_code)
        return dict()

def get_info_gpon(data):
    url = "http://10.0.0.15:8888/topoManagement/getGponOnuBasicInfo"
    params = {
        "moid": data[0],
        "moname": data[1],
        "classname": data[2]
    }
    response = session.post(url, data=params)
    if response.status_code == 200:
        datastr = response.text
        my_dict = json.loads(datastr)
        return my_dict
    else:
        print("Ошибка выполнения запроса: ", response.status_code)
        return dict()
    
def decodeStatus(s):
    s = str(s)
    onl = ''
    if s == '3':
        onl = '✅'
    elif s == '2':
        onl = '❌'
    elif s == '0':
        onl = '🔵'
    elif s == '4':
        onl = '⚪'
    return onl

def extract_info(info,d):
    #print(d[4])
    onl = decodeStatus(d[4])
    return info['onuExtraPonInfo']['belongOLTName'].split('|')[0]+' '+d[3].split('/')[1]+'\n'+d[5]+'  '+onl,info['onuBasicInfo']['software'].replace('\x00',''),'RX: '+info['onuBasicInfo']['rxPower'],'TX: '+info['onuPonRxPower'],info['onuConfigInfo'][0]

def extract_info_gpon(info,d):
    #print(d)
    onl = decodeStatus(d[4])
    return info['onuExtraPonInfo']['belongOLTName'].split('|')[0]+' '+d[3].split('/')[1]+'\n'+d[5]+'  '+onl,'RX: '+info['onuInfos'][7]

def getInfoForMac(mac,gpon):
    login()
    if gpon:
        d = get_moid_gpon(mac)
        info = get_info_gpon(d)
        einfo = extract_info_gpon(info,d)
    else:
        d = get_moid_epon(mac)
        info = get_info(d)
        einfo = extract_info(info,d)
    return einfo

def getChassis(mac,gpon):
    login()
    if gpon:
        d = get_moid_gpon(mac)
        p = get_portPolling(d)
    else:
        d = get_moid_epon(mac)
        p = get_portPolling(d)
    if p[0] == '1':
        return 'On'
    else:
        return 'Off'

def get_portPolling(data):
    
    url = "http://10.0.0.15:8888/topoManagement/portPolling"
    datap = {
    "moid": data[0],
    "classname": data[2],
    "devname": "ONU_1GE",
    "shelfName": "1GE",
    "snmp": '{"ip":"'+data[1].split('-')[0]+'","netmask":"255.255.255.0","community":"nms","version":"v2","port":161,"moName":"10.0.0.125-EPON","writeCommunity":"nms","timeOut":-1,"enterpriseId":"3320","srcMoInfo":{"moid":661,"name":"10.0.0.125-EPON","classname":"EponOLTDevice","displayName":"EPON-OLT-01 | 10.0.0.125","managed":false,"status":5,"statusPollEnabled":false,"uClass":"com.bdcom.nmsweb.rest.topo.polling.OltStatusUpdate","webNMS":"3320","writeCommunity":"nms","portIfIndex":-1,"ipAddress":"10.0.0.125","snmpport":161,"belongPonPort":"","onuBelongP_Port_Descr_2":"","distance":0,"rxPower":0,"GESize":0,"FESize":0,"onlineTime":0,"offlineTime":0,"pvid":0}}',
    "portType[]": ["1", "2"],
    "hasPower": "false",
}
    
    response = session.post(url, data=datap)
    if response.status_code == 200:
        datastr = response.text
        my_dict = json.loads(datastr)
        return my_dict.get('portInfo')
    else:
        print("Ошибка выполнения запроса: ", response.status_code)
        return list()
    
def get_mactable(data):
    url = f"http://10.0.0.15:8888/topoManagement/obtainOnuDeviceMac?sEcho=1&iColumns=2&sColumns=%2C&iDisplayStart=0&iDisplayLength=-1&mDataProp_0=vlan&mDataProp_1=mac&moid={data[0]}"
    response = session.get(url)
    data_dict = json.loads(response.text)
    str = ''
    l = data_dict['aaData']
    for i in l:
        str =str +i.get('vlan','')+'   '+i.get('mac','')+'\n'
    return str

def get_mactable_gpon(data):
    url = f"http://10.0.0.15:8888/topoManagement/obtainGOnuDeviceMac?sEcho=1&iColumns=2&sColumns=%2C&iDisplayStart=0&iDisplayLength=-1&mDataProp_0=vlan&mDataProp_1=mac&moid={data[0]}"
    response = session.get(url)
    data_dict = json.loads(response.text)
    str = ''
    l = data_dict['aaData']
    for i in l:
        str =str +i.get('vlan','')+'   '+i.get('mac','')+'\n'
    return str


def getMacTable(mac,gpon):
    login()
    if gpon:
        d = get_moid_gpon(mac)
        p = get_mactable_gpon(d)
    else:
        d = get_moid_epon(mac)
        p = get_mactable(d)
    return p

def reboot_onu(data):
    url = "http://10.0.0.15:8888/topoManagement/rebootONU"
    params = {
        "moid": data[0],
        "moname": data[1],
        "classname": data[2]
    }
    
    response = session.post(url, data=params)
    return response.text

def delete_onu(data):
    url = "http://10.0.0.15:8888/topoManagement/deleteOnu"
    params = {
        "moid": data[0],
        "name": data[1],
        "classname": data[2],
        "flag": "true"
    }
    
    response = session.post(url, data=params)
    print(response.text)
    return response.text
    
def rebootOnu(mac,gpon):
    login()
    if gpon:
        d = get_moid_gpon(mac)
        p = reboot_onu(d)
    else:
        d = get_moid_epon(mac)
        p = reboot_onu(d)
    return p

def deleteOnu(mac,gpon):
    login()
    if gpon:
        d = get_moid_gpon(mac)
        p = delete_onu(d)
    else:
        d = get_moid_epon(mac)
        p = delete_onu(d)
    return p