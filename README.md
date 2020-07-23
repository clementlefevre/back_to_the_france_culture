# Store France Culture progrqms on AWS S3 and create RSS feed

- set the `config.py` according to the `config_template.py` with your own S3 credentials and bucket name.
- check the example in the jupyter notebook, to set the program's name, check the url, e.g for *Les Chemins de la Philosophie*, the url is *https://www.franceculture.fr/emissions/les-chemins-de-la-philosophie*, thus the program name is *les-chemins-de-la-philosophie*
- the script retrieves all broadcasts available from the France Culture website, which is much more than the official rss feed (back to 2010)
- once you ran the `process()` function, the script retrieves the list of podcasts, store the mp3 files to your S3 bucket and then create a RSS Feed file on the same S3 bucket. For instance, for *les-chemins-de-la-philosophie*, just look for the *les-chemins-de-la-philosophie.rss* file in your S3 bucket and open this file with your podcast player.

# activate conda env within windows bash shell :
eval "$(conda shell.bash hook)"
conda activate back_to_france_culture

# add MS font to Linux (Google colab)
!sudo apt-get install ttf-mscorefonts-installer
!sudo fc-cache