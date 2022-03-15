import requests
from bs4 import BeautifulSoup as bs

URL = 'https://www.bondibon.ru/catalog/logicheskie_i_nastolnye_igry/'
BASE_URL = 'https://www.bondibon.ru'


def get_page(url:str, session:requests.Session) -> str:
    try:
        html = session.get(url)
        html.raise_for_status()        
        return html.text
    except(requests.RequestException, ValueError):
        return None


def get_last_page(html:str) -> int:
    soup = bs(html, 'html.parser')
    url = soup.findAll('a', class_="dark_link")[-1]['href']
    return int(url.split('=')[1])


def get_page_links(html:str) -> list:
    links = []  
    soup = bs(html, 'html.parser')
    link = soup.findAll('a', class_='dark_link option-font-bold font_sm')
    for i in link:
        links.append(f'{BASE_URL}{i["href"]}')
    return links
    
if __name__ == '__main__':
    sess = requests.Session()
    with open('links.txt', 'w', encoding='utf-8') as l:
        for page in range(1,get_last_page(get_page(URL,sess))+1):
            current_page = f'{URL}?PAGEN_1={page}'
            links = get_page_links(get_page(current_page, sess))
            for link in links:
                l.writelines(f"{link}\n")

#print(get_page_links(get_page(URL)))