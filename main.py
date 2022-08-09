import json
import time

import requests
from bs4 import BeautifulSoup


def get_data(url):
    while True:
        with requests.Session() as connection:
            connection.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                }
            )
            response = connection.get(url=url)
            print(response.status_code)
            if response.status_code == 200:
                break
            else:
                time.sleep(10)

    not_last_page = True
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
            print(next_url)

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

    if not_last_page:
        time.sleep(1)
        get_data(next_url)


def main():
    url = "https://lenta.com/catalog/myaso-ptica-kolbasa/"
    get_data(url)


if __name__ == "__main__":
    main()
