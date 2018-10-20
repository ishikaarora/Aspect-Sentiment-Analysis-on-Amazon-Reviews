# Script to be run on all the downloaded files to understand contents, etc getcwd

import requests
import os
import csv
import numpy as np
import pandas as pd
import urllib.request
import gzip
import sys


BASE_PATH = os.getcwd() # base path of project
DATA_PATH = BASE_PATH + "/data/raw/"



def load_data(file_path, nrow_limit = None) :
    raw_data = pd.read_table(file_path,error_bad_lines=False, nrows=nrow_limit)
    return raw_data

def get_dtypes(df):
    return df.dtypes


#TODO
# 1. NAs in all columns

def runall_tests(file):



def create_summary_file(df):
