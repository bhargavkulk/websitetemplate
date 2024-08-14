import re
import xml.etree.ElementTree as etree
from ..bibliography import BibEntry
import markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from typing import Dict, Tuple, Optional

class CitationProcessor(InlineProcessor):
    def __init__(self, pattern: str, md: markdown.Markdown, entries: Dict[str, BibEntry]):
        super(CitationProcessor, self).__init__(pattern, md)
        self.entries = entries

    def handleMatch(self, m: re.Match, data: str) -> Optional[Tuple[etree.Element, int, int]]:
        text = m.group(1)
        id = m.group(2)
        print(f"text: {text}")
        print(f"id: {id}")
        print(self.entries)
        if id in self.entries:
            entry = self.entries[id]
            el = etree.Element('a')
            el.set('href', entry.url)

            if text == 'title':
                el.text = entry.title
            elif text == 'url':
                el.text = entry.url
            else:
                el.text = text
            return el, m.start(0), m.end(0)

class CitationExtension(Extension):
    def __init__(self, entries: Dict[str, BibEntry]):
        self.entries = entries

    def extendMarkdown(self, md: markdown.Markdown):
        PATTERN = r'\[\$(.*?)\]\(\%([^\)]+)\)'
        md.inlinePatterns.register(CitationProcessor(PATTERN, md, self.entries), 'dict', 175)
