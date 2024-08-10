import re
import xml.etree.ElementTree as etree
import markdown
from markdown.inlinepatterns import InlineProcessor, Pattern
from markdown.extensions import Extension
from typing import Dict, Tuple, Optional

class NameLinkProcessor(InlineProcessor):
    def __init__(self, pattern: str, md: markdown.Markdown, mapping: Dict[str, str]):
        super(NameLinkProcessor, self).__init__(pattern, md)
        self.mapping = mapping

    def handleMatch(self, m: re.Match, data: str) -> Optional[Tuple[etree.Element, int, int]]:
        text = m.group(1)
        id = m.group(2)
        print(text)
        if id in self.mapping:
            val = self.mapping[id]
            el = etree.Element('a')
            el.set('href', val)
            el.text = text
            return el, m.start(0), m.end(0)

class NameLinkExtension(Extension):
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
        print(mapping)

    def extendMarkdown(self, md: markdown.Markdown):
        PATTERN = r'\[(.*?)\]\(\@([^\)]+)\)'
        md.inlinePatterns.register(NameLinkProcessor(PATTERN, md, self.mapping), 'dict', 175)

if __name__ == "__main__":
    mapping = {'eeide': 'https://www.cs.utah.edu/~eeide/', 'kulkarni': 'https://www.cs.utah.edu/~mflatt/', 'ganesh': 'https://www.cs.utah.edu/~ganesh/', 'blg': 'https://users.cs.utah.edu/~blg/', 'mhall': 'https://www.cs.utah.edu/~mhall/', 'vijay': 'https://users.cs.utah.edu/~vijay/', 'pavpan': 'https://pavpanchekha.com', 'saday': 'https://www.cs.utah.edu/~saday/', 'regehr': 'http://www.cs.utah.edu/~regehr/', 'bhargav': 'https://bhargavkulk.github.io', 'artem': 'https://www.linkedin.com/in/artem-yadrov-ba847a2b0/', 'zane': 'https://zaneenders.com/'}
    md = markdown.Markdown(extensions=[NameLinkExtension(mapping)])
    print(md.convert('''- TEST NEWS ITEM 1 [Bhargav asda]($bhargav)
- TEST NEWS ITEM 2'''))
