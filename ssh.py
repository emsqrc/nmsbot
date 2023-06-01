import paramiko
from config import *
import re


def parse_data(text):
    l = text.split('\n')
    lh = list()
    lb = list(list())
    for i in l:
        if 'Columns:' in i:
            i = i.replace(',','')
            tl = i.strip().split(' ')
            lh = tl[1:]
        elif (not '#' in i) and (not 'Flags:' in i) and (i != ''):
            i = i.replace(',','')
            tl = i.strip().split(' ')
            ll = list()
            for j in tl:
                if j!='':
                    ll.append(j)
            lb.append(ll)
    lb = lb[:10]
    s = ''
    for i in lb:
        if len(i)>0:
            try:
                s=s+f'{i[1]} {i[2]} {i[3]} {i[4]}\n'
            except:
                s=s+f'{i[1]} {i[2]} {i[3]}\n'
    return s


def connect(ip):
    # создаем объект SSHClient
    ssh = paramiko.SSHClient()
    # устанавливаем политику подключения (принимаем все ключи)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # подключаемся к удаленному серверу
    ssh.connect(hostname=ip, username=USERNAMESSH, password=PASSWORDSSH, timeout=3)
    return ssh

def getBsInfo(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/interface wireless registration-table print stats')
    # выводим результат
    r = stdout.read().decode()
    # создать паттерн для поиска ключ-значение пар
    pattern = r'(\w[\w-]*\w)=(?:"([^"]*)"|(\S*))'
    # извлекаем данные из строки с помощью findall
    l = re.findall(pattern, r)
    ll = list()
    for i in l:
        a = list()
        for j in i:
            if j!='':
                a.append(j)
        ll.append(a)
    d = dict()
    for i in ll:
        d[i[0]] = i[1]
    # закрываем соединение
    ssh.close()
    return d


def getEtherInfo(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/interface ethernet print detail where name=ether1')
    # выводим результат
    r = stdout.read().decode()
    d = dict()
    # Ищем флаг
    flag_match = re.search(r'\s*\d+\s+(R|S|X)', r)
    if flag_match:
        flag = flag_match.group(1)
    else:
        flag = ''
    # Ищем скорость
    speed_match = re.search(r'speed=([\d]+\S+)', r)
    if speed_match:
        speed = speed_match.group(1)
    else:
        speed = ''
    d['flag'] = flag
    d['speed'] = speed
    # закрываем соединение
    ssh.close()
    return d

def getLease(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/ip dhcp-server lease print')
    # выводим результат
    r = stdout.read().decode()
    r =parse_data(r)
    # закрываем соединение
    ssh.close()
    return r

def getLeaseAndEtherInfo(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/interface ethernet print detail where name=ether1')
    # выводим результат
    r = stdout.read().decode()
    d = dict()
    # Ищем флаг
    flag_match = re.search(r'\s*\d+\s+(R|S|X)', r)
    if flag_match:
        flag = flag_match.group(1)
    else:
        flag = ''
    # Ищем скорость
    speed_match = re.search(r'speed=([\d]+\S+)', r)
    if speed_match:
        speed = speed_match.group(1)
    else:
        speed = ''
    d['flag'] = flag
    d['speed'] = speed

    stdin, stdout, stderr = ssh.exec_command('/ip dhcp-server lease print')
    # выводим результат
    r = stdout.read().decode()
    r =parse_data(r)
    # закрываем соединение
    ssh.close()
    return d, r

def get_passphrase(text):
    try:
        pattern = r'passphrase="(\w+)"'
        match = re.search(pattern, text)
        if match:
            return match.group().split('=')[1].replace('"','')
        else:
            return ""
    except:
        return ""
    
def get_passphrase2(text):
    try:
        pattern = r'wpa2-pre-shared-key="(\w+)"'
        match = re.search(pattern, text)
        if match:
            return match.group().split('=')[1].replace('"','')
        else:
            return ""
    except:
        return ""


def getWifiPass(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/caps-man security print')
    # выводим результат
    r = stdout.read().decode()
    r = get_passphrase(r)
    r2 = ''
    if r == '':
        stdin, stdout, stderr = ssh.exec_command('/interface wireless security-profiles print')
        r2 = stdout.read().decode()
        r2 = get_passphrase2(r2)
    # закрываем соединение
    ssh.close()
    return f'{r}\n{r2}'

def reboot(ip):
    ssh = connect(ip)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command('/system reboot')
    # выводим результат
    r = stdout.read().decode()
    # закрываем соединение
    try:
        ssh.close()
    except:
        pass


def createForwardToClient(ip,port):
    # создаем объект SSHClient
    ssh = paramiko.SSHClient()
    # устанавливаем политику подключения (принимаем все ключи)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # подключаемся к удаленному серверу
    ssh.connect(hostname=IPA, username=USERA, password=PASSA, timeout=3)
    # выполняем команду и получаем ее вывод
    stdin, stdout, stderr = ssh.exec_command(f'/ip firewall nat remove [find comment=bot-server]')
    stdin, stdout, stderr = ssh.exec_command(f'/ip firewall nat add chain=dstnat action=dst-nat to-addresses={ip} to-ports={port} protocol=tcp in-interface=pppoe-out1 dst-port=45555 comment=bot-server')
    # выводим результат
    r = stdout.read().decode()
    # закрываем соединение
    ssh.close()
    return '45.155.81.22:45555'
