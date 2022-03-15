import requests

URL = 'https://www.bondibon.ru/catalog/razvitie_poznavatelnykh_deystviy/logicheskaya_nastolnaya_igra_kamelot_smart_games_bondibon'


SESS = requests.Session()

def get_page(url):
    try:
        html = SESS.get(url)
        html.raise_for_status()        
        return html.text
    except(requests.RequestException, ValueError):
        return None

with open('test.html', 'w', encoding='utf=8') as f:
    f.writelines(get_page(URL))