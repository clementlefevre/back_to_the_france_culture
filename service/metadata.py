import requests

URL = "https://collections.vam.ac.uk/search/?offset=3300&limit=15&narrow=1&extrasearch=&q=creswell&commit=Search&quality=0&objectnamesearch=&placesearch=&after=&before=&namesearch=&materialsearch=&mnsearch=&locationsearch="


def get_metadata():
    r = requests.get(URL)
    main_page = etree.HTML(r.content)
    link_rss = main_page.xpath('//div[@class="teaser-content"]/a/@href')

