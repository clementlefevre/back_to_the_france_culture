# -*- coding: utf-8 -*-

import argparse
from model.podcast import Podcast


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--podcast", required=True, type=str)
    args = parser.parse_args()
    podcast = args.podcast

    podcast = Podcast(podcast)
    podcast.process()
