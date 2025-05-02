import urllib.parse

import requests
from bs4 import BeautifulSoup as bs

DOMAIN = 'http://www.dgma.donetsk.ua'

URL_CALL_SCHEDULE = 'http://www.dgma.donetsk.ua/13-09-22-rozklad-dzvinkiv.html'
URL_CLASS_SCHEDULE = 'http://www.dgma.donetsk.ua/rozklad-dlya-dennogo-viddilennya.html'
URL_SESSION_SCHEDULE = 'http://www.dgma.donetsk.ua/index.php?option=com_content&Itemid=1650&id=2819&lang=uk&layout=edit&view=article'
URL_SCHOLARSHIP_LIST = 'http://www.dgma.donetsk.ua/stipendiya.html'


# -----------------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------------

def class_schedule_parser():
    request_class_schedule = requests.get(URL_CLASS_SCHEDULE)
    soup = bs(request_class_schedule.text, 'html.parser')

    class_schedule_divs = soup.find_all('div', class_='item-page')
    class_schedule_h = class_schedule_divs[0].find('h2')

    class_schedule_a = soup.find_all('a', class_='raspisanie')
    class_schedule_images = []

    for a_tag in class_schedule_a:
        img_href = a_tag.get('href')
        if img_href:
            if img_href.startswith('/'):
                full_url = DOMAIN + img_href
            else:
                full_url = img_href
            class_schedule_images.append(full_url)

    return class_schedule_h.text.strip(), class_schedule_images, URL_CLASS_SCHEDULE


# -----------------------------------------------------------------------------------

def session_schedule_parser():
    session_request_schedule = requests.get(URL_SESSION_SCHEDULE)
    soup = bs(session_request_schedule.text, 'html.parser')

    session_schedule_divs = soup.find_all('div', class_='item-page')
    session_schedule_h = session_schedule_divs[0].find('h2')

    session_schedule_a = soup.find_all('a', class_='raspisanie')
    session_schedule_images = []

    for a_tag in session_schedule_a:
        img_href = a_tag.get('href')
        if img_href:
            if img_href.startswith('/'):
                full_url = DOMAIN + img_href
            else:
                full_url = img_href
            session_schedule_images.append(full_url)

    return session_schedule_h.text.strip(), session_schedule_images, URL_SESSION_SCHEDULE


# -----------------------------------------------------------------------------------

def scholarship_list_parser():
    response = requests.get(URL_SCHOLARSHIP_LIST)
    soup = bs(response.text, 'html.parser')

    link_tag = soup.find("a", string=lambda text: text and "Наказ ДДМА про призначення академічної стипендії" in text)

    if not link_tag:
        raise Exception("No link found with the requested text!")

    href = link_tag.get("href")
    filename = href.split('/')[-1]
    link_text = link_tag.text.strip()

    full_url = urllib.parse.urljoin(DOMAIN, href)

    parsed = urllib.parse.urlparse(full_url)

    encoded_path = urllib.parse.quote(parsed.path)
    encoded_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"

    return encoded_url, filename, link_text, URL_SCHOLARSHIP_LIST
