import pandas as pd


from service.asyncio_scrapper_description import scrap_descriptions
from service.asyncio_scrapper_metadata import scrap_all_metadata
from service.s3 import get_s3_content, get_s3_session
from service.download_mp3 import download_podcasts
from service.create_rss import create_rss_feed
from service.scraper_picture import set_podcast_picture

from config import bucket_name, ROOT_URL, range_url


class Podcast:
    def __init__(self, name):

        self.podcast = name
        self.podcast_url = ROOT_URL.format(name, "")
        self.podcast_trim = name.replace("-", "_")
        self.s3 = get_s3_session()
        self.range_url = range_url
        self.bucket_name = bucket_name
        self.pic_filename = self.podcast_trim + ".jpg"
        self.rss_filename = self.podcast_trim + ".rss"

    def retrieve_infos(self):

        df_metadata = scrap_all_metadata(self)
        df_descriptions = scrap_descriptions(df_metadata)
        self.df_podcasts = pd.merge(
            df_metadata, df_descriptions, on="data-media-id"
        )
        self.df_podcasts.to_csv("podcasts.csv", sep=";")

    def download_mp3_to_s3(self):

        df_s3 = get_s3_content(self)

        self.df_url_to_dl = self.df_podcasts[
            ~(self.df_podcasts["data-asset-source"].isnull())
            & ~(self.df_podcasts["data-media-id"].isin(df_s3["data-media-id"]))
        ]

        download_podcasts(self)

    def set_picture(self):
        try:
            set_podcast_picture(self)
            self.podcast_pic_url = f"https://{self.bucket_name}.s3.amazonaws.com/{self.pic_filename}"
        except Exception:
            self.podcast_pic_url = None

    def create_rss_feed(self):
        df_s3_after_dl = get_s3_content(self)

        self.df_for_rss = self.df_podcasts[
            self.df_podcasts["data-media-id"].isin(
                df_s3_after_dl["data-media-id"]
            )
        ]

        create_rss_feed(self)

    def process(self):
        self.retrieve_infos()
        self.download_mp3_to_s3()
        self.set_picture()
        self.create_rss_feed()
