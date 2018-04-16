from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import csv


filename = 'data_atelier_vladimir.csv'

urls = ("https://start33.ru/companies/service/atelier?page=1", "https://start33.ru/companies/service/atelier?page=2")
cards = []
for url in urls:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'xml')
    for i in soup.find_all(href=re.compile("/company/")):
        card = i.attrs["href"]
        cards.append(card)


for card in cards:
    data = []
    html = urlopen("https://start33.ru"+card)
    soup = BeautifulSoup(html, "lxml")
    try:
        name = soup.find("h1").get_text()
        data.append(name)
    except Exception:
        data.append('name error')
    try:
        adress = soup.find('div', {'class': 'com_item__adr_text'}).find('a').get_text()
        data.append(adress)
    except Exception:
        data.append('adress error')
    try:
        phones = soup.find_all(href=re.compile("tel:"))
        data_phones = []
        for phone in phones:
            data_phones.append(phone.get_text())
        data.append(data_phones)
    except Exception:
        data_phones.append('phone error')
    try:
        worktime = soup.find("div", {"class": "working_mode"})
        data_work = []
        for item in worktime:
            if type(item) is NavigableString:
                data_work.append(item.strip())
        data.append(data_work)
    except Exception:
        try:
            data_work = []
            worktime = []
            days = ['Пн: ', 'Вт: ', 'Ср: ', 'Чт: ', 'Пт: ', 'Сб: ', 'Вс: ']
            for td in soup.find_all('td'):
                time = []
                for div in td.find_all('div'):
                    if div != ' ':
                        time.append(div.text.strip())
                    if div.find('i', {'class': 'i_icon i_icon-block'}):
                        time.append('Выходной')
                if time != []:
                    worktime.append(time)

            for day, time in dict(zip(days, worktime)).items():
                if 'Выходной' not in time:
                    data_work.append('{0}{1}'.format(day, ' - '.join(time)))
                else:
                    data_work.append('{0}{1}'.format(day, time[1]))
        except Exception:
            data_work.append('worktime error')
        data.append(data_work)
    try:
        html = urlopen("https://start33.ru" + card + '/map')
        soup = BeautifulSoup(html, 'xml')
        coord = soup.find('script', src='https://api-maps.yandex.ru/2.1/?lang=ru-RU').find_next('script').text
        num = re.findall('\[\d.*\d\]', coord)
        data.append('Координаты : '+num[0])
    except Exception:
        data.append('map error')
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
print('gotovo bldjad')
