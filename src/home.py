import io
import os

import requests
from PIL import Image
from lxml import etree

base_url = 'https://play.google.com/store/apps/details?id='
current_path = os.path.dirname(os.path.realpath(__file__))
final_path: str = os.path.join(current_path, 'app_icons')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}


def download_with_lxml():
    if not os.path.exists(final_path):
        os.mkdir(final_path)
    package_name = input('Enter App Package Name :')
    package_url = base_url + package_name
    print(f"Package url link -> {package_url}")

    response_package_url = requests.get(package_url, headers=headers)
    if response_package_url.status_code == 200:
        tree = etree.HTML(response_package_url.text)

        img_element = tree.xpath("//img")[1]
        app_icon_url = img_element.attrib['src']
        print(f"App Icon Url -> {app_icon_url}")

        response_icon_url = requests.get(app_icon_url)  # app icon url request call
        if response_icon_url.status_code == 200:
            saving_icon_path = final_path + '/' + package_name + '.webp'
            icon_size = response_icon_url.content.__sizeof__()
            with Image.open(io.BytesIO(response_icon_url.content)) as im:
                im = im.resize((96, 96))
                if icon_size > 5120:
                    im.save(saving_icon_path, 'webp')
                    print(f"App Icon Downloaded for {package_name} as Compressed and Resized")
                else:
                    im.save(saving_icon_path, 'webp')
                    print(f"App Icon Downloaded for {package_name} as Original")
                print(im)
        else:
            print(f"App Icon url request failed with {response_icon_url.status_code}")
    else:
        print(f"Package Icon url request failed with {response_package_url.status_code}")


if __name__ == '__main__':
    download_with_lxml()
