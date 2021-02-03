import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import sys
import random
from datetime import datetime
from colorama import init, Fore
init(convert=True)


def generate_number():
	num1 = random.randint(7, 8)
	num2 = random.choice(['920', '980', '910', '953', '900', '930', '915', '919', '962'])
	num3 = random.randint(152, 853)
	num4 = random.randint(3523, 9997)
	number_phone = f'{num1} ({num2}) {num3}-{num4}'
	return number_phone


url = 'https://aquastop.online'
ua = UserAgent().random

proxy_list = []
headers = {
	'User-Agent': ua
}

count = 0
print(f'{Fore.CYAN}[{datetime.now().strftime("%X")}] Начинаю работу!')
while True:
	responce = requests.get('https://free-proxy-list.net/', headers=headers)
	bs = BeautifulSoup(responce.text, 'lxml')
	table = bs.find('table')
	rows = table.find_all('tr')
	try:
		print(f'{Fore.LIGHTBLUE_EX}[{datetime.now().strftime("%X")}] Ищу прокси, жди...')
		for row in rows:
			ip = row.contents[0].text
			port = row.contents[1].text
			anonym = row.contents[4].text
			select = row.contents[6].text
			if(select == 'yes' and (anonym == 'anonymus' or anonym == 'elite proxy')):
				line = f'http://{ip}:{port}'
				proxies = {'http': line, 'https': line}
				try:
					testIP = requests.get(url, proxies=proxies, timeout=2)
					if testIP.status_code == 200:
						good_proxie = proxies['http'].replace('http://', '')
						print(f'{Fore.LIGHTYELLOW_EX}[{datetime.now().strftime("%X")}] Использую прокси: {good_proxie}')
						gen_phone = generate_number()
						post_page = requests.post('https://aquastop.online/send-form/telegram-form.php', headers=headers, proxies=proxies, data={'user_phone': gen_phone}, allow_redirects=False)
						if post_page.status_code == 302:
							count += 1
							print(f'{Fore.LIGHTGREEN_EX}[{datetime.now().strftime("%X")}] Отправил номер: {gen_phone}')
							print(f'{Fore.LIGHTBLUE_EX}[{datetime.now().strftime("%X")}] Ищу прокси, жди...')
							time.sleep(5)
				except Exception:
					pass
	except KeyboardInterrupt:
		print(f'{Fore.CYAN}[{datetime.now().strftime("%X")}] Завершил работу! Отправил сообщений: {str(count)}')
		sys.exit(0)
