from collections import namedtuple
import bibtexparser as bibtex
from typing import List, Any, Dict

BibEntry = namedtuple('BibEntry', ['title', 'url'])

def bib_from_file(bib_path: str) -> List[Any]:
    with open(bib_path, "rb") as file:
        bib = bibtex.load(file)
    return bib.entries

def flatten_entries(entries: List[Dict[str, str]]) -> Dict[str, BibEntry]:
    ids = {}
    for entry in entries:
        assert entry['ID'] not in ids, f"Duplicate bib ID: {entry['ID']}"
        ids[entry['ID']] = BibEntry(entry['title'], entry['url'])
    return ids
