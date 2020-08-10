from aiohttp import ClientSession, TCPConnector
from lxml import etree
import asyncio
import pandas as pd
import logging

from service.scrap_metadata import get_podcast_metadata

from config import ROOT_URL


async def get_list_of_podscast_on_page(pod, page_number, session):
    url = ROOT_URL.format(str(pod.podcast), str(page_number))
    logging.info(f"getting metadata for {url}")
    try:
        async with session.get(url) as r:
            content = await r.text()
            df = get_podcast_metadata(content)
            return df

    except Exception as e:
        print(e)
        return None


async def run(pod):

    tasks = []
    logging.info(f"pod.range_url : {pod.range_url}")
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    # we set the connector to 10 because we are well educated people who play by the rules :
    connector = TCPConnector(limit=10)
    async with ClientSession(connector=connector) as session:
        for page in pod.range_url:
            logging.info(f"(pod, page, session){(pod, page, session)}")
            task = asyncio.ensure_future(
                get_list_of_podscast_on_page(pod, page, session)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        # you now have all response bodies in this variable
        return responses


def combine_all_metadata(df_list):
    df = pd.DataFrame()
    for d in df_list:
        df = pd.concat([df, d], axis=0)

    return df


def scrap_all_metadata(pod):

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(pod))
    df_list = loop.run_until_complete(future)
    df = combine_all_metadata(df_list)

    return df
