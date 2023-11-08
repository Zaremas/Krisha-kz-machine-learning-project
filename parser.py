import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

columns = [
        "Title", "Price", "Location", "Rooms", "Bail", "TypeOfBuilding", "ResidentialComplex",
        "YearBuilt", "Floor", "Area", "PreviouslyDorm", "Conditions", "Phone",
        "Internet", "Bathroom", "Balcony", "BalconyIsGlazed", "Door", "Parking", "Furnished",
        "Flooring", "CeilingHeight", "Security", "Miscellaneous","ExchangePossible", "Description"
    ]

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
    "Возможен обмен": 24,
    "Oписание": 25
}

def get_links(soup):
    links = []
    for a in soup.find_all('a', {"class":"a-card__title"}):
        links.append('https://krisha.kz' + a['href'])

    return links

def parse_page(url):
    page = requests.get(url)
    html = page.content
    data = [None]*26
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='offer__advert-title').h1.text.strip()
    data[index["Title"]] = title

    price = soup.find(['div','p'], class_='offer__price').contents[0].text.strip()
    data[index["Price"]] = price

    parameters1 = soup.find_all("div", {"class":"offer__info-item"})
    for parameter in parameters1:
        attr = parameter.find("div", {"class":"offer__info-title"}).text.strip()
        if attr in index:
            data[index[attr]] = parameter.find('div',{"class":"offer__advert-short-info"}).contents[0].text

    if soup.find('div',{'class':"offer__parameters-mortgaged"}):
        data[index["В залоге"]] = True
    else:
        data[index["В залоге"]] = False

    parameters2 = soup.find("div", {"class":"offer__parameters"}).find_all("dl")
    for parameter in parameters2:
        attr = parameter.find('dt').text.strip()
        if attr in index:
            data[index[attr]] = parameter.find('dd').text

    if soup.find('div',{'class':"a-text a-text-white-spaces"}):
        data[index["Oписание"]] = soup.find('div',{'class':"a-text a-text-white-spaces"}).text

    #print('finished a row')
    return data



url = 'https://krisha.kz/prodazha/kvartiry/almaty/?page=1'
rows = []

#limit = 10
page_counter=1

while True:
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = get_links(soup)

    for link in links:
        row = parse_page(link)
        rows.append(row)
        time.sleep(1)

    next_page_url = soup.find("a", {"class": "paginator__btn--next"})

    print("page done:", page_counter)

    if next_page_url:
        url = "https://krisha.kz"+next_page_url["href"]
    else:
        break

    #if page_counter == limit:
    #    break

    page_counter+=1

df = pd.DataFrame(rows, columns=columns)
df.to_csv("krisha.csv")
