#!/usr/bin/env python3


import os
import pathlib
import sys

import chardet
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in
from whoosh.writing import AsyncWriter


if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

schema = Schema(
    title=TEXT(stored=True),
    path=ID(stored=True),
    content=TEXT,
    textdata=TEXT(stored=True),
)
ix = create_in("indexdir", schema)


def read_text(fpath):
    with open(fpath, "rb") as file_obj:
        data = file_obj.read()
        encoding = chardet.detect(data)["encoding"] or "latin1"
        return data.decode(encoding, errors="ignore")


def add_doc(path):
    writer = ix.writer()
    try:
        title = path.name
        print(f"Adding {title}")
        text = read_text(path)
        writer.add_document(title=title, path=str(path), content=text, textdata=text)
        print(f"Added {title} to index")

    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        writer.commit()


def createSearchableData(root):
    """
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    """
    if isinstance(root, str):
        root = pathlib.Path(root)
    try:
        [add_doc(path) for path in root.rglob("*.html")]
    except KeyboardInterrupt:
        return


root = "/var/www/html/site/files/Webs"
createSearchableData(root)
