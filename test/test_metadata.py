from model.podcast import Podcast
from service.asyncio_scrapper_metadata import scrap_all_metadata
from service.scraper_picture import set_podcast_picture


def test_metadata():
    pod = Podcast("lart-est-la-matiere")
    df_all_metada = scrap_all_metadata(pod)
    assert df_all_metada.shape[0] > 0


def test_pic():
    pod = Podcast("lart-est-la-matiere")
    set_podcast_picture(pod)
    assert 1 == 1


def test_process():
    pod = Podcast("lart-est-la-matiere")
    pod.process()
