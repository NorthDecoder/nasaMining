from __future__ import unicode_literals
import json


from collections import Counter, defaultdict




db = authenticate_to_mongo.db_json_from_agency()

if __name__ == '__main__':
    counts = Counter()
    collocs = defaultdict(set)

    for i, kwds in enumerate(db.datasets.find({'source': 'http://data.nasa.gov/data.json'}, {'_id': 0, 'keyword': 1})):
        if i and i % 1000 == 0:
            print i

        counts.update(kwds['keyword'])

        for kw in kwds['keyword']:
            collocs[kw] |= set(kwds['keyword']) - {kw}

    # collocs = dict(sorted(collocs.items(), key=lambda c: len(c)))

    collocs = sorted([(v1, list(v2)) for v1, v2 in collocs.items()], key=lambda v_: len(v_[1]), reverse=True)

    json.dump(counts, open('kw_counts_orig.json', 'w'))
    json.dump(collocs, open('kw_collocations_orig.json', 'w'))

    print 'Done'