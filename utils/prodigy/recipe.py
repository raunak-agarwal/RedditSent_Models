"""
Custom Multilabel Prodigy Trainer

PRODIGY_PORT=8085 prodigy textcat.teach partd en_core_web_sm partitionad.jsonl \
-F recipe_2.py --label positive,negative,neutral,sarcastic,non-sarcastic
"""
import prodigy
from prodigy.models.textcat import TextClassifier
from prodigy.components.sorters import prefer_uncertain
from prodigy import recipe, get_stream
import spacy
from prodigy import set_hashes

@recipe('textcat.teach',
    dataset=prodigy.recipe_args['dataset'],
    spacy_model=prodigy.recipe_args['spacy_model'],
    source=prodigy.recipe_args['source'],
    label=prodigy.recipe_args['label_set']
    )
def teach(dataset, spacy_model, source,label):
    print(dataset,source,spacy_model,label)
    nlp = spacy.load(spacy_model, disable=['tagger', 'parser', 'ner']) 
    stream = get_stream(source,loader='jsonl')
    stream = filter_stream(stream)
    stream = add_options(stream)
    print(stream)
    model = TextClassifier(nlp, label) #multilabel CNN
    # components = teach(dataset=dataset, spacy_model=spacy_model,label=label, source=stream)
    return {
        'dataset': dataset,
        'view_id': 'choice',
        'patterns': 'data/terms.jsonl',
        'stream': prefer_uncertain(model(filter_stream(stream))),
        'update': model.update,
        "choice_style": "multiple",
        'config': {'lang': nlp.lang, 'label': model.labels}
    }

def filter_stream(stream):
    seen = set()
    for eg in stream:
        eg = set_hashes(eg)
        input_hash = eg['_task_hash']
        print(input_hash)
        if input_hash not in seen:
            seen.add(input_hash)
            yield eg

def add_options(stream):
    """Helper function to add options to every task in a stream."""
    options = [{'id': 'positive', 'text': '😄 positive'},
               {'id': 'negative', 'text': '😞 negative'},
               {'id': 'neutral', 'text': '😐 neutral'},
               {'id':'sarcastic','text': '🙃 sarcastic'},
               {'id':'non-sarcastic','text': '🤔 non-sarcastic'}]
    for task in stream:
        task['options'] = options
        yield task