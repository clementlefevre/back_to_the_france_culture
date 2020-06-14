# -*- coding: utf-8 -*-

from rfeed import Item, Feed, Guid, Image
import datetime


def create_rss_object(all_titles_with_s3, pod):
    items_list = []
    for title in all_titles_with_s3:
        id = title["data-media-id"]
        guid = f"https://{pod.bucket_name}.s3.amazonaws.com/{id}.mp3"
        url = guid

        item = Item(
            title=title["data-asset-title"],
            link=url,
            description=title["data-title-description"],
            author="France Culture",
            guid=Guid(guid),
            pubDate=datetime.datetime.fromtimestamp(
                int(title["data-asset-created-date"])
            ),
        )
        items_list.append(item)

    feed = Feed(
        title=pod.podcast,
        link="https://www.franceculture.fr/emissions/" + pod.podcast,
        image=Image(pod.podcast_pic_url, pod.podcast, pod.podcast_url),
        description=pod.podcast,
        language="en-US",
        lastBuildDate=datetime.datetime.now(),
        items=items_list,
    )
    return feed


def create_rss_feed(pod):
    all_titles_with_s3 = pod.df_for_rss.to_dict("records")
    feed = create_rss_object(all_titles_with_s3, pod)

    text_file = open(pod.rss_filename, "w", encoding="utf-8")

    text_file.write(feed.rss())

    text_file.close()

    pod.s3.meta.client.upload_file(
        pod.rss_filename,
        pod.bucket_name,
        pod.rss_filename,
        ExtraArgs={"ACL": "public-read"},
    )
