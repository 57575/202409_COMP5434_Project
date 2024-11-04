from typing import Union, List, Dict
from typing import Optional


class Author:
    first: str
    middle: List[str]
    last: str
    suffix: str
    affiliation: dict
    email: str

    def __init__(self, first: str, middle: List[str], last: str, suffix: Optional[str], affiliation: Dict,
                 email: Optional[str]):
        self.first = first
        self.middle = middle
        self.last = last
        self.suffix = suffix
        self.affiliation = affiliation
        self.email = email


class CiteSpan:
    def __init__(self, start: int, end: int, text: str, ref_id: str):
        self.start = start
        self.end = end
        self.text = text
        self.ref_id = ref_id


class BibEntry:
    def __init__(self, ref_id: str, title: str, authors: List[Author], year: int, venue: str, volume: Optional[str],
                 issn: Optional[str], pages: Optional[str], other_ids: Dict[str, List[str]]):
        self.ref_id = ref_id
        self.title = title
        self.authors = authors
        self.year = year
        self.venue = venue
        self.volume = volume
        self.issn = issn
        self.pages = pages
        self.other_ids = other_ids


class Paragraph:
    def __init__(self, text: str, cite_spans: List[CiteSpan], ref_spans: List[CiteSpan], section: str):
        self.text = text
        self.cite_spans = cite_spans
        self.ref_spans = ref_spans
        self.section = section


class RefEntry:
    def __init__(self, text: str, latex: any, type: str):
        self.text = text
        self.type = type
        self.latex = latex


class AbstractParagraph:
    def __init__(
            self, text: str, cite_spans: List[CiteSpan], ref_spans: List[Dict], section: str
    ):
        self.text = text
        self.cite_spans = cite_spans
        self.ref_spans = ref_spans
        self.section = section


class PaperMetaData:
    title: str
    authors: List[Author]

    def __init__(self, title: str, authors: List[Author]):
        self.title = title
        self.authors = authors


class PaperSchema:
    paper_id: str
    metadata: Optional[PaperMetaData]
    back_matter: Union[List, Dict]
    abstract: List[AbstractParagraph]
    body_text: List[Paragraph]
    bib_entries: Dict[str, BibEntry]
    ref_entries: Dict[str, RefEntry]
    back_matter: List[Paragraph]

    def __init__(
            self,
            paper_id: str,
            metadata: PaperMetaData,
            abstract: List[AbstractParagraph],
            body_text: List[Paragraph],
            bib_entries: Dict[str, BibEntry],
            ref_entries: Dict[str, RefEntry],
            back_matter: List[Paragraph]
    ):
        self.paper_id = paper_id
        self.metadata = metadata
        self.abstract = abstract
        self.body_text = body_text
        self.bib_entries = bib_entries
        self.ref_entries = ref_entries
        self.back_matter = back_matter
