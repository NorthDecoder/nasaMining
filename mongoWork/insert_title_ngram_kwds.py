import authenticate_to_mongo #local module


import json



db = authenticate_to_mongo.db_json_from_agency()

if __name__ == '__main__':
    data = json.load(open('data/nasa_title_ngram_np.json'))['dataset']

    for i, d in enumerate(data):
        if i and i % 100 == 0:
            print i

        db.datasets.update({'identifier': d['identifier']}, {'$set': {
            'title_ngram_np': d['title_ngram_np']
        }})