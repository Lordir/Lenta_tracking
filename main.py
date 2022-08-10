import json
import time

import requests
from bs4 import BeautifulSoup


def get_data(url, name_new_file):
    with requests.Session() as connection:
        connection.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            }
        )
        response = connection.get(url=url)
        if response.status_code == 444:
            print("Блокировка от ленты")
        print(response.status_code)

    not_last_page = False
    next_url = url

    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find_all("div", class_="sku-card-small-container")
    pagination = soup.find_all("ul", class_="pagination")
    for page in pagination:
        if page.find("li", class_="next disabled"):
            not_last_page = False
        else:
            number_of_pages = page.find("li", class_="next")
            next_class = number_of_pages.find("a")
            next_url = next_class.get("href")
            # print(next_url)
            not_last_page = True

    if name_new_file == "no":
        with open("products_dict.json", encoding="utf-8") as file:
            products_dict = json.load(file)

        for product in products:
            product_name = product.find("div", class_="sku-card-small-header__title").text.strip()
            product_price = product.find("span", class_="price-label__integer").text.strip()
            find_href = product.find("a", class_="sku-card-small")
            product_url = f'https://lenta.com/{find_href.get("href")}'
            slug = product_url.split('/')[-2]

            if slug in products_dict:
                continue
            else:
                products_dict[slug] = {
                    "name": product_name,
                    "price": product_price,
                    "url": product_url
                }
        with open("products_dict.json", "w", encoding="utf-8") as file:
            json.dump(products_dict, file, indent=4, ensure_ascii=False)

    else:
        products_dict = {}
        for product in products:
            product_name = product.find("div", class_="sku-card-small-header__title").text.strip()
            product_price = product.find("span", class_="price-label__integer").text.strip()
            find_href = product.find("a", class_="sku-card-small")
            product_url = f'https://lenta.com/{find_href.get("href")}'
            slug = product_url.split('/')[-2]

            if slug in products_dict:
                continue
            else:
                products_dict[slug] = {
                    "name": product_name,
                    "price": product_price,
                    "url": product_url
                }
        with open(f"{name_new_file}.json", "w", encoding="utf-8") as file:
            json.dump(products_dict, file, indent=4, ensure_ascii=False)

    if not_last_page:
        time.sleep(2)
        get_data(next_url, name_new_file)


def main():
    print("Введите ссылку на нужный раздел: (Ссылка должна быть ввиде: https://lenta.com/catalog/)")
    url = input()
    print(
        "Введите 'yes', если хотите сохранить данные в новом файле, или 'no', если хотите сохранить в общий файл products_dict.json")
    while True:
        new_file = input()
        if new_file == "yes":
            name_new_file = url.split('/')[-2]
            print(name_new_file)
            break
        elif new_file == "no":
            name_new_file = new_file
            break
        else:
            print("Ошибка, необходимо ввести 'yes' или 'no' ")
    get_data(url, name_new_file)


if __name__ == "__main__":
    main()
