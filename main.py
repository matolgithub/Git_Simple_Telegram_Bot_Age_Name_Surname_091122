from os import getenv
import requests
from fake_headers import Headers
import telebot
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

url = f"https://api.telegram.org/bot{getenv('MY_TOKEN')}"
my_tlg_bot_091122 = telebot.TeleBot(getenv("MY_TOKEN"))
headers = Headers()
header = headers.generate()


def check_bot():
    check_method = "/getMe"
    response = requests.get(url=f"{url}{check_method}", headers=header)
    print(response, response.status_code)
    print(response.text)
    pprint(response.json())
    print(f'ID-bot: {response.json()["result"]["id"]}\nUsername: {response.json()["result"]["username"]}')


def send_msg_tothebot():
    send_msg_method = "/sendMessage"
    response = requests.get(url=f"{url}{send_msg_method}?chat_id={getenv('CHAT_ID')}&text={getenv('TEXT')}",
                            headers=header)
    pprint(response.json())

    return response.json()


def get_updates():
    get_updates_method = "/getUpdates"
    response = requests.get(url=f"{url}{get_updates_method}", headers=header)
    print(response, response.status_code)
    pprint(response.json())

    return response.json()


def main():
    # check_bot()
    # send_msg_tothebot()
    get_updates()


if __name__ == "__main__":
    main()
