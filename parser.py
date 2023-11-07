import requests
from bs4 import BeautifulSoup
import pandas as pd

index = {
    "Title": 0,
    "Price": 1,
    "Город": 2,
    "Комнаты": 3,
    "В залоге": 4,
    "Тип дома": 5,
    "Жилой комплекс": 6,
    "Год постройки": 7,
    "Этаж": 8,
    "Площадь, м²": 9,
    "Бывшее общежитие": 10,
    "Состояние": 11,
    "Телефон": 12,
    "Интернет": 13,
    "Санузел": 14,
    "Балкон": 15,
    "Балкон остеклён": 16,
    "Дверь": 17,
    "Парковка": 18,
    "Квартира меблирована": 19,
    "Пол": 20,
    "Потолки": 21,
    "Безопасность": 22,
    "Разное": 23,
    "Возможен обмен": 24
}

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', {"class":"a-card__title"}):
        links.append('https://krisha.kz' + a['href'])

    return links

def parse_page(url):
    page = requests.get(url)
    html = page.content
    data = [None]*25
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('div',{'class':"offer__parameters-mortgaged"}):
        data[index["В залоге"]] = True
    else:
        data[index["В залоге"]] = False

    parameters = soup.find("div", {"class":"offer__parameters"}).find_all("dl")
    for parameter in parameters:
        attr = parameter.find('dt').text.strip()
        if attr in index:
            data[index[attr]] = parameter.find('dd').text
    return data

url = 'https://krisha.kz/prodazha/kvartiry/almaty/?page=1'
links = get_links(url)

rows = []
for link in links:
    row = parse_page(link)
    rows.append(row)

columns = [
    "Title", "Price", "Location", "Rooms", "Bail", "TypeOfBuilding", "ResidentialComplex",
    "YearBuilt", "Floor", "Area", "PreviouslyDorm", "Conditions", "Phone",
    "Internet", "Bathroom", "Balcony", "BalconyIsGlazed", "Door", "Parking",
    "Furnished", "Flooring", "CeilingHeight", "Security", "Miscellaneous","ExchangePossible"
]
df = pd.DataFrame(rows, columns=columns)


df.to_csv("krisha.csv")
