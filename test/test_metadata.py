from iconic import get_page_data


def test_iconic_content():
    page_content = get_page_data(
        "https://iconicphotos.wordpress.com/2009/05/25/war-is-over/"
    )
    print(page_content)

