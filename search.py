#!/usr/bin/env python3

from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

ix = open_dir("indexdir")


def search(query_str, top=10):
    query_str = f"*{query_str}*"
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("title", ix.schema).parse(query_str)
        for result in searcher.search(query):
            # yield result["title"]
            yield result["textdata"]
        # print(results[title'], str(results[.score), results[i]['textdata'])


def all_docs():
    for doc in ix.searcher().documents():
        yield doc["title"]


if __name__ == "__main__":
    import sys

    query = sys.argv.pop()
    if sys.argv:
        name = sys.argv.pop()
        results = search(query)
        print(name, query)
        for res in results:
            print(res)
