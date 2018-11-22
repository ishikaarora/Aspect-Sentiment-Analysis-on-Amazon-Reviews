# Python script for extracting aspects based on dependancy rules
#! /usr/bin/env python


import requests
import os
import csv
import numpy as np
import pandas as pd
import urllib.request
import gzip
import sys
import spacy
import json
import boto3
from boto.s3.connection import S3Connection

#import enchant
from nltk.sentiment.vader import SentimentIntensityAnalyzer


BASE_PATH = os.getcwd()
PARENT = os.path.dirname(BASE_PATH)
CRED_PATH = BASE_PATH + "/data/credentials.txt"

#USE THIS FOR IMPORTING ANY FUNCTIONS FROM src
sys.path.insert(0,BASE_PATH)
from src.dataprep import clean_data

prod_pronouns = ['it','this','they','these']

def fetch_reviews(filepath):
    raw_data = pd.read_table(filepath,nrows=300,error_bad_lines=False) #nrows = 300
    return raw_data

def fetch_s3(filename):
    s3_basepath = 's3://amazon-reviews-pds/tsv/'
    s3_fullpath = s3_basepath + filename
    raw_data = pd.read_table(s3_fullpath, compression = 'gzip',error_bad_lines=False)
    return raw_data


def apply_extraction(row,nlp,sid):
    review_body = row['review_body']
    review_id = row['review_id']
    review_marketplace = row['marketplace']
    customer_id = row['customer_id']
    product_id = row['product_id']
    product_parent = row['product_parent']
    product_title = row['product_title']
    product_category = row['product_category']
    date = str(row['review_date'])
    star_rating = row['star_rating']
    url = add_amazonlink(product_id)



    doc=nlp(review_body)


    ## FIRST RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## RULE = M is child of A with a relationshio of amod
    rule1_pairs = []
    for token in doc:
        A = "999999"
        M = "999999"
        if token.dep_ == "amod" and not token.is_stop:
            M = token.text
            A = token.head.text

            # add adverbial modifier of adjective (e.g. 'most comfortable headphones')
            M_children = token.children
            for child_m in M_children:
                if(child_m.dep_ == "advmod"):
                    M_hash = child_m.text
                    M = M_hash + " " + M
                    break

            # negation in adjective, the "no" keyword is a 'det' of the noun (e.g. no interesting characters)
            A_children = token.head.children
            for child_a in A_children:
                if(child_a.dep_ == "det" and child_a.text == 'no'):
                    neg_prefix = 'not'
                    M = neg_prefix + " " + M
                    break

        if(A != "999999" and M != "999999"):
            rule1_pairs.append((A, M,sid.polarity_scores(token.text)['compound'],1))

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
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if((child.dep_ == "dobj" and child.pos_ == "ADJ") and not child.is_stop):
                M = child.text
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

    if (add_neg_pfx and M != "999999"):
        M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            rule2_pairs.append((A, M,sid.polarity_scores(M)['compound'],2))


    ## THIRD RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## Adjectival Complement - A is a child of something with relationship of nsubj, while
    ## M is a child of the same something with relationship of acomp
    ## Assumption - A verb will have only one NSUBJ and DOBJ
    ## "The sound of the speakers would be better. The sound of the speakers could be better" - handled using AUX dependency



    rule3_pairs = []

    for token in doc:

        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "acomp" and not child.is_stop):
                M = child.text

            # example - 'this could have been better' -> (this, not better)
            if(child.dep_ == "aux" and child.tag_ == "MD"):
                neg_prefix = "not"
                add_neg_pfx = True

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M
                #check_spelling(child.text)

        if(A != "999999" and M != "999999"):
            rule3_pairs.append((A, M, sid.polarity_scores(M)['compound'],3))

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
        add_neg_pfx = False
        for child in children :
            if((child.dep_ == "nsubjpass" or child.dep_ == "nsubj") and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "advmod" and not child.is_stop):
                M = child.text
                M_children = child.children
                for child_m in M_children:
                    if(child_m.dep_ == "advmod"):
                        M_hash = child_m.text
                        M = M_hash + " " + child.text
                        break
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            rule4_pairs.append((A, M,sid.polarity_scores(M)['compound'],4)) # )


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
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "cop" and not child.is_stop):
                buf_var = child.text
                #check_spelling(child.text)

        if(A != "999999" and buf_var != "999999"):
            rule5_pairs.append((A, token.text,sid.polarity_scores(token.text)['compound'],5))


    ## SIXTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## Example - "It ok", "ok" is INTJ (interjections like bravo, great etc)


    rule6_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        if(token.pos_ == "INTJ" and not token.is_stop):
            for child in children :
                if(child.dep_ == "nsubj" and not child.is_stop):
                    A = child.text
                    M = token.text
                    # check_spelling(child.text)

        if(A != "999999" and M != "999999"):
            rule6_pairs.append((A, M,sid.polarity_scores(M)['compound'],6))


    ## SEVENTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## ATTR - link between a verb like 'be/seem/appear' and its complement
    ## Example: 'this is garbage' -> (this, garbage)

    rule7_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if((child.dep_ == "attr") and not child.is_stop):
                M = child.text
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            rule7_pairs.append((A, M,sid.polarity_scores(M)['compound'],7))



    aspects = []

    aspects = rule1_pairs + rule2_pairs + rule3_pairs +rule4_pairs +rule5_pairs + rule6_pairs + rule7_pairs

    # replace all instances of "it", "this" and "they" with "product"
    aspects = [(A,M,P,r) if A not in prod_pronouns else ("product",M,P,r) for A,M,P,r in aspects ]

    dic = {"review_id" : review_id , "aspect_pairs" : aspects, "review_marketplace" : review_marketplace
    , "customer_id" : customer_id, "product_id" : product_id, "product_parent" : product_parent,
    "product_title" : product_title, "product_category" : product_category, "date" : date, "star_rating" : star_rating, "url" : url}

    return dic


# def init_spacy():
#     print("Loading Spacy")
#     nlp=spacy.load("en_core_web_lg")
#     for w in stopwords:
#         nlp.vocab[w].is_stop = True
#     for w in exclude_stopwords:
#         nlp.vocab[w].is_stop = False
#     return nlp
#
# def init_nltk():
#     print("\nLoading NLTK....")
#     try :
#         sid = SentimentIntensityAnalyzer()
#     except LookupError:
#         print("Please install SentimentAnalyzer using : nltk.download('vader_lexicon')")
#     print("NLTK successfully loaded")
#     return(sid)

def spell_check_init():
    spell_dict = enchant.Dict("en_US")
    return spell_dict

def check_spelling(word):
    spell_dict = spell_check_init()
    if not spell_dict.check(word):
        list_of_words = spell_dict.suggest(word)
        #print(list_of_words)
        with open('spelling.txt', 'a') as f:
            f.write("%s :" % word)

            for item in list_of_words:

                f.write("%s ," % item)

            f.write("\n")


def extract_aspects(reviews,nlp,sid):

    #reviews = df[['review_id', 'review_body']]
    # nlp = init_spacy()
    # sid = init_nltk()

    print("Entering Apply function!")
    aspect_list = reviews.apply(lambda row: apply_extraction(row,nlp,sid), axis=1) #going through all the rows in the dataframe

    return aspect_list


def aspect_extraction(nlp,sid):
    # filepath = BASE_PATH + "/data/raw/amazon_reviews_us_Electronics_v1_00.tsv"
    # reviews =  fetch_reviews(filepath)

    # UNCOMMENT THIS WHEN RUNNING ON AWS
    s3_filename = "amazon_reviews_us_Wireless_v1_00.tsv.gz"
    reviews = fetch_s3(s3_filename)

    reviews = clean_data.clean_data(reviews)
    aspect_list = extract_aspects(reviews,nlp,sid)

    #print(aspect_list)

    return aspect_list


def add_amazonlink(product_id):
    AMAZON_BASE_URL = "http://amazon.com/dp/"
    url = AMAZON_BASE_URL + str(product_id)
    #product_url = {"product_id" : product_id, "url" : url}
    return url

if __name__ == '__main__' :
    # nlp = init_spacy()
    a = aspect_extraction(nlp,sid)

    # USE THIS IF YOU WANT TO SEE THE ASPECTS IN A FILE
    # with open('your_file.txt', 'w') as f:
    #     for item in a:
    #         f.write("%s\n" % item)
