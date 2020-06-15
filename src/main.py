import os

import requests
from bs4 import BeautifulSoup

base_url = 'https://play.google.com/store/apps/details?id='
current_path = os.path.dirname(os.path.realpath(__file__))
final_path = os.path.join(current_path, 'app_icons')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}


def main():
    if not os.path.exists(final_path):
        os.mkdir(final_path)
    download_icon()


def download_icon():
    package_name = input('Enter App Package Name :')  # User Input on Run
    package_url = base_url + package_name  # Constructed app link from user input and base url
    print(f"Package url link -> {package_url}")
    app_url_response = requests.get(package_url, headers=headers)  # url request call
    page = app_url_response.content  # fetching page raw data
    parsed_html_page = BeautifulSoup(page, 'html.parser')  # parsed raw html data using beautiful soup
    # parsed_html_page = BeautifulSoup(page, 'html.parser')  # parsed raw html data using beautiful soup
    results = parsed_html_page.findAll('img', recursive=True, limit=5)  # queried for img tag in parsed data
    print(f"Count of img tags -> {results.__len__()}")
    app_img_tag = results.pop(1)  # fetched 2nd element for img for app icon
    app_icon_url = app_img_tag.get('src')  # fetched src attribute for app icon url
    print(f"App Icon link -> {app_icon_url}")

    icon_url_response = requests.get(app_icon_url)  # app icon url request call
    icon_path = final_path + '/' + package_name + '.webp'  # app icon file name
    with open(icon_path, 'wb') as file:  # saving app icon with app name
        file.write(icon_url_response.content)
    print(f"App Icon Downloaded for {package_name}")


# package_name com.zhiliaoapp.musically
# Xpath -> //*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[1]/div/img
# Full XPath -> /html/body/div[1]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[1]/div/img

if __name__ == '__main__':
    main()
