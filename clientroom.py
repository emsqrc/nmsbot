import requests
from bs4 import BeautifulSoup


headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://my.novanet.in.ua/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }


def login(username: str, password: str) -> requests.Session:
    session = requests.Session()

    # Адрес страницы входа и POST параметры
    url = 'https://my.novanet.in.ua/login.php'
    data = {'login': username, 'pass': password, 'go': 'Ввійти'}

    # Отправляем POST запрос на страницу входа
    response = session.post(url, data=data, headers=headers)

    # Проверяем статус ответа
    if response.status_code != 200:
        raise Exception('Failed to log in')
    #print(response.text)
    return session


def parse_tariffs(form_html):
    soup = BeautifulSoup(form_html, 'html.parser')
    tariffs = {}
    for tariff in soup.find_all('div', class_='m2'):
        tariff_input = tariff.find('input')
        tariff_id = tariff_input['value']
        tariff_name = tariff.find('label').text.strip()
        tariff_transition_cost = tariff.find('i').text.strip().replace('(переход - ', '').replace(' Грн.)', '')
        tariffs[tariff_id] = {'name': tariff_name, 'transition_cost': tariff_transition_cost}
    return tariffs

def getTarifInfo(session, tarifid):
    url = f'https://my.novanet.in.ua/api.php?action=GETGROUPDESCRIPTION&value={tarifid}'
    # Отправляем GET запрос 
    response = session.get(url, headers=headers)

    # Проверяем статус ответа
    if response.status_code != 200:
        raise Exception('Failed to log in')
    return response.text 

def getTarif(session):
    url = f'https://my.novanet.in.ua/changetarif.php'
    # Отправляем GET запрос 
    response = session.get(url, headers=headers)

    # Проверяем статус ответа
    if response.status_code != 200:
        raise Exception('Failed to log in')
    return parse_tariffs(response.text)

def change_tariff(session, tariff_id):
    url = "https://my.novanet.in.ua/changetarif.php"
    data = {"tarif": tariff_id, "name": "go"}
    response = session.post(url, data=data, headers=headers)
    return response.text



def extract_payments(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='payments')
    rows = table.find_all('tr')[1:] # пропускаем заголовок таблицы

    payments = []
    for row in rows:
        cols = row.find_all('td')
        payment = {
            'Дата': cols[0].text.strip(),
            'Тип операции': cols[1].find('i')['class'][1],
            'Сума': cols[2].text.strip(),
            'Баланс': cols[3]['data-html'] + cols[3].text.strip(),
            'Примечание': cols[4].text.strip()
        }
        payments.append(payment)

    return payments

def format_payments(payments):
    rows = []
    for payment in payments[:30]:
        if not '-' in payment['Сума']:
            row = f"*{payment['Дата']}   {payment['Сума']}   {payment['Примечание']}*"
        else:
            row = f"{payment['Дата']}   {payment['Сума']}   {payment['Примечание']}"
        rows.append(row)
    return "\n".join(rows)


def getPayment(session):
    url = "https://my.novanet.in.ua/payments.php"
    response = session.post(url, headers=headers)
    return format_payments(extract_payments(response.text))

def Payment(user,passwd):
    s = login(user,passwd)
    return getPayment(s)

import re

def extract_sum(text):
    pattern = r'(\d+)\s*Грн\.'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    else:
        return 0


def Tarifs(user,passwd):
    s = login(user,passwd)
    d = getTarif(s)
    dd = dict()
    for i in d.keys():
        dd[d[i]['name']] = extract_sum(getTarifInfo(s,i))
    str = ''
    for i in dd.keys():\
        str = str + f"{i}   {dd[i]} грн\n"
    return str
