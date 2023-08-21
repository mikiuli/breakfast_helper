import requests
from bs4 import BeautifulSoup as BS
from time import sleep


# заголовки, которые описывают пользователя, что переходит по конкретному URL адресу,
# ArithmeticError чтоб сайт не считал нас ботом
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.124 Safari/537.36'
}

def get_dish_urls():
    for page in range(2, 6):
        page_url = f'https://1000.menu/catalog/na-zavtrak/{page}'
        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BS(response.text, 'html.parser')
            dish_urls = soup.find_all('a', class_="h5")
            for dish_url in dish_urls:
                full_url = 'https://1000.menu' + dish_url['href']
                yield full_url
        else:
            print(response.status_code)


def get_a_recipe():
    for dish_url in get_dish_urls():
        sleep(0.1)
        response = requests.get(dish_url, headers=headers)
        if response.status_code == 200:
            soup = BS(response.text, 'html.parser')
            name = soup.find('h1', itemprop="name").text

            ingredients = soup.find_all('meta', itemprop="recipeIngredient")
            list_of_ingredients = []
            for ingredient in ingredients:
                list_of_ingredients.append(ingredient.get('content'))

            PFC = soup.find('div', id="calories-graph")
            proteins = PFC.find('span', id="nutr_p").text
            fats = PFC.find('span', id="nutr_f").text
            carbohydrates = PFC.find('span', id="nutr_c").text
            calories = soup.find("div", class_="calories").text.strip()
            portions = soup.find_all("span", class_='label')[2].text + soup.find("input", class_='mr-1').get('value')
            portions = portions[7:]
            time_for_cooking = soup.find_all("span", class_='label')[3].text
            time_for_cooking = time_for_cooking[21:]
            picture_url = "https:" + soup.find("img", itemprop="image").get("src")
            # print(name, '; \n'.join(list_of_ingredients), proteins, fats, carbohydrates, calories[:-5],
            #         time_for_cooking, portions, url[26:], picture_url)
            yield (name, ';'.join(list_of_ingredients), proteins, fats,
                   carbohydrates, calories[:-5], portions, time_for_cooking, picture_url[44:], dish_url[26:])
        else:
            print(response.status_code)
