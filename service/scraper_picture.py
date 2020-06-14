
import requests
from lxml import etree
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import re

from config import ROOT_URL


def get_rss_official_link(pod):

    r = requests.get(ROOT_URL.format(pod.podcast, ""))
    main_page = etree.HTML(r.content)
    link_rss = main_page.xpath('//div[@class="heading-zone-buttons"]//script/text()')
    s = link_rss[0]
    result = re.search('\"RSS\":"(.*).xml', s)
    url_rss = result.group(1)+".xml"

    return url_rss


def set_podcast_picture(pod):

    rss_link = get_rss_official_link(pod)
    root = etree.parse(rss_link)
    # Print the loaded XML
    url_podcast_jpg = root.xpath("//image/url/text()")[0]
    url_podcast_jpg
    img_data = requests.get(url_podcast_jpg).content
    with open(pod.pic_filename, 'wb') as handler:
        handler.write(img_data)

    img = Image.open(pod.pic_filename)
    draw = ImageDraw.Draw(img)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/humor-sans/Humor-Sans.ttf", 150)
    font = ImageFont.truetype("arial.ttf", 100)
    draw.text((70, 20), 'Archives', fill='#ff0081', font=font)
    img.save(pod.pic_filename)
    pod.s3.meta.client.upload_file(
        pod.pic_filename, pod.bucket_name, pod.pic_filename, ExtraArgs={"ACL": "public-read"}
    )


