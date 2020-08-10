import requests
import pandas as pd
from model.podcast import Podcast
from service.asyncio_scrapper_metadata import scrap_all_metadata
from service.scraper_picture import set_podcast_picture
from service.scrap_metadata import get_podcast_metadata
import logging


def test_scrap_metadata():
    pod = Podcast("ecole-normale-superieure", range_url=range(0,2))
    df_all_metadata = scrap_all_metadata(pod)
    df_all_metadata = df_all_metadata[~df_all_metadata["data-media-id"].isnull()]
    assert df_all_metadata.shape[0] > 0


def test_metadata():
    pod = Podcast("lart-est-la-matiere", range_url=range(0,2))
    df_all_metada = scrap_all_metadata(pod)
    assert df_all_metada.shape[0] > 0


def test_pic():
    pod = Podcast("lart-est-la-matiere")
    set_podcast_picture(pod)
    assert 1 == 1


def test_process():
    pod = Podcast("lart-est-la-matiere")
    pod.process()
