from os.path import abspath
from io import StringIO
from datetime import datetime
from src.news import generate_news_lists
from src.namelist import gen_name_lists
from src.utils import gen_website_list
from src.bibliography import bib_from_file, flatten_entries
from mako.runtime import Context
from mako.template import Template

INDEX_TEMPLATE: Template = Template(filename=abspath("./templates/index.html"))
NEWS_TEMPLATE: Template = Template(filename=abspath("./templates/news.html"))

BIB_ENTRIES = flatten_entries(bib_from_file(abspath("./data/references.bib")))

LEVELS = ["faculty", "grads", "ras", "ugrads", "groups"]

website_list = gen_website_list(abspath("./data/names"), LEVELS)
name_lists = gen_name_lists(abspath("./data/names"), abspath("./templates/name_list.html"), LEVELS)
news_list = generate_news_lists(abspath("./data/news"), website_list, BIB_ENTRIES)

recent_news = news_list[0]

index = StringIO()
index_ctx = Context(index, recent_news=recent_news, **name_lists)

news = StringIO()
news_ctx = Context(news, news_list=news_list)

INDEX_TEMPLATE.render_context(index_ctx)
NEWS_TEMPLATE.render_context(news_ctx)


with open(abspath("./docs/index.html"), "w") as file:
    file.write(index.getvalue())

with open(abspath("./docs/news.html"), "w") as file:
    file.write(news.getvalue())
