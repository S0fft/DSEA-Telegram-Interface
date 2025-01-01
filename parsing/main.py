import requests
from bs4 import BeautifulSoup as bs

DOMAIN = 'http://www.dgma.donetsk.ua'

URL_CALL_SCHEDULE = 'http://www.dgma.donetsk.ua/13-09-22-rozklad-dzvinkiv.html'


def schedule_parser(url):
    request_schedule = requests.get(url)
    soup = bs(request_schedule.text, 'html.parser')

    # Text
    call_schedule_divs = soup.find_all('div', class_='item-page')
    call_schedule_p = call_schedule_divs[0].find_all('p')

    # Image
    call_schedule_a = call_schedule_divs[0].find_all('a')
    call_schedule_image = call_schedule_a[0].find('img')['src']

    return [p.text for p in call_schedule_p] + ["\n" + (f'{DOMAIN}{call_schedule_image}')]


print("\n".join(schedule_parser(URL_CALL_SCHEDULE)))
