import boto3
from collections import namedtuple
import pandas as pd

from config import AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY

FileS3 = namedtuple("FileS3", ["key", "last_date", "size"])


def get_s3_session():
    session = boto3.Session(
        aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
        aws_secret_access_key=AWS_SERVER_SECRET_KEY,
    )

    s3 = session.resource("s3")
    return s3


def get_s3_content(pod):
    all_files = pod.s3.Bucket(pod.bucket_name).objects.all()
    all_files = list(all_files)
    all_files_infos = [
        FileS3(f.key, f.last_modified, f.size) for f in all_files
    ]
    df_s3 = pd.DataFrame(all_files_infos)
    df_s3 = df_s3[df_s3.key.str.contains(".mp3")]
    df_s3["data-media-id"] = df_s3["key"].apply(lambda x: x.split(".mp3")[0])
    return df_s3
