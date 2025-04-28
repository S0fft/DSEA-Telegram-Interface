import requests
from bs4 import BeautifulSoup as bs

DOMAIN = 'http://www.dgma.donetsk.ua'

URL_CALL_SCHEDULE = 'http://www.dgma.donetsk.ua/13-09-22-rozklad-dzvinkiv.html'
URL_CLASS_SCHEDULE = 'http://www.dgma.donetsk.ua/rozklad-dlya-dennogo-viddilennya.html'


def call_schedule_parser():
    request_call_schedule = requests.get(URL_CALL_SCHEDULE)
    soup = bs(request_call_schedule.text, 'html.parser')

    call_schedule_divs = soup.find_all('div', class_='item-page')
    call_schedule_p = call_schedule_divs[0].find_all('p')

    call_schedule_a = call_schedule_divs[0].find_all('a')
    call_schedule_image = call_schedule_a[0].find('img')['src']

    text = [p.text for p in call_schedule_p]
    image_url = f"{DOMAIN}{call_schedule_image}"

    return text, image_url, URL_CALL_SCHEDULE


def class_schedule_parser():
    request_schedule = requests.get(URL_CLASS_SCHEDULE)
    soup = bs(request_schedule.text, 'html.parser')

    schedule_divs = soup.find_all('div', class_='item-page')
    schedule_h = schedule_divs[0].find('h2')

    schedule_a = soup.find_all('a', class_='raspisanie')
    schedule_images = []

    for a_tag in schedule_a:
        img_href = a_tag.get('href')
        if img_href:
            if img_href.startswith('/'):
                full_url = DOMAIN + img_href
            else:
                full_url = img_href
            schedule_images.append(full_url)

    return schedule_h.text.strip(), schedule_images, URL_CLASS_SCHEDULE


print(class_schedule_parser())
