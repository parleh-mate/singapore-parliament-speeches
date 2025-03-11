import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_root_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_directory, _ = os.path.split(script_dir)

    return root_directory


def join_path(root_path, file_path):
    return os.path.join(root_path, file_path)


def send_telebot(status):
    key = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    current_dt = datetime.datetime.now()
    dt_string = current_dt.strftime("%Y-%m-%d %H:%M:%S")
    message = f"Run successful as at GMT+0 {dt_string} with status:\n{status}"
    url = f"https://api.telegram.org/bot{key}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={message}"
    requests.get(url)
