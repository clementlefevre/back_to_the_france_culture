import requests
from lxml import etree
import pandas as pd
import logging



def get_podcast_metadata(content):

    e = etree.HTML(content)
    elements = e.xpath(
        "//div[@class='teaser-replay-button-wrapper']//button"
    )
    list_dic = [dict(d.attrib) for d in elements]
    df = pd.DataFrame(list_dic)
    logging.info(df)
    return df
