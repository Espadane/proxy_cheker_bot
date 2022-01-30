import requests
from os import getenv
from sys import exit
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import emoji


bot_token = getenv("PROXY_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")
    
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['help'])
async def process_start_command(msg: types.Message):
    """Обработчик команды '/start'"""
    await msg.reply(f"Привет, {msg.from_user.first_name}!\n\nЯ простой бот, которой поможет проверить рабочий ли у тебя прокси адрес. Просто отрпавь мне его и я скажу работает он или нет. Так же можно отправить список адресов.\nАдреса писать в формате - адрес:порт:логин:пароль.\nНапример - 127.0.0.1:8080:вася:1234\n\nПожалуйста, если у тебя есть пожелания напиши: t.me/espadane",disable_web_page_preview=True)


@dp.message_handler(Text)
async def get_message(msg:types.Message):
    try:
        requests.get('https://icanhazip.com/')
        message = msg.text
        proxies = message.split('\n')
        good_proxies = []
        for proxy in proxies:
            proxy_data = get_proxy_data(proxy)
            address = proxy_data[0]['address']
            port = proxy_data[0]['port']
            login = proxy_data[0]['login']
            password = proxy_data[0]['password']
            code = proxy_data[0]['code']
            ip = check_ip(code)
            if ip == None:
                proxy_message = f'Адрес: {address}\nЛогин: {login}\nПароль: {password}\nПорт: {port}'
                await msg.answer(emoji.emojize(f':stop_sign::sad_but_relieved_face:Прокси не рабочий!\n\n' +proxy_message), disable_web_page_preview=True )
            else:
                proxy_message = f'Адрес: {address}\nЛогин: {login}\nПароль: {password}\nПорт: {port}\n'
                await msg.answer(emoji.emojize(f':green_circle::slightly_smiling_face:Прокси в порядке!\n\n' + proxy_message + f'Сайт видит IP - {ip}'))
                good_proxies.append(code+'\n')
        good_proxy_list = ''.join(good_proxies)
        await msg.answer(f'Хорошие, годные прокси:\n{good_proxy_list}')
    except Exception as e:
        print(e)
        await msg.answer('Ну тут одно из двух, или вы написали что-то то не то. Или проверяльщик айпишника ушел на перерыв. Дай бог чтобы не в запой. Поставьте нам 5 звездочек пожалуйста.')
        
def get_proxy_data(proxy):
    proxy_data = []
    proxy_parts = proxy.split(':')
    try:
        address = proxy_parts[0]
    except:
        address = ''
    try:
        port = proxy_parts[1]
    except:
        port = ''
    try:
        login = proxy_parts[2]
    except:
        login = ''
    try:
        password = proxy_parts[3]
    except:
        password = ''
    if login == '':
        code = f'{address}:{port}'
    else:
        code = f'{login}:{password}@{address}:{port}'
    
    proxy_data.append({
        'login' : login,
        'password' : password, 
        'address' : address,
        'port' : port, 
        'code' : code
    })
    
    return proxy_data


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
        response = session.get(url, timeout=3)
        ip = response.text
    except Exception as e:
        ip = None

    return ip



if __name__ == '__main__':
    executor.start_polling(dp)
