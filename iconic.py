import requests
from requests.auth import HTTPProxyAuth
import pandas as pd
from lxml import etree
from pathlib import Path
import time
import ipdb

# webproxy.comp.db.de:8080
# wwwproxy.tech.rz.db.de
proxyDict = {
    "http": "127.0.0.1:3128",
    "https": "127.0.0.1:3128",
}
auth = HTTPProxyAuth("clementlefevre", "Ergosum2048?")


def get_meta(page):
    url = f"https://iconicphotos.wordpress.com/page/{page}/"
    print(url)
    r = requests.get(url, proxies=proxyDict, auth=auth)
    main_page = etree.HTML(r.content)
    links = main_page.xpath('//h1[@class="entry-title"]//@href')
    time.sleep(2)
    print(links)
    return links


def scrap_all_metadata():
    all_links = []
    for i in range(0, 93):
        print(i)
        try:
            all_links += get_meta(i)
        except Exception as e:
            print(e)

    df = pd.DataFrame(all_links)
    df.to_csv("iconic_posts_list.csv", sep=";")


def get_page_data(url):

    r = requests.get(url, proxies=proxyDict, auth=auth)
    main_page = etree.HTML(r.content)
    title = main_page.xpath('//div[@class="entry-category"]//text()')
    text = main_page.xpath('//p[@style="text-align:justify;"]//text()')
    pic_url = main_page.xpath('//div[@class="entry-content"]//img//@src')

    return {"title": title, "text": text, "pic_url": pic_url}

