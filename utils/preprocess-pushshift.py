"""
Raunak Agarwal
File Created: 17/02/2019
Last Edit: 17/02/2019

python3 preprocess-pushshift.py -

"""
import argparse
import json

import jsonlines
import spacy
import pandas as pd

from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_lg")

def parse_args():
    """Parse CLI Arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-infile",help="Pushshift Dump To Preprocess",type=str)
    parser.add_argument("-corpus_1",default="None",help="Label 1 to Add",type=str)
    parser.add_argument("-corpus_2",default="None",help="Label 2 to Add",type=str)
    parser.add_argument("-outfile",help="Directory for Output JSONL",type=str)
    parser.add_argument("-ignore",default="None",help="File for terms to ignore",type=str)
  
    argv = parser.parse_args()
    
    return argv

def preprocess_df(data):
    new_data = pd.DataFrame()
    def generate_sents(data):
        """
        generator function to read in sents from the dataframe
        """
        for body in data['body']:
            yield str(body)
    def preprocess_sents(data):
        for i,doc in enumerate(nlp.pipe(generate_sents(data),batch_size=1000, n_threads=-1)):
            row = data.loc[i]
            noun_chunks = [tok for chunk in doc.noun_chunks for tok in chunk.lower_.split() if tok not in STOP_WORDS]
            ents = []
            relations = []
            for ent in filter(lambda w: w.ent_type_, doc):
                ents.append((ent,ent.ent_type_))
                if ent.dep_ in ('attr', 'dobj'):
                    subject = [w for w in ent.head.lefts if w.dep_ == 'nsubj']
                    if subject:
                        subject = subject[0]
                        relations.append((subject, ent))
                elif ent.dep_ == 'pobj' and ent.head.dep_ == 'prep':
                    relations.append((ent.head.head, ent))
            row['ent'] = ents if len(ents) else None
            row['ent_phrases'] = relations if len(relations) else None
            row['chunks'] = noun_chunks if len(noun_chunks) else None
            nonlocal new_data
            new_data = new_data.append(row)
            if not i % 1000: print(i)
            # if i==100:
            #     return new_data
        return new_data
    return(preprocess_sents(data))
# test = preprocess_df(data[:100])
# print(test['chunks'])
def operate(df,fname):
    df = preprocess_df(df)
    df.astype(str).to_json(fname,orient="records",lines=True)
    return set(df['id'])

    # for index, row in df.iterrows():
        # with jsonlines.open(argv.outfile,mode = "a") as f:
        #     f.write(json.dumps(row.to_dict()))
        
    
if __name__ == "__main__":
    argv = parse_args()
    infile = argv.infile
    outfile = argv.outfile
    df = pd.read_json(infile,orient='records')
    df = df.drop_duplicates(subset='id', keep="first")
    df = df.reset_index(drop=True)
    print(df.shape)
    df['corpus_1'] = argv.corpus_1
    df['corpus_2'] = argv.corpus_2
    print(argv.ignore)
 
    if argv.ignore == "None":
        ids = operate(df,outfile)
    else:
        with open(argv.ignore, "r") as f:
            ignore_ids = f.read().splitlines()
        print(ignore_ids)
        ids = set(df['id'])
        ignore_ids = set(ignore_ids)
        if ids & ignore_ids:
            print("match")
            print(len(df))
            df = df[~df['id'].isin(ignore_ids)]
            print(len(df))
            df = df.reset_index(drop=True)
        ids = operate(df,outfile)
        with open(argv.ignore, 'a') as f:
            for item in ids:
                f.write("%s\n" % item)

