from service.asyncio_scrapper_metadata import scrap_all_metadata
from service.scraper_picture import get_podcast_picture


def test_metadata():

    df_all_metada = scrap_all_metadata("lart-est-la-matiere")
    assert df_all_metada.shape[0] > 0


def test_pic():
    get_podcast_picture("lart-est-la-matiere")
    assert 1 == 1
