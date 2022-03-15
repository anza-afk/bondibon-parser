import requests
from bs4 import BeautifulSoup as bs
import csv
import os

def get_html(url:str,session:requests.Session) -> str:
    try: 
        result = session.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return None


def get_games_data(html:str) -> dict:
    soup = bs(html, 'html.parser')
    property_table = soup.find('div', class_="tab-content").findAll('td')
    property_list = [i.text.replace('\n','').replace('\t','').strip() for i in property_table]
    game_dict = dict(zip(property_list[::2],property_list[1::2]))
    game_dict['Название'] = soup.find('h1', id="pagetitle").text
    return game_dict
    

if __name__ == '__main__':
    sess = requests.Session()
    with open('links.txt', 'r', encoding="utf-8") as links_file:
        lines = links_file.readlines()[:]
        all_games = []
        counter = 0
        for line in lines:
            if line:
                current_line = get_games_data(get_html(line.strip('\n'), sess))
                current_line['Ссылка'] = line.strip('\n')
                all_games.append(current_line)
                print(f'link -> dict {counter}')
                if(os.name == 'posix'):
                    os.system('clear')
                else:
                    os.system('cls')
                counter += 1
    with open ('games.csv', 'a', encoding='utf-8', newline='') as target_file:
        fields = ['Название', 'Ссылка', 'Пол', 'Возраст от', 'Возраст до', 'Время игры', 'Количество игроков', 'Тип', 'Развитие навыков', 'Серия', 'Материал', 'На батарейках', 'Новинка', 'Артикул']
        writer = csv.DictWriter(target_file, fields, delimiter = ';')
        writer.writeheader()
        counter2 = 0            
        for game in all_games:
            try: 
                writer.writerow(game)
                print(f'dict -> csv {counter}')
                if(os.name == 'posix'):
                    os.system('clear')
                else:
                    os.system('cls')
                counter2 += 1
            except ValueError:
                continue

# url = 'https://www.bondibon.ru/catalog/oznakomlenie_s_mirom_prirody/nabor_nakleek_bondibon_nano_stiker_uchim_tsveta/'
# sess = requests.Session()
# a = get_games_data(get_html(url, sess))
# print(a)