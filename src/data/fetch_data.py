# Python script to download reviews data from Amazon S3 bucket

#How to run it?
# fetch_data.py local
# local == 1 or 0


import requests
import os
import csv
import numpy as np
import pandas as pd
import urllib.request
import gzip
import sys


def fetch_data(filename ,base_url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/"):
    #BASE_URL = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/"
    BASE_PATH = os.getcwd()
    response = urllib.request.urlopen(base_url + filename)

    outpath = BASE_PATH + "/data/raw/" + filename[:-3]
    with open(outpath, 'wb') as outfile:
        outfile.write(gzip.decompress(response.read()))

    return 1


def download_data(local) :
    BASE_PATH = os.getcwd()


    #All the links for the data

    #if local == True, only download selected files
    if local == 1 :
        print('Downloading data for local testing')
        links = ["amazon_reviews_us_Electronics_v1_00.tsv.gz","amazon_reviews_us_Office_Products_v1_00.tsv.gz"]
        for link in links:
            print(f'Dowloading {link}...')
            fetch_data(filename=link)


    #dowload all 46 files
    else :
        print('Beware : Downloading all 46 files!! Terminate if you did not want this.')

        links_file = BASE_PATH + "/data/raw/list_urls.csv"
        df_links = pd.read_csv(links_file, header = None)
        assert df_links.shape[0] == 46 , "Check Links file!!"
        links = df_links[0]
        for link in links:
            print(f'Dowloading {link}...')
            fetch_data(filename=link)



if __name__ == '__main__' :
    #Runner main function for downloading data
    print(f'You provided {sys.argv[1]} as the argument')
    download_data(local = int(sys.argv[1]))
