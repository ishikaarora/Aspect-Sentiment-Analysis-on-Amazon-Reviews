#!home/ec2-user/miniconda3/bin/python3.7


import os
import sys
import spacy
from time import time
import json
import requests
import csv

import urllib.request
import gzip
import sys
import boto3
from nltk.sentiment.vader import SentimentIntensityAnalyzer

BASE_PATH = os.getcwd()
# PARENT = os.path.dirname(BASE_PATH)
# os.chdir(PARENT)
# print(BASE_PATH)
sys.path.insert(0,BASE_PATH)
NUM_CLUSTERS = 5

from src.models import aspect_extraction
from src.models import aspect_clustering
from src.models import mapper


stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

exclude_stopwords = ['it','this','they','these'] # update in aspect_extraction script as well to be replaced by 'product'
# stopwords = np.setdiff1d(stopwords, ['it','this']
def init_spacy():
    print("\nLoading spaCy Model....")
    nlp = spacy.load('en_core_web_lg')
    print("spaCy successfully loaded")
    for w in stopwords:
        nlp.vocab[w].is_stop = True
    for w in exclude_stopwords:
        nlp.vocab[w].is_stop = False
    return nlp

def init_nltk():
    print("\nLoading NLTK....")
    try :
        sid = SentimentIntensityAnalyzer()
    except LookupError:
        print("Please install SentimentAnalyzer using : nltk.download('vader_lexicon')")
    print("NLTK successfully loaded")
    return(sid)

def main(arg):
    time1 = time()
    nlp = init_spacy()
    sid = init_nltk()
    time2 = time()
    print("----------------***----------------")
    print("\nExtracting aspect pairs")
    aspect_extraction.aspect_extraction(nlp,sid,arg)
    print("Finished running aspect extraction!!\n")

    # json_data = json.dumps(reviews_data)
    # with open('data.json', 'w') as outfile:
    #     f.write(json_data)

    # print("----------------***----------------")
    # time3 = time()
    # aspect_clustering.update_reviews_data(reviews_data, nlp)
    time4 = time()
    print("Time for spacy loading: {0:.2}s".format(time2-time1))
    # print("Time for aspect extraction: {0:.2}s".format(time3-time2))
    print("Time for EVERYTHING: {0:.2}s".format(time4-time1))
    print("Running mapper")
    file_in = "data/interim/reviews_aspect_raw.json"
    file_out = "data/processed/reviews_aspect_mapping.json"
    mapper.map(file_in, file_out)

    print("Godspeed!")



if __name__ == '__main__' :
    print(f'You provided {sys.argv[1]} as the argument')

    main(sys.argv[1])
