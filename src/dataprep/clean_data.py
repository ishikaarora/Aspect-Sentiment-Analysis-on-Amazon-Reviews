import pandas as pd
from sys import argv

#Input file name as argv to run

#Achyut - Commenting this out because repeated
# def read_data():
#     return pd.read_csv(file_name,
#         sep = "\t", header=0, error_bad_lines = False)

def clean_data(df):

    pd.options.mode.chained_assignment = None

    print("******Cleaning Started*****")

    print(f'Shape of df before cleaning : {df.shape}')
    df['review_date'] = pd.to_datetime(df['review_date'])
    df = df[df['review_body'].notna()]
    df['review_body'] = df['review_body'].str.replace("<br />", " ")
    df['review_body'] = df['review_body'].str.replace("\[?\[.+?\]?\]", " ")
    df['review_body'] = df['review_body'].str.replace("\/{3,}", " ")
    df['review_body'] = df['review_body'].str.replace("\&\#.+\&\#\d+?;", " ")
    df['review_body'] = df['review_body'].str.replace("\d+\&\#\d+?;", " ")
    df['review_body'] = df['review_body'].str.replace("\&\#\d+?;", " ")

    #facial expressions
    df['review_body'] = df['review_body'].str.replace("\:\|", "")
    df['review_body'] = df['review_body'].str.replace("\:\)", "")
    df['review_body'] = df['review_body'].str.replace("\:\(", "")
    df['review_body'] = df['review_body'].str.replace("\:\/", "")

    #replace multiple spaces with single space
    df['review_body'] = df['review_body'].str.replace("\s{2,}", " ")

    df['review_body'] = df['review_body'].str.lower()
    print(f'Shape of df after cleaning : {df.shape}')
    print("******Cleaning Ended*****")


    return(df)
#
# if __name__ == '__main__':
#     #file_name = str(argv[1])
#     #df = read_data()
#
#
#     out_name = "CLEANED_"+file_name
#
#     df.to_csv(out_name, sep='\t', index=False)
