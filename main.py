import json
import requests
from bs4 import BeautifulSoup

url = "https://lenta.com/catalog/bakaleya/chipsy-suhariki-sneki/chipsy-i-kukuruznye-sneki/"


def get_data():
    with requests.Session() as connection:
        connection.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            }
        )
        response = connection.get(url=url)
        print(response.status_code)

    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find_all("div", class_="sku-card-small-container")

    products_dict = {}
    for product in products:
        product_name = product.find("div", class_="sku-card-small-header__title").text.strip()
        product_price = product.find("span", class_="price-label__integer").text.strip()
        find_href = product.find("a", class_="sku-card-small")
        product_url = f'https://lenta.com/{find_href.get("href")}'
        slug = product_url.split('/')[-2]

        products_dict[slug] = {
            "name": product_name,
            "price": product_price,
            "url": product_url
        }

    with open("products_dict.json", "w", encoding="utf-8") as file:
        json.dump(products_dict, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == "__main__":
    main()
