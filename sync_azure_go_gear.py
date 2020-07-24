#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import pandas as pd
import string
import unidecode
import shutil
from tqdm import tqdm
import argparse
import sqlalchemy


DEVICE_PATH = "/media/yvette/EC95-4FBB/Music/"
GPODDER_DOWNLOADS = "/home/yvette/gPodder/Downloads"
db_name = "/home/yvette/gPodder/Database"



def convert_to_valid_filename(filename):
    u = unidecode.unidecode(filename)
    valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
    valid_name = ''.join(c for c in u if c in valid_chars)
    return valid_name.replace(" ","_")


def get_podcast_on_device(device_path):
    print(f"device_path :{device_path}")
    podcasts_device_dic=[]
    p = Path(device_path)
    folders=[i for i in p.glob('**/*')if i.is_dir()]
    for f in folders:
        p = Path(DEVICE_PATH).joinpath(f)
        podcasts_device_dic+=[(f.name,i.name) for i in p.iterdir() if i.is_file()]

    try:
        df = pd.DataFrame(podcasts_device_dic)
  
        df.columns =["podcast","file"]
        df['title']=df['file'].str.split(".mp3", n = 1, expand = True)[0]
        df['title']= df['title'].apply(convert_to_valid_filename)
        df['podcast']= df['podcast'].apply(convert_to_valid_filename)
        return df
    except :
        print(f"no file found on device in {device_path}")
        return None



def get_podcast_on_gpodder(gpod_path):
    table_name = "episode"
    engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
    df_episodes = pd.read_sql_table(table_name, engine)
    df_episodes =  df_episodes[~df_episodes.download_filename.isnull()]
    
    table_name = "podcast"
    engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
    df_podcasts = pd.read_sql_table(table_name, engine)
    df = pd.merge(df_episodes,df_podcasts,left_on='podcast_id',right_on="id", suffixes=["_episode","_podcast"])
    return df

   

def get_new_podcasts(gpod_path,device_path):
    df_device = get_podcast_on_device(device_path)
    df_gpodder = get_podcast_on_gpodder(gpod_path)
    df_gpodder['filename_to_copy']= df_gpodder['title_episode'].apply(convert_to_valid_filename)+".mp3"
    df_gpodder['folder_to_copy']= df_gpodder['download_folder'].apply(convert_to_valid_filename)
    if df_device is not None:
        df_new_podcasts = df_gpodder[~df_gpodder.filename_to_copy.isin(df_device.file.tolist())]
    else :
        df_new_podcasts= df_gpodder
    
    return df_new_podcasts


def create_folders(podcast,device_path):
    Path(device_path).joinpath(podcast).mkdir(parents=True, exist_ok=True)


def copy_new_podcast(new_pod,gpod_path,device_path):
        from_file = Path(GPODDER_DOWNLOADS).joinpath(new_pod['download_folder']).joinpath(new_pod['download_filename'])
        to_file = Path(DEVICE_PATH).joinpath(new_pod['folder_to_copy']).joinpath(new_pod['filename_to_copy'])
        
        create_folders(new_pod['folder_to_copy'],device_path)
        shutil.copy(str(from_file), str(to_file))
     
        
def sync_device(gpod_path=GPODDER_DOWNLOADS,device_path=DEVICE_PATH):
    df_new = get_new_podcasts(gpod_path,device_path)
    with tqdm(total=df_new.shape[0]) as pbar:
    
        
        for new in df_new.to_dict('records'):
            copy_new_podcast(new,gpod_path,device_path)
            pbar.set_description(f'finished copy {new["folder_to_copy"]} / {new["filename_to_copy"]}')
            pbar.update(1)
    print("finished sync.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
   
    parser.add_argument('--gpod_path', required=False)
    parser.add_argument('--device_path', required=False)

    args = parser.parse_args()

    if args.gpod_path is not None and args.device_path is not None:
        sync_device(args.gpod_path,args.device_path)
    else :
        sync_device()

