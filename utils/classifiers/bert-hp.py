import argparse
import pandas as pd

from flair.hyperparameter.param_selection import TextClassifierParamSelector, OptimizationValue
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, CharLMEmbeddings, ELMoEmbeddings
from flair.embeddings import DocumentLSTMEmbeddings, CharacterEmbeddings, BertEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path
from flair.optim import AdamW, SGDW

from hyperopt import hp
from flair.hyperparameter.param_selection import SearchSpace, Parameter
from flair.hyperparameter.param_selection import TextClassifierParamSelector, OptimizationValue


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-input", help="Input Directory", type=str)
	parser.add_argument("-output", help="Output Directory String", type=str)
	argv = parser.parse_args()
	return argv

if __name__ == "__main__":
    args = parse_args()

    corpus = NLPTaskDataFetcher.load_classification_corpus (
        Path(args.input), test_file='test.csv', train_file='train.csv',dev_file='dev.csv')
    
    search_space = SearchSpace()
    search_space.add(Parameter.EMBEDDINGS, hp.choice,
                     options=[[WordEmbeddings('en-twitter')], [WordEmbeddings('en-crawl')],[WordEmbeddings('extvec')],
                               [WordEmbeddings('extvec'), BertEmbeddings('bert-base-uncased')],
                               [WordEmbeddings('en-crawl'), BertEmbeddings('bert-base-uncased')],
                            [WordEmbeddings('en-twitter'), BertEmbeddings('bert-base-uncased')]])
    search_space.add(Parameter.HIDDEN_SIZE, hp.choice, options=[32, 64, 128, 512])
    search_space.add(Parameter.RNN_LAYERS, hp.choice, options=[1, 2])
    search_space.add(Parameter.DROPOUT, hp.uniform, low=0.0, high=0.5)
    search_space.add(Parameter.LEARNING_RATE, hp.choice, options=[0.05, 0.1, 0.15, 0.2])
    search_space.add(Parameter.MINI_BATCH_SIZE, hp.choice, options=[8, 16, 32])

    

    # create the parameter selector
    param_selector = TextClassifierParamSelector(
        corpus, 
        False, 
        args.output, 
        'lstm',
        max_epochs=60, 
        training_runs=3,
        optimization_value=OptimizationValue.DEV_SCORE
    )

    # start the optimization
    param_selector.optimize(search_space, max_evals=100)

