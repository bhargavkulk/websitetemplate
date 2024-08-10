import os
from datetime import datetime

from .markdown.citation import CitationExtension
from .bibliography import BibEntry
from .markdown.namelink import NameLinkExtension
from .utils import TomlExpr
import markdown
from typing import Dict, List, Tuple

News = Tuple[datetime, str]
NewsList = List[News]

def get_sorted_files(folder: str) -> NewsList:
    files = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            date_str = filename[:-3]  # remove the ".md" extension
            date = datetime.strptime(date_str, "%b-%Y")
            filepath = os.path.abspath(os.path.join(folder, filename))
            files.append((date, filepath))
    files.sort(reverse=True)  # sort from newest to oldest
    return files

def generate_news_lists(news_folder: str, mapping: Dict[str, str], entries: Dict[str, BibEntry]) -> NewsList:
    def generate_news_list(news_path: str) -> str:
        # Steps:
        # 1. Read .md from file
        with open(news_path, "r") as file:
            news_md = file.read()
        # 2. Convert .md to .html
        md = markdown.Markdown(extensions=[NameLinkExtension(mapping), CitationExtension(entries)])
        news_html = md.convert(news_md)
        # 3. [Optional] add style classes to .html
        # 4. Return with tuple
        return news_html

    news_files = get_sorted_files(news_folder)
    return [(timestamp, generate_news_list(news_file))
        for (timestamp, news_file) in news_files]
