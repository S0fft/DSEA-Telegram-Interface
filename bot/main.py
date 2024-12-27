import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from bs4 import BeautifulSoup
from decouple import config

bot = Bot(config("TOKEN"))
dp = Dispatcher(bot)

DOMAIN = "https://www.dgma.donetsk.ua/"


@dp.message_handler(commands=["start"])
async def start(message: types.message):
    await bot.send_message(
        message.chat.id,
        "'Greatings'",
        parse_mode="html",
        disable_web_page_preview=0
    )


# @dp.message_handler(content_types=["text"])
# async def parser(message: types.message):
#     headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
#     # print(message.text)

#     url = "https://prom.ua/ua/search?search_term=" + message.text
#     request = requests.get(url, headers=headers)
#     soup = BeautifulSoup(request.text, "html.parser")

#     links = soup.find_all('a', class_='_0cNvO jwtUM', attrs={'data-qaid': 'product_link'})

#     for link in links[:10]:
#         # print(DOMEN + link["href"] + "\n")

#         url = DOMAIN + link["href"]
#         request = requests.get(url, headers=headers)
#         soup = BeautifulSoup(request.text, "html.parser")

#         name = soup.find("h1", class_="_3Trjq F7Tdh vj3pM htldP", attrs={'data-qaid': 'product_name'}).text
#         price = soup.find("span", class_="yzKb6").text.replace(" ", ".")
#         image = soup.find("img", class_="MPQaS gHc6F")["src"]
#         # print(name, "\n", price, "\n", image, "\n")

#         await bot.send_photo(message.chat.id, image, caption="<b>" + name + "</b>\n<i>" + price + " грн." + f"</i>\n<a href='{url}'>Link to the page</a>", parse_mode="html")

# executor.start_polling(dp)
