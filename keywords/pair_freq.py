from __future__ import unicode_literals
import argparse
import json, operator
from itertools import combinations
import logging
logging.basicConfig(  level=logging.DEBUG )
from math import log

#

class Helper:
    def __init__(self):
        ''' Help for pair_freq.py '''

    def pair_freq_augmented_help():
        '''
        # Keyword pair frequency count

        > Original contributor: flava flav

        ## Overview

        Generate a list of frequency counts for keyword pairs,
        sorted in reverse order by total.

        The script pair_freq.py is user configurable by
        command line arguments which determine
        where to acquire the input data file,
        the field in the input file to acquire the keywords,
        and the name and path of the output file.

        The script is generic and can be used on
        any dataset that is in the expected input
        format.  The default is to look for the
        nasaMining inputs, however the default
        inputs can be changed to the desired input
        with the arguments.

        ## Usage

        cd keywords
        python3 pair_freq.py \\
                --input ../data/nasa_keywords.json \\
                --field ngram_keywords \\
                --output ../data/nasa_np_strengths.json

        ## Inputs

        The format of the json input file is expected
        to be like:
                    {"dataset":[{},{},{}]}
        OR
                    [{},{},{}]

        Each object in the json array must have a
        name which can be identified by the argument
        something like:

        --field ngram_keywords

        [ {"ngram_keywords":["real-time","sea surface","temperature"]},
          {"ngram_keywords":["foundation","sea surface","temperature"]},
          {"ngram_keywords":["global","distribution","node"]}
        ]

        Choose a field name that matches what you
        are inspecting.

        ## Output

        The format of the json output file will be like
        [{},{},{}]

        Each object of the json array will have data something like
        {"count": 340.0,
         "a": 7492,
         "b": 7492,
         "keyword": ["soil moisture accuracy", "soil moisture algorithm performance"],
         "pmi_doc": -1.6840664693580758,
         "pmi_kw": -1.7938470459262326
        }


        ## Reference

        - Acronyms
          - np:   noun phrase
          - pmi:  pointwise mutual information
          - dpmi: dataset pointwise mutual information
          - kpmi: keyword pointwise mutual information

        - 6.6 Pointwise Mutual Information, pdf pg 109
          - Speech and Language Processing, 3rd Edition draft,
            Daniel Jurafsky, Stanford University

        - [Noun Phrase](https://en.wikipedia.org/wiki/Noun_phrase)
           a phrase that has a noun or pronoun as its head


        '''
#

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyword pair frequency extraction')

    parser.add_argument('-i', "--input", type=str, default='../data/nasa_keywords.json', \
                         help='path to a data.json format file containing keyword ngrams')

    parser.add_argument('-f', "--field", type=str, default='ngram_keywords', \
                         help='field in the dataset in which to find the keywords')

    parser.add_argument('-o', "--output", type=str, default='../data/nasa_np_strengths.json', \
                         help='path to output the data with extracted keywords')

    parser.add_argument("--augmented_help", action='store_true', default="", \
                         help="Verbose help")


    args = parser.parse_args()

    if args.augmented_help:
        help( Helper.pair_freq_augmented_help )
        exit()

    path_to_input_json  = args.input
    path_to_output_json = args.output
    kw_field            = args.field

    #

    data = json.load( open( path_to_input_json )  )

    try:
        dataset = data['dataset']
    except TypeError as e:
        logging.info( "TypeError:")
        logging.info( e )
        logging.info("Hint: keyword name `dataset` is not available in the input,")
        logging.info("attempting to access the list directly.")
        dataset = data

    keyholder = {}
    outdata = []

    pairs = {}
    single_words = {}

    #

    for i, ds in enumerate(dataset):
        for pair in combinations(ds[kw_field], 2):

            sl_pair = sorted( [x.lower() for x in pair], key=str.lower )

            if sl_pair[0] != sl_pair[1]:
                # if there are projects with duplicate
                # keywords in the metadata

                key = str(sl_pair)
                keyholder[key] = sl_pair
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 1;

                # left word
                if sl_pair[0] in single_words:
                    single_words[sl_pair[0]] += 1
                else:
                    single_words[sl_pair[0]] = 1

                # right word, probly a better way to do this
                if sl_pair[1] in single_words:
                    single_words[sl_pair[1]] += 1
                else:
                    single_words[sl_pair[1]] = 1

    #

    for pair, count in sorted(pairs.items(), key=operator.itemgetter(1), reverse=True):
        cA = single_words[keyholder[pair][0]] # total count of the first word
        cB = single_words[keyholder[pair][1]] # total count of the second word
        cAB = float(count)

        # If A and B only occur together once (this happens),
        # then avoid a ZeroDivisionError.

        # If A and B individually each appear only 1 time,
        # then this is significant (set to 1),
        # otherwise it is probably not significant at all (set to 0)

        if cAB == 1:
            if cA == 1 and cB == 1:
                dpmi = 1
                kpmi = 1
            else:
                dpmi = 0
                kpmi = 0
        else:
            dpmi = log((cAB * len(dataset)) / (cA * cB), 10) / -1 * log(cAB / len(dataset), 10)
            kpmi = log((cAB * len(single_words)) / (cA * cB), 10) / -1 * log(cAB / len(single_words), 10)
        outdata.append({'keyword': keyholder[pair], \
                          'count': cAB, \
                              'a': cA, \
                              'b': cB, \
                        'pmi_doc': dpmi, \
                         'pmi_kw': kpmi})

    with open( path_to_output_json, 'w' ) as f:
        json.dump(outdata, f)

    length_of_outdata_list = len( outdata  )

    msg = "Saving " + str( length_of_outdata_list ) \
                    + " records into a json array to file " \
                    + path_to_output_json

    logging.info( msg )

