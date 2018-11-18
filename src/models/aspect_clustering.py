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
NUM_CLUSTERS = 5

from src.models import aspect_extraction

def init_spacy():
    print("\nLoading spaCy Model....")
    nlp = spacy.load('en_core_web_lg')
    print("spaCy successfully loaded")
    return nlp

def get_reviews_data(nlp):
    print("----------------***----------------")
    print("\nExtracting aspect pairs")
    reviews_data = aspect_extraction.aspect_extraction(nlp)
    print("Finished running aspect extraction!!\n")
    print("----------------***----------------")
    return reviews_data

def get_unique_product_ids(reviews_data):
    product_ids = []
    product_ids = [r['product_id'] for r in reviews_data]
    return list(set(product_ids))

def get_aspects(reviews_data):
    aspects = []
    for review in reviews_data:
        aspect_pairs = review["aspect_pairs"]
        for noun,_,_ in aspect_pairs:
            aspects.append(noun)
    # aspects = [r['aspect_pairs'][0] for r in reviews_data]
    return aspects

def get_aspect_freq_map(aspects):
    aspect_freq_map = defaultdict(int)
    for asp in aspects:
        aspect_freq_map[asp] += 1
    return aspect_freq_map

def get_unique_aspects(aspects):
    unique_aspects = list(set(aspects)) # use this list for clustering
    return unique_aspects


def get_word_vectors(unique_aspects, nlp):
    asp_vectors = []
    for aspect in unique_aspects:
        # print(aspect)
        token = nlp(aspect)
        asp_vectors.append(token.vector)
    return asp_vectors

def get_word_clusters(unique_aspects, nlp):
    print("Found {} unique aspects for this product".format(len(unique_aspects)))
    asp_vectors = get_word_vectors(unique_aspects, nlp)
    # n_clusters = min(NUM_CLUSTERS,len(unique_aspects))
    if len(unique_aspects) <= NUM_CLUSTERS:
        print("Too few aspects ({}) found. No clustering required...".format(len(unique_aspects)))
        return list(range(len(unique_aspects)))

    print("Running k-means clustering...")
    n_clusters = NUM_CLUSTERS
    kmeans = cluster.KMeans(n_clusters=n_clusters)
    kmeans.fit(asp_vectors)
    labels = kmeans.labels_
    print("Finished running k-means clustering with {} labels".format(len(labels)))
    return labels

def get_cluster_names_map(asp_to_cluster_map, aspect_freq_map):
    cluster_id_to_name_map = defaultdict()
    # cluster_to_asp_map = defaultdict()
    n_clusters = len(set(asp_to_cluster_map.values()))
    for i in range(n_clusters):
        this_cluster_asp = [k for k,v in asp_to_cluster_map.items() if v == i]
        filt_freq_map = {k:v for k,v in aspect_freq_map.items() if k in this_cluster_asp}
        filt_freq_map = sorted(filt_freq_map.items(), key = lambda x: x[1], reverse = True)
        try:
            cluster_id_to_name_map[i] = filt_freq_map[0][0]
        except IndexError:
            print("Filtered freq map: {}".format(str(filt_freq_map)))
        # cluster_to_asp_map[i] = cluster_nouns

    # print(cluster_to_asp_map)
    return cluster_id_to_name_map

def add_clusters_to_reviews(reviews_data, nlp):
    product_aspects = get_aspects(reviews_data)
    print("Total aspects found: {}".format(len(product_aspects)))
    aspect_freq_map = get_aspect_freq_map(product_aspects)
    unique_aspects = aspect_freq_map.keys()
    # print("Runnig clustering on {} unique aspects".format(len(unique_aspects)))

    aspect_labels = get_word_clusters(unique_aspects, nlp)
    asp_to_cluster_map = dict(zip(unique_aspects, aspect_labels))
    cluster_names_map = get_cluster_names_map(asp_to_cluster_map, aspect_freq_map)

    for review in reviews_data:
        cluster_mapping = []
        aspect_pairs = review["aspect_pairs"]
        for noun,_,_  in aspect_pairs:
            cluster_label_id = asp_to_cluster_map[noun]
            cluster_label_name = cluster_names_map[cluster_label_id]
            cluster_mapping.append(cluster_label_name)

        assert len(cluster_mapping) == len(aspect_pairs)
        review['clusters'] = cluster_mapping
    # all_label_ids = []
    # for asp in all_aspects:
    #     this_label = asp_to_cluster_id_map[asp]
    #     this_label_name = cluster_names_map[this_label]
    #     all_label_ids.append(this_label)
    #     all_label_names.append(this_label_name)

    return reviews_data

def update_reviews_data(reviews_data):
    updated_reviews = []
    product_ids = get_unique_product_ids(reviews_data)
    print("Total number of unique products in this category: {}".format(len(product_ids)))

    no_asp_reviews = [r for r in reviews_data if len(r['aspect_pairs']) == 0]
    print("Total reviews found with no aspect pairs: {}".format(len(no_asp_reviews)))

    for prod_id in product_ids:
        print("\nRunning clustering for product ID - {}".format(prod_id))
        this_product_reviews = [r for r in reviews_data if r['product_id'] == prod_id]
        this_no_asp_reviews = [r for r in this_product_reviews if len(r['aspect_pairs']) == 0]
        print("Total reviews found: {}. Reviews with no aspect pairs: {}".format(len(this_product_reviews), len(this_no_asp_reviews)))

        add_clusters_to_reviews(this_product_reviews, nlp)
        updated_reviews.extend(this_product_reviews)

    print("\n----------------***----------------")
    print("Updating final results")
    with open('results_file_1000.txt', 'w') as f:
        for item in updated_reviews:
            f.write("%s\n" % item)
    print("Finished writing results to txt!!")
    print("----------------***----------------")

if __name__ == '__main__' :
    time1 = time()
    nlp = init_spacy()
    time2 = time()
    reviews_data = get_reviews_data(nlp)
    time3 = time()
    update_reviews_data(reviews_data)
    time4 = time()
    print("Time for spacy loading: {0:.2%}s".format(time2-time1))
    print("Time for aspect extraction: {0:.2%}s".format(time3-time2))
    print("Time for aspect clustering: {0:.2%}s".format(time4-time3))
