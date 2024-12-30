import requests
from bs4 import BeautifulSoup as bs

URL = 'http://www.dgma.donetsk.ua/'
r = requests.get(URL)

print(r.text)
