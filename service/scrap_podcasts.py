import requests
from lxml import etree

from config import ROOT_URL


def get_all_podcasts_links(pod):

    r = requests.get(ROOT_URL.format("", ""))
    main_page = etree.HTML(r.content)
    link_rss = main_page.xpath('//div[@class="teaser-content"]/a/@href')
    link_rss = [t.replace("/emissions/", "") for t in link_rss]
    return link_rss
