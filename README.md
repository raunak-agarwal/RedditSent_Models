# RedditSent Models

This project is created as a part of the Advanced Natural Language Processing (ANLP 2018) course at Universität Potsdam, Germany.   

## Setup

`sudo apt-get install python3-venv`

`virtualenv --python=python3.6 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## 1. Benchmarking against the *SARC* dataset 

Self-Annotated Reddit Corpus [(*SARC*)](https://github.com/NLPrinceton/SARC) is the largest publicly available annotated corpus for reddit comments. We utilise comments from the balanced section of the corpus to benchmark our future algorithms. 


## 2. Building Corpora With *Pushshift*

1. [Lexicons](docs/lexicons.md)
2. [Data Scrape](docs/data.md)
3. [Filtering and Preprocessing](docs/preprocessing.md)
4. [Word Vectors](docs/vectors.md)

## 3. Data Annotation through *Prodigy* 

![Prodigy](img/prodigy-example.gif)

[Try Prodigy](https://redditsent-corpus.serveo.net/) with our r/politics corpus. 

