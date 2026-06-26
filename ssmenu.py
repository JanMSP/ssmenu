from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup

url = "https://able.dk/wp-admin/admin-ajax.php"
headers = {
    'User-Agent': 'MenuPoster/1.0.0'
}
data = {
    'action': 'load_menus',
    'post_id': '5458'
}
response = requests.post(url, data=data, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

target_day = "I dag"
day_names = {
    0: "Søndag",
    1: "Mandag",
    2: "Tirsdag",
    3: "Onsdag",
    4: "Torsdag",
    5: "Fredag",
    6: "Lørdag"
}

day_title = soup.find('h2', class_='day-title', string=target_day)

if day_title:
    day = day_title.find_parent('div', class_='day')
    dishes = day.find_all('div', class_='dish')

    day_name = day_names[datetime.now().weekday()]

    menu = f"*{day_name} - Menu*\n\n"

    for dish in dishes:
        heading = dish.find('div', class_='heading').get_text(strip=True)
        description = dish.find('div', class_='text').get_text(strip=True)
        menu += f"*_{heading}_*\n{description}\n\n"

        # Tartelet handling
        if heading == "Dagens ret" and "tarteletter" in description.lower():
            menu = ":rotating_light: Kode 42 :rotating_light:\n\n" + menu

    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    requests.post(slack_webhook_url, json={"text": menu}, headers={'Content-Type': 'application/json'})

else:
    print(f"Could not find a section matching '{target_day}'")