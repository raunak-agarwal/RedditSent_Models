"""
Raunak Agarwal
File Created: 17/02/2019
Last Edit: 17/02/2019

python3 preprocess-pushshift.py -

"""
import argparse

import jsonlines
import spacy
import pandas as pd

nlu = spacy.load("en_core_web_sm")

def parse_args():
    """Parse CLI Arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-subreddit", help="Subreddits to Scrape", type=str)
    parser.add_argument("-year", help="Year", type=str)
    parser.add_argument("-query",help="Query File",type=str)
    parser.add_argument("-logfile",help="Log File",type=str)
    parser.add_argument("-output",help="JSON Directory for Output",type=str)
    argv = parser.parse_args()
    
    return argv

if __name__ == "__main__":
    argv = parse_args()
    query_file = argv.query
    logfile = argv.logfile
    with open(query_file, 'r') as f:
        queries = f.read().splitlines()
    with open(logfile,'w') as log:
        print(argv,file=log)
    df = pd.read_json("all_intersection_pos_2010_18.json")
    df['corpus_1'] = argv.corpus_1
    df['corpus_2'] = argv.corpus_2
    for index, row in df.iterrows():
        with jsonlines.open(argv.logfile,mode = "a") as f:
            f.write(row.to_dict())
    

