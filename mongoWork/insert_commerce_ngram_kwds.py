import authenticate_to_mongo #local module


import json



db = authenticate_to_mongo.db_json_from_agency()

if __name__ == '__main__':
    data = json.load(open('data/commerce_ngram_np.json'))

    db.datasets.insert(data)