from os import getenv
import requests
from fake_headers import Headers
import telebot
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

my_tlg_bot_091122 = telebot.TeleBot(getenv("MY_TOKEN"))
headers = Headers()
header = headers.generate()


def check_bot():
    url = f"https://api.telegram.org/bot{getenv('MY_TOKEN')}"
    check_method = "/getMe"
    response = requests.get(url=f"{url}{check_method}", headers=header)
    print(response, response.status_code)
    pprint(response.text)


def main():
    check_bot()


if __name__ == "__main__":
    main()
