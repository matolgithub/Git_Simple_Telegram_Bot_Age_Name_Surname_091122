from os import getenv
import requests
from fake_headers import Headers
import telebot
from telebot import types
from pprint import pprint
from dotenv import load_dotenv
import random

load_dotenv()

url = f"https://api.telegram.org/bot{getenv('MY_TOKEN')}"
my_tlg_bot_091122 = telebot.TeleBot(getenv("MY_TOKEN"))
headers = Headers()
header = headers.generate()
persons = []
current_user = []


def check_bot():
    check_method = "/getMe"
    response = requests.get(url=f"{url}{check_method}", headers=header)
    print(response, response.status_code)
    print(response.text)
    pprint(response.json())
    print(f'ID-bot: {response.json()["result"]["id"]}\nUsername: {response.json()["result"]["username"]}')


def send_msg_tothebot():
    send_msg_method = "/sendMessage"
    response = requests.get(url=f"{url}{send_msg_method}?chat_id={getenv('ID')}&text={getenv('TEXT')}",
                            headers=header)
    # pprint(response.json())

    return response.json()


def get_updates():
    get_updates_method = "/getUpdates"
    response = requests.get(url=f"{url}{get_updates_method}", headers=header)
    print(response, response.status_code)
    pprint(response.json())

    return response.json()


@my_tlg_bot_091122.message_handler(content_types=["text"])
def greeting(message):
    try:
        if message.text == "Hello" or message.text == "hello" or message.text == "Hello!":
            my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Hello, nice to meet you?")
            my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="What is your name?")
            my_tlg_bot_091122.register_next_step_handler(message, get_name)
        else:
            my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Sorry! Don't understand you!")
    except Exception:
        my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Sorry! Damage!")


@my_tlg_bot_091122.message_handler(content_types=["text"])
def get_name(message):
    user_id = random.randint(1, 1000000)
    current_user.append(user_id)
    name = message.text
    current_user.append(name)
    my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="What is your surname?")
    my_tlg_bot_091122.register_next_step_handler(message, get_surname)

    return name


@my_tlg_bot_091122.message_handler(content_types=["text"])
def get_surname(message):
    surname = message.text
    current_user.append(surname)
    my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="What is your age?")
    my_tlg_bot_091122.register_next_step_handler(message, get_age)

    return surname


@my_tlg_bot_091122.message_handler(content_types=["text"])
def get_age(message):
    global current_user
    age = message.text
    current_user.append(age)
    id, name, surname, age = current_user[0], current_user[1], current_user[2], current_user[3]
    my_tlg_bot_091122.send_message(chat_id=message.chat.id, text=f"Very glad: {name} {surname}, with age: "
                                                                 f"{age} years.")
    persons.append({
        id: [name, surname, age]
    })
    print(f"Current user before: {current_user}.")
    current_user = []
    pprint(persons)
    print(f"Current user after: {current_user}.")
    my_tlg_bot_091122.register_next_step_handler(message, finish_talk)

    return age


@my_tlg_bot_091122.message_handler(content_types=["text"])
def finish_talk(message):
    try:
        if message.text == "Good by" or message.text == "by" or message.text == "By":
            my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Good by! Hope see you again!")
        else:
            my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Sorry! Don't understand you!")
    except Exception:
        my_tlg_bot_091122.send_message(chat_id=message.chat.id, text="Sorry! Damage!")
    my_tlg_bot_091122.register_next_step_handler(message, greeting)


if __name__ == "__main__":
    # check_bot()
    # get_updates()
    send_msg_tothebot()
    my_tlg_bot_091122.infinity_polling()
    greeting()
