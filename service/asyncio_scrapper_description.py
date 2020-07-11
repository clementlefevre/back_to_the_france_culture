from aiohttp import ClientSession, TCPConnector
from lxml import html
import pandas as pd
import asyncio


async def get_podcast_description(title_infos, session):

    url_full = "https://www.franceculture.fr" + title_infos[1]

    try:
        async with session.get(url_full) as r:

            response = await r.text()
            tree = html.fromstring(response)

            elements = tree.xpath("//div[@class='text-zone']")
            infos = elements[0].text_content()
            return (title_infos[0], infos)
    except Exception as e:
        print(e)
        return None


async def run_title_infos(title_infos_list):

    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    # we set the connector to 10 because we are well educated people who play by the rules :
    connector = TCPConnector(limit=15)
    async with ClientSession(connector=connector) as session:
        for title_infos in title_infos_list:
            task = asyncio.ensure_future(
                get_podcast_description(title_infos, session)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        # you now have all response bodies in this variable
        return responses


def scrap_descriptions(df_metadata):
    url_title_links = df_metadata.set_index("data-media-id")[
        ["data-title-link"]
    ].to_dict()
    url_title_links = list(url_title_links["data-title-link"].items())
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run_title_infos(url_title_links))
    df_list = loop.run_until_complete(future)

    df_title_infos = pd.DataFrame(df_list)
    df_title_infos.columns = ["data-media-id", "data-title-description"]

    return df_title_infos
