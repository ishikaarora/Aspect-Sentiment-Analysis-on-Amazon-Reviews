import pandas as pd
from sys import argv

#Input file name as argv to run
file_name = str(argv[1])

def read_data():
    return pd.read_csv(file_name,
        sep = "\t", header=0, error_bad_lines = False)

if __name__ == '__main__':
    df = read_data()
    df = df[df['review_body'].notna()]
    df['review_body'] = df['review_body'].str.replace("<br />", "")
    df['review_body'] = df['review_body'].str.replace("\[?\[.+?\]?\]", "")
    df['review_body'] = df['review_body'].str.replace("\/{3,}", " ")
    df['review_body'] = df['review_body'].str.replace("\&\#.+\&\#\d+?;", "")
    df['review_body'] = df['review_body'].str.replace("\d+\&\#\d+?;", "")
    df['review_body'] = df['review_body'].str.replace("\&\#\d+?;", "")

    #facial expressions
    df['review_body'] = df['review_body'].str.replace("\:\|", "")
    df['review_body'] = df['review_body'].str.replace("\:\)", "")
    df['review_body'] = df['review_body'].str.replace("\:\(", "")
    df['review_body'] = df['review_body'].str.replace("\:\/", "")

    #replace multiple spaces with single space
    df['review_body'] = df['review_body'].str.replace("\s{2,}", " ")

    df['review_body'] = df['review_body'].str.lower()

    out_name = "CLEANED_"+file_name

    df.to_csv(out_name, sep='\t', index=False)



