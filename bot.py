import requests
from os import getenv
from sys import exit
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import emoji



bot_token = getenv("TEST_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")
    
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['help'])
async def process_start_command(msg: types.Message):
    """Обработчик команды '/start'"""
    await msg.reply(f"Привет, {msg.from_user.first_name}!\n\nЯ простой бот, которой поможет проверить рабочий ли у тебя прокси адрес. Просто отрпавь мне его и я скажу работает он или нет. Так же можно отправить список адресов.\nАдреса писать в формате - логин:пароль@адрес:порт.\nНапример - вася:1234@127.0.0.1:8022\n\nПожалуйста, если у тебя есть пожелания напиши: t.me/espadane",disable_web_page_preview=True)
    user_id = msg.from_user.id


@dp.message_handler(Text)
async def add_tracked_ad(msg:types.Message):
    try:
        requests.get('https://icanhazip.com/')
        message = msg.text
        proxies = message.split('\n')
        for proxy in proxies:
            proxy_message = get_proxy_message(proxy)
            ip = check_ip(proxy)
            if ip == None:
                smile = emoji.emojize(':sad_but_relieved_face:')
                await msg.answer(f'{smile}Прокси не рабочий!\n\n' +proxy_message, disable_web_page_preview=True )
            else:
                smile = emoji.emojize(':slightly_smiling_face:')
                await msg.answer(f'{smile}Прокси в порядке!\n\n' + proxy_message + f'Сайт видит IP - {ip}')
    except:
        await msg.answer('Ну тут одно из двух, или вы написали что-то то не то. Или проверяльщик айпишника ушел на перерыв. Дай бог чтобы не в запой. Поставьте нам 5 звездочек пожалуйста.')        

def get_proxy_message(proxy):
    if '@' in proxy:
        proxy_parts = proxy.split(':')
        proxy_address = proxy_parts[1].split('@')[1]
        proxy_login = proxy_parts[0]
        proxy_pass = proxy_parts[1].split('@')[0]
        try:
            proxy_port = proxy_parts[2]
        except:
            proxy_port = '_______'
    elif '@' not in proxy:
        proxy_parts = proxy.split(':')
        proxy_address = proxy_parts[0]
        proxy_login = '_______'
        proxy_pass = '_______'
        proxy_port = proxy_parts[1]
    
    return f'Адрес: {proxy_address}\nЛогин: {proxy_login}\nПароль: {proxy_pass}\nПорт: {proxy_port}\n'

def check_ip(proxy=None):
    url = 'https://icanhazip.com/'
    proxy = proxy.strip()
    proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
                }

    try:
        session = requests.Session()
        session.proxies.update(proxies)
        response = session.get(url, timeout=10)
        ip = response.text
    except Exception as e:
        ip = None

    return ip


if __name__ == '__main__':
    executor.start_polling(dp)