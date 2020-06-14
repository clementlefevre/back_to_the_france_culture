import os
import threading
import requests
from queue import Queue
from config import bucket_name
import shutil
from pathlib import Path


class DownloadThread(threading.Thread):
    def __init__(self, s3, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True
        self.s3 = s3

    def run(self):
        while True:
            title = self.queue.get()
            try:
                # self.download_url(url)

                self.dl_mp3(title)
            except Exception as e:
                print("   Error: %s" % e)
            self.queue.task_done()

    def dl_mp3(self, title):

        name = title["data-media-id"] + ".mp3"
        file_url = title["data-asset-source"]
        dest = os.path.join(self.destfolder, name)

        try:
            # print ("[%s] Downloading %s -> %s"%(self.ident,file_url, dest))
            r = requests.get(file_url, stream=True)
            if r.status_code == 200:
                with open(dest, "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                # upload cleaned df to s3
                # print(f'uploading {name} to S3 bucket {bucket_name}')
                # s3.Bucket(bucket_name).put_object(Key=name, Body=data)
                self.s3.meta.client.upload_file(
                    dest, bucket_name, name, ExtraArgs={"ACL": "public-read"}
                )
                os.remove(dest)
        except Exception as e:
            print(e)


def download(s3, df_url, destfolder, numthreads=10):
    urls = df_url.to_dict("records")
    queue = Queue()
    for url in urls:
        queue.put(url)

    for i in range(numthreads):
        t = DownloadThread(s3, queue, destfolder)
        t.start()

    queue.join()


def download_podcasts(pod):
    dirpath = os.path.dirname("tmp")
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    Path("tmp").mkdir(parents=True, exist_ok=True)
    print(f"files to be downloaded : {pod.df_url_to_dl.shape[0]}")
    download(pod.s3, pod.df_url_to_dl, "tmp/")
    shutil.rmtree("tmp/")
