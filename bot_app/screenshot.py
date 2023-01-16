from __future__ import annotations
from aiogram import types
from .app import dp, bot
import urllib.parse as urlparse
import time
import regex
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')


def get_status_code(text: str) -> int | str:
    try:
        r = requests.head('{}'.format(text))
        return r.status_code
    except requests.ConnectionError:
        return "failed to connect"


def get_file_name(text: str) -> str:
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    link_with_replace = regex.sub(r"[\p{P}\p{S}]+", "", f'{text}'[:235])
    return f'./screens/{current_time}_{link_with_replace}.jpg'


def save_screenshot(text: str, file_name: str) -> None:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f'{text}')
    time.sleep(0.5)
    driver.save_screenshot(file_name)
    driver.quit()


@dp.message_handler()
async def screenshot(message: types) -> None:
    if urlparse.urlparse(message.text).scheme:
        chat_id = message['chat']['id']
        page_code = get_status_code(message['text'])
        file_name = get_file_name(message['text'])
        save_screenshot(message['text'], file_name)
        await bot.send_photo(chat_id, photo=open(file_name, 'rb'), caption=f'Response code - {page_code}')
    else:
        await message.answer("This isn't a link,\n'I'm waiting for a link")



