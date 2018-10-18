# Python script to download reviews data from Amazon S3 bucket
import requests
import os
import urllib.request
import gzip

BASE_URL = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/"
BASE_PATH = os.getcwd()





filename = "amazon_reviews_us_Electronics_v1_00.tsv.gz"

response = urllib.request.urlopen(BASE_URL + filename)

outpath = BASE_PATH + "/data/raw/" + filename[:-3]
with open(outpath, 'wb') as outfile:
    outfile.write(gzip.decompress(response.read()))
