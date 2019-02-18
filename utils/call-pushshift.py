"""
Author(s): Raunak Agarwal
File Created: 14/02/2019
Last Edit: 18/02/2019

Help: python3 call-pushshift.py -h

Example Usage:
python3 call-pushshift.py \
    -subreddit politics,europe,unitedkingdom,news,worldnews \
    -year 2010 \
    -query SCL_OPP_neg-Copy2.txt \
    -output all_SCL_OPP_neg_2010_18_2.json \
    -logfile all_SCL_OPP_neg_2010_18_2.txt
"""
import random
import time
import datetime
import argparse
import string 

import pandas as pd
import requests 
import regex as re

import textacy

BASE = "https://api.pushshift.io/reddit/search/comment/?q={q}&size=1000&\
fields=body,id,subreddit,created_utc,author,score,parent_id&before={before}&after={after}\
&&sort_type=score&sort=desc&nest_level=1&score=>20&subreddit={subreddit}"

def parse_args():
    """
    Parse CLI Arguments
    Params:
        None
    Return: 
        dict() - Relevant CLI Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-subreddit", help="Subreddits to Scrape", type=str)
    parser.add_argument("-year", help="Year", type=str)
    parser.add_argument("-query",help="Query File",type=str)
    parser.add_argument("-logfile",help="Log File",type=str)
    parser.add_argument("-output",help="JSON Directory for Output",type=str)
    argv = parser.parse_args()
    
    return argv

def get_ut(dt):
    """
    Return UT for a given DT
    Params: 
        dt - Datetime object
    Return: 
        int() - Unix timestamp for a datetime object
    """
    return int(time.mktime(dt.timetuple()))

def fetch_specific(start_ut,end_ut,query,subs,logfile):
    """
    Fetch from 'start_ut' to 'end_ut' for a specific query string
    Params:
        start_ut - int() - timestamp to start querying
        end_ut - int() - timestamp to terminate querying
        query - str() - query string for pushshift (can be an empty string)
        subs - str() - list of subreddits to query (separated by commas)
        logfile - str() - location of the logfile
    Return:
        pd.DataFrame - A Pandas DataFrame with preprocessed data
    """
    terminate_ut = end_ut
    cols = ['author','body','created_utc','id','score','subreddit','parent_id']
    s = pd.DataFrame(columns=cols)
    while start_ut < terminate_ut:
        time.sleep(0.2)
        ts = int(start_ut)
        end_ut = start_ut + random.randint(35000,100000)*50
        query = query.strip().replace(' ','+')
        url = BASE.format(
                before=end_ut,
                after=start_ut,
                subreddit=subs,
                q = query)
        try:
            def is_valid(resp):
                """Checks for Valid Responses"""
                return resp.status_code == 200 and resp.json() is not None

            response = requests.get(url)
            if is_valid(response):
                print("valid: ",query," ",ts)
                repeat = False
                response = response.json()
            else:
                repeat = True
            if repeat:
                for i in range(25):
                    response = requests.get(url)
                    print("Retrying: ",i," ",query," ",ts)
                    if is_valid(response):
                        response = response.json()
                        repeat = False
                        break
                if repeat:
                    print("invalid: ",query," ",ts)
                    start_ut = end_ut
                    continue
                
            d = pd.DataFrame(response['data'],columns=cols)
            d['valid'] = d['body'].apply(lambda x: x!='[deleted]' or x!='[removed]' or x is not None)
            d = d[d['valid'] == True]
            # d['len'] = d['body'].apply(lambda x: len(x))
            # d['valid_len'] = d['len'].apply(lambda x: x<=300 and x>=10)
            # d = d[d['valid_len'] == True]
            d = d[cols]
            d['body'] = d['body'].apply(lambda x: clean(x))
            d['valid_len'] = d['body'].apply(lambda x: len(x)>=10 and len(x)<=300)
            d = d[d['valid_len'] == True]
            d = d[cols]

            #print(ts)
            start_ut = end_ut
            with open(logfile,'a') as f:
                print(datetime.datetime.utcfromtimestamp(ts).strftime(
                    '%Y-%m-%d %H:%M:%S'),file=f)
                print(url,file=f)
                print("Total Comments Added: " + str(len(d)),file=f)
            s = s.append(d,ignore_index=True)
        except Exception as e:
            pass

    s = s.drop_duplicates(subset='id', keep="first")
    return s

def clean(text):
    """
    Preprocessor
    Params: 
        text - str() - text to preprocess
    Return: 
        text - str() - preprocessed text
    """
    parent_symbol = re.compile(r"&gt;.*?\\n\\n")
    user_symbol = re.compile(r"u/ *|r/| /user/*")
    text = re.sub(parent_symbol,"",text)
    text = user_symbol.sub("",text)

    puncts = string.punctuation.replace(".","")
    puncts = puncts.replace("?","").replace("!","").replace("\'","").replace(",","")
    translator = str.maketrans(puncts, ' '*len(puncts)) #map punctuation to space

    # url_re = re.compile(r'\[([^]]+)\]\(%%URL\)')
    link_re = re.compile(r'\[([^]]+)\]\(https?://[^\)]+\)')

    pre_format_re = re.compile(r'^[\`\*\~]')
    post_format_re = re.compile(r'[\`\*\~]$')

    text = link_re.sub(r'\1', text)
    text = text.replace('&gt;', '').replace('&lt;', '')
    text = pre_format_re.sub('', text)
    text = post_format_re.sub('', text)
    text = re.sub(r'\s+', ' ', text)
    # text = url_re.sub('',text)
    text = link_re.sub('',text)

    text = textacy.preprocess.preprocess_text(
                text, fix_unicode=True, 
                lowercase=False, transliterate=True, 
                no_urls=True, no_emails=True,
                no_phone_numbers=True, no_numbers=True, 
                no_currency_symbols=True, 
                no_punct=False, no_contractions=True, no_accents=False)
    text = text.translate(translator)
    text = textacy.preprocess.normalize_whitespace(text)
    return re.sub(" {2,}", " ", text.strip())

def query(n,queries,year,subreddit,logfile):
    """
    Set query range, iterate over queries doc. Uses fetch_specific()
    Params:
        n - str() - output filename
        queries - list(str) - list of queries
        year - str() - first year of queries
        subreddit - str() - list of subreddits to query (separated by commas)
        logfile - str() - location of the logfile
    Return:
        pd.DataFrame - A Pandas DataFrame with combined preprocessed data
    """
    start_ut = get_ut(datetime.datetime(int(year),1,1))
    end_ut = get_ut(datetime.datetime(2018,12,31))
    cols = ['author','body','created_utc','id','score','subreddit','parent_id']
    joined = pd.DataFrame(columns=cols)
    for i,q in enumerate(queries):
        print(q)
        d = fetch_specific(start_ut,end_ut,q,subreddit,logfile)
        joined = joined.append(d,ignore_index=True)
#         if i == 1:
#             break
        joined.to_json("temp_"+n,orient="records")
    joined = joined.drop_duplicates(subset='id', keep="first")
    
    return joined

if __name__ == "__main__":
    argv = parse_args()
    query_file = argv.query
    logfile = argv.logfile
    with open(query_file, 'r') as f:
        queries = f.read().splitlines()
    with open(logfile,'w') as log:
        print(argv,file=log)
    subreddits = argv.subreddit
    df = query(argv.output,queries,argv.year,argv.subreddit,logfile)
    df.to_json(argv.output,orient="records")

