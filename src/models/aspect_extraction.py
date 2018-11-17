# Python script for extracting aspects based on dependancy rules



import requests
import os
import csv
import numpy as np
import pandas as pd
import urllib.request
import gzip
import sys
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer


BASE_PATH = os.getcwd()

def fetch_reviews(filepath):
    raw_data = pd.read_table(filepath,nrows = 300,error_bad_lines=False)
    return raw_data



def apply_extraction(row,nlp):
    review_body = row['review_body']
    review_id = row['review_id']

    doc=nlp(review_body)
    sid = SentimentIntensityAnalyzer()

    ## FIRST RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## RULE = M is child of A with a relationshio of amod
    rule1_pairs = []
    for token in doc:
        if token.dep_ == "amod":
            rule1_pairs.append((token.head.text, token.text, sid.polarity_scores(token.text)['compound']))
            #return row['height'] * row['width']


    ## SECOND RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    #Direct Object - A is a child of something with relationship of nsubj, while
    # M is a child of the same something with relationship of dobj
    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule2_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        for child in children :
            if(child.dep_ == "nsubj"):
                A = child.text
            if(child.dep_ == "dobj"):
                M = child.text
        if(A != "999999" and M != "999999"):
            rule2_pairs.append((A, M, sid.polarity_scores(M)['compound']))


    ## THIRD RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    #Adjectival Complement - A is a child of something with relationship of nsubj, while
    # M is a child of the same something with relationship of acomp
    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule3_pairs = []

    for token in doc:

        children = token.children
        A = "999999"
        M = "999999"
        for child in children :
            if(child.dep_ == "nsubj"):
                A = child.text

            if(child.dep_ == "acomp"):
                M = child.text

        if(A != "999999" and M != "999999"):
            rule3_pairs.append((A, M, sid.polarity_scores(M)['compound']))

    ## FOURTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect

    #Adverbial modifier to a passive verb - A is a child of something with relationship of nsubjpass, while
    # M is a child of the same something with relationship of advmod

    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule4_pairs = []
    for token in doc:


        children = token.children
        A = "999999"
        M = "999999"
        for child in children :
            if(child.dep_ == "nsubjpass"):
                A = child.text

            if(child.dep_ == "advmod"):
                M = child.text

        if(A != "999999" and M != "999999"):
            rule4_pairs.append((A, M, sid.polarity_scores(M)['compound']))


    ## FIFTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect

    #Complement of a copular verb - A is a child of M with relationship of nsubj, while
    # M has a child with relationship of cop

    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule5_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        buf_var = "999999"
        for child in children :
            if(child.dep_ == "nsubj"):
                A = child.text

            if(child.dep_ == "cop"):
                buf_var = child.text

        if(A != "999999" and buf_var != "999999"):
            rule3_pairs.append((A, token.text, sid.polarity_scores(token.text)['compound']))

    aspects = []
    aspects = rule1_pairs + rule2_pairs + rule3_pairs +rule4_pairs +rule5_pairs
    dic = {"review_id" : review_id , "aspect_pairs" : aspects}
    return dic



def extract_aspects(df):

    reviews = df[['review_id', 'review_body']]
    nlp=spacy.load("en_core_web_lg")
    aspect_list = reviews.apply(lambda row: apply_extraction(row,nlp), axis=1) #going through all the rows in the dataframe

    return aspect_list


def aspect_extraction():
    filepath = BASE_PATH + "/data/raw/amazon_reviews_us_Electronics_v1_00.tsv"

    reviews =  fetch_reviews(filepath)
    aspect_list = extract_aspects(reviews)

    print(aspect_list)

    return aspect_list



if __name__ == '__main__' :
    aspect_extraction()
