import authenticate_to_mongo #local module

msg_verbocity = 'verbose'
db = authenticate_to_mongo.db_json_from_agency( msg_verbocity )

# description_ngram_np
if __name__ == '__main__':
    # res = db.datasets.find({}, {"_id": 0, "identifier": 1, "title": 1, "source": 1, "description_ngram_np": 1})
    res = db.datasets.find({}, {"_id": 0, "identifier": 1, "title": 1, "source": 1, "description_ngram_np": 1})

    keywords = []

    for r in res:
        for kw in r["description_ngram_np"]:
            keywords.append({
                "identifier": r["identifier"],
                "title": r["title"],
                "source": r["source"],
                "keyword": kw,
                "keywords_full": r["description_ngram_np"]
            })

    db.keywords.insert(keywords)

    db.keywords.create_index("keyword", background=True)
    db.keywords.create_index("source", background=True)
    db.keywords.create_index([
        ("keyword", pymongo.ASCENDING),
        ("source", pymongo.ASCENDING)
    ], background=True)

