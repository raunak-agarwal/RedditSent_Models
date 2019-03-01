# RedditSent Models

This project is created as a part of the Advanced Natural Language Processing (ANLP 2018) course at Universität Potsdam, Germany.   

## Setup

`sudo apt-get install python3-venv`

`virtualenv --python=python3.6 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## 1. Benchmarking against the *SARC* dataset 

Self-Annotated Reddit Corpus [(*SARC*)](https://github.com/NLPrinceton/SARC) is the largest publicly available annotated corpus for reddit comments. We utilise comments from the balanced section of the corpus to benchmark our future models. 


## 2. Building Corpora via *Pushshift*

[*Pushshift*](http://pushshift.io/) is a free service that ingests real-time comments from Reddit. We query its API to create a corpus of comments from 5 of the biggest English-language political subreddits - [r/politics](http://reddit.com/r/politics), [r/news](http://reddit.com/r/news/), [r/worldnews](http://reddit.com/r/worldnews/), [r/unitedkingdom](http://reddit.com/r/unitedkingdom), [r/europe](http://reddit.com/r/europe/). The corpus is available [**here**](https://tinyurl.com/y5rkylj4).


1. [Lexicons](docs/lexicons.md)
2. [Data Scrape](docs/data.md)
3. [Filtering and Preprocessing](docs/preprocessing.md)
4. [Word Vectors](docs/vectors.md)

## 3. Data Annotation using *Prodigy* 

Using the corpus created above, we annotate a subset of comments from [r/politics](https://reddit.com/r/politics/). To perform data annotation, we use [*Prodigy*](https://prodi.gy/). 


![Prodigy](img/prodigy-example.gif)

**Note**: Prodigy is not a free software


[Try Prodigy](https://redditsent-corpus.serveo.net/) with our r/politics corpus. 


