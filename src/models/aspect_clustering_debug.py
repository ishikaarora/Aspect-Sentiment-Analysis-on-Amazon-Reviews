import json
import spacy
import pandas as pd
import os
import sys
from sklearn import cluster
from collections import defaultdict
from time import time

BASE_PATH = os.getcwd()
# PARENT = os.path.dirname(BASE_PATH)
# os.chdir(PARENT)
# print(BASE_PATH)
sys.path.insert(0,BASE_PATH)
NUM_CLUSTERS = 4

# @profile
def init_spacy():
    print("\nLoading spaCy Model....")
    nlp = spacy.load('en_core_web_lg')
    print("spaCy successfully loaded")
    return nlp

def get_unique_product_ids(reviews_data):
    product_ids = []
    # product_ids = [r['product_id'] for r in reviews_data]
    return list(set(product_ids))

def get_aspects(reviews_data):
    aspects = []
    for review in reviews_data:
        aspect_pairs = review["aspect_pairs"]
        for map in aspect_pairs:
            aspects.append(map['noun'])
    return aspects

def get_aspect_freq_map(aspects):
    aspect_freq_map = defaultdict(int)
    for asp in aspects:
        aspect_freq_map[asp] += 1
    return aspect_freq_map

def get_unique_aspects(aspects):
    unique_aspects = list(set(aspects)) # use this list for clustering
    return unique_aspects
# @profile
def get_word_vectors(unique_aspects, nlp):
    asp_vectors = []
    for aspect in unique_aspects:
        # print(aspect)
        token = nlp(aspect)
        asp_vectors.append(token.vector)
    return asp_vectors
# @profile
def get_word_clusters(unique_aspects, nlp):
    # print("Found {} unique aspects for this product".format(len(unique_aspects)))
    asp_vectors = get_word_vectors(unique_aspects, nlp)
    if len(unique_aspects) <= NUM_CLUSTERS:
        # print("Too few aspects ({}) found. No clustering required...".format(len(unique_aspects)))
        return list(range(len(unique_aspects)))

    # print("Running k-means clustering...")
    n_clusters = NUM_CLUSTERS
    kmeans = cluster.KMeans(n_clusters=n_clusters)
    kmeans.fit(asp_vectors)
    labels = kmeans.labels_
    # dbscan = cluster.DBSCAN(eps = 0.2, min_samples = 2).fit(asp_vectors)
    # labels = dbscan.labels_

    # print("Finished running k-means clustering with {} labels".format(len(labels)))
    # print(labels)
    return labels
# @profile
def get_cluster_names_map(asp_to_cluster_map, aspect_freq_map):
    cluster_id_to_name_map = defaultdict()
    # cluster_to_asp_map = defaultdict()
    clusters = set(asp_to_cluster_map.values())
    for i in clusters:
        this_cluster_asp = [k for k,v in asp_to_cluster_map.items() if v == i]
        filt_freq_map = {k:v for k,v in aspect_freq_map.items() if k in this_cluster_asp}
        filt_freq_map = sorted(filt_freq_map.items(), key = lambda x: x[1], reverse = True)
        cluster_id_to_name_map[i] = filt_freq_map[0][0]

        # cluster_to_asp_map[i] = this_cluster_asp

    return cluster_id_to_name_map
# @profile
def add_clusters_to_reviews(reviews_data, prod_id, nlp):
    product_aspects = get_aspects(reviews_data)
    # print("Total aspects found: {}".format(len(product_aspects)))
    aspect_freq_map = get_aspect_freq_map(product_aspects)
    unique_aspects = aspect_freq_map.keys()
    # print("Running clustering on {} unique aspects".format(len(unique_aspects)))

    aspect_labels = get_word_clusters(unique_aspects, nlp)
    asp_to_cluster_map = dict(zip(unique_aspects, aspect_labels))
    cluster_names_map = get_cluster_names_map(asp_to_cluster_map, aspect_freq_map)
    updated_reviews = []

    for review in reviews_data:
        aspect_pairs_upd = []
        aspect_pairs = review["aspect_pairs"]
        for map in aspect_pairs:
            noun = map['noun']
            cluster_label_id = asp_to_cluster_map[noun]
            cluster_label_name = cluster_names_map[cluster_label_id]
            map['cluster'] = cluster_label_name
            aspect_pairs_upd.append(map)

        # assert len(result) == len(aspect_pairs)
        review['aspect_pairs'] = aspect_pairs_upd
        updated_reviews.append(review)
    result = {prod_id:updated_reviews}
    return result
# @profile
def update_reviews_data(reviews_data, nlp):
    updated_reviews = []
    ctr = 0
    print("Total number of unique products in this category: {}".format(len(reviews_data)))
    # no_asp_reviews = [r for r in reviews_data if len(r['aspect_pairs']) == 0]
    # print("Total reviews found with no aspect pairs: {}".format(len(no_asp_reviews)))

    for i,product in enumerate(reviews_data):
        for prod_id, this_product_reviews in product.items():
            # this_no_asp_reviews = [r for r in this_product_reviews if len(r['aspect_pairs']) == 0]
            # print("Total reviews found: {}. Reviews with no aspect pairs: {}".format(len(this_product_reviews), len(this_no_asp_reviews)))
            # print("\nRunning clustering for product ID - {}".format(prod_id))
            this_product_upd_reviews = add_clusters_to_reviews(this_product_reviews, prod_id, nlp)
            updated_reviews.append(this_product_upd_reviews)

        if ((i%10000 == 0) ):
            ctr += 1
            print("\n----------------***----------------")
            print("Updating results - batch {}".format(ctr))
            # print(updated_reviews)
            with open('results_file_4L.json', 'a') as f:
                json.dump(updated_reviews,f)
            updated_reviews = []
            print("Finished writing results to json!!")
            print("----------------***----------------")

    # Finally write to output file
    ctr += 1
    print("\n----------------***----------------")
    print("Updating results - batch {}".format(ctr))
    # print(updated_reviews)
    with open('results_file_4L.json', 'a') as f:
        json.dump(updated_reviews,f)
    updated_reviews = []
    print("Finished writing results to json!!")
    print("----------------***----------------")
# @profile
def main():
    # time1 = time()
    nlp = init_spacy()
    # sid = init_nltk()
    # time2 = time()
    print("----------------***----------------")
    print("\nLoading aspect pairs file")
    with open('src/data/reviews_mapping.json', 'r') as fobj:
        reviews_data = json.load(fobj)
    print("Finished loading aspect pairs!!\n")
    print("----------------***----------------")
    # time3 = time()
    update_reviews_data(reviews_data, nlp)
    # time4 = time()
    # print("Time for spacy loading: {0:.2}s".format(time2-time1))
    # print("Time for aspect extraction: {0:.2}s".format(time3-time2))
    # print("Time for aspect clustering: {0:.2}s".format(time4-time3))

if __name__ == '__main__' :
    main()
