"""
   # file: extract.py

   > Original contributor: github.com/MattL920

   ### usage:


   ### Reference

   1. ../readme.md
   2. Topic modeling for humans[Gensim](https://radimrehurek.com/gensim)
   3. Natural Language Toolkit [NLTK](https://nltk.org
"""

from __future__ import unicode_literals
import json
from gensim.models.phrases import Phrases
from textblob import TextBlob
import nltk
print(63*"*")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
print(63*"*")
import pickle
import argparse
import logging
logging.basicConfig(  level=logging.DEBUG )
import time

def parse_input(input_json, input_source=None):
    print( '\n', input_json, ': Tokenizing descriptions' )
    print( '-------------------------------------------\n')
    desc = []
    doc_id = []
    dataset = json.load(open(input_json))['dataset']

    for i, ds in enumerate(dataset):
        if input_source:
            ds['source'] = input_source

        text = TextBlob(ds['description'])
        for sentence in text.sentences:
            desc.append(sentence.tokens)
            doc_id.append(i)

    return dataset, desc, doc_id


def construct_ngrams(desc, desc_seed=None, phrase_passes=5, phrase_threshold=10, model_output=None):
    models = []
    desc_seed = desc_seed or []

    memory_intensive = "Function gensim Phrases is memory intensive \n" \
                     + "and if it consumes all of the memory it will \n" \
                     + "crash this script without warning.  \n"

    problem_resolution = "View a pre-crash failure report with filprofiler. \n" \
                       + "See https://pythonspeed.com/fil/docs/index.html. \n" \
                       + "One possible way to eliminate the crashing is to \n" \
                       + "set up virtual swap memory. Another, is to \n"\
                       + "run the script on a server with more memory. \n" \
                       + "Guess how much memory is needed? "

    logging.warning( memory_intensive + problem_resolution + "\n")

    print( '\nConstructing ngrams' )
    print( '--------------------')
    for i in range(phrase_passes):
        print( '\t', "phrase_pass: ",i )
        model = Phrases(desc + desc_seed if i == 0 else desc, threshold=phrase_threshold)
        desc = model[desc]
        models.append(model)

    if model_output:
        with open(model_output, 'wb+') as f:
            pickle.dump(models, f)

    return desc


def extract(ngrams, dataset, doc_id):
    # extract keywords
    print( '\nExtracting keywords' )
    print( '-------------------')
    for i, ngram in enumerate(ngrams):
        doc = doc_id[i]

        if field not in dataset[doc]:
            dataset[doc][field] = set()

            if doc > 0 and doc % 1000 == 0:
                print( '\t', doc )

        for kw in filter(lambda k: '_' in k, ngram):
            keyword = kw.replace('_', ' ')

            kw_tb = TextBlob(keyword)

            # filter out punctuation, etc (make sure that there are two non-punc words)
            if len(kw_tb.words) < 2:
                continue

            # add keywords which are all proper nouns
            distinct_tags = set(t[1] for t in kw_tb.tags)
            if distinct_tags - {'NNP', 'NNPS'} == {}:
                dataset[doc][field].add(kw_tb.lower())
                continue

            # add noun phrases
            for np in kw_tb.lower().noun_phrases:
                dataset[doc][field].add(np)

    return kw_set_to_list(dataset)


def kw_set_to_list(dataset):
    # convert set into list for json serialization
    for d in dataset:
        d[field] = list(d[field])

        # fix 's
        for i, np in enumerate(d[field]):
            if np.endswith(" 's"):
                np = np[:-3]

            if np.startswith("'s "):
                np = np.replace("'s ", "", 1)

            np = np.replace(" 's", "'s")

            d[field][i] = np
        d[field] = list(set(d[field]))

    return dataset


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description='SpaceTag keyword extraction')
    parser.add_argument('-i', "--input", type=str, default='data.json', help='path to a data.json format file')
    parser.add_argument('-s', "--source", type=str, default="", help='data source annotation (e.g. data.nasa.gov/data.json')
    parser.add_argument('-o', "--output", type=str, default='keywords.json', help='path to output the data with extracted keywords')
    parser.add_argument('-f', "--field", type=str, default='description_ngram_np', help='field in each dataset to store the keywords')
    parser.add_argument('-m', "--model", type=str, default='models.pkl', help='file to save the pickled phrase extraction models')
    parser.add_argument('-p', "--passes", type=int, default=5, help="number of phrase extraction passes to make")
    parser.add_argument('-t', "--threshold", type=int, default=10, help="phrase extraction significance threshold")
    parser.add_argument("--seed", type=str, default=None, help="path to a data.json to seed the phrase extraction statistics with")

    args = parser.parse_args()

    input_json = args.input
    input_source = args.source
    seed_json = args.seed
    output_file = args.output
    model_output = args.model
    field = args.field
    phrase_passes = args.passes
    phrase_threshold = args.threshold

    # input_json = 'data/defense.json'
    # input_source = 'defense.gov/data.json'
    # seed_json = 'data/nasa.json'
    # output_file = 'data/defense_ngram_np2.json'
    # model_output = 'models.pkl'
    # field = 'description_ngram_np'
    # phrase_passes = 5
    # phrase_threshold = 10

    # parse input data
    dataset, desc, doc_id = parse_input(input_json, input_source)

    # parse secondary seed data
    desc_seed = []
    if seed_json:
        _, desc_seed, _ = parse_input(seed_json)

    ngrams = construct_ngrams(desc, desc_seed, phrase_passes, phrase_threshold, model_output)

    dataset = extract(ngrams, dataset, doc_id)

    with open(output_file, 'w') as f:
        json.dump(dataset, f)
        print( '\nkeywords written to: ', output_file )

    end_time = time.time()

    print("in ", round( ( end_time - start_time )/60  , 2 )   , " minutes.")
