from typing import Union, List, Dict
from typing import Optional


class Location:
    settlement: str
    region: str
    addrLine: str

    def __init__(self, settlement: str = "", region: str = "", addrLine: str = ""):
        self.settlement = settlement
        self.region = region
        self.addrLine = addrLine


class Affiliation:
    laboratory: str
    institution: str
    location: dict

    def __init__(self, laboratory: str = "", institution: str = "", location: dict = None):
        self.laboratory = laboratory
        self.institution = institution
        if location is not None:
            self.location = location


class Author:
    first: str
    middle: List[str]
    last: str
    suffix: str
    affiliation: Optional[Affiliation]
    email: str

    def __init__(self, first: str, middle: List[str], last: str, suffix: Optional[str], affiliation: dict,
                 email: Optional[str]):
        self.first = first
        self.middle = middle
        self.last = last
        self.suffix = suffix
        self.affiliation = Affiliation(**affiliation)
        self.email = email


class CiteSpan:
    def __init__(self, start: int, end: int, text: str, ref_id: str):
        self.start = start
        self.end = end
        self.text = text
        self.ref_id = ref_id


class BibEntry:
    def __init__(self, ref_id: str, title: str, authors: List[dict], year: int, venue: str, volume: Optional[str],
                 issn: Optional[str], pages: Optional[str], other_ids: Dict[str, List[str]]):
        self.ref_id = ref_id
        self.title = title
        self.authors = [Author(**a) for a in authors]
        self.year = year
        self.venue = venue
        self.volume = volume
        self.issn = issn
        self.pages = pages
        self.other_ids = other_ids


class Paragraph:
    text: str
    cite_spans: List[CiteSpan]
    ref_spans: List[CiteSpan]
    section: str

    def __init__(self, text: str, cite_spans: List[dict], ref_spans: List[dict], section: str):
        self.text = text
        self.cite_spans = [CiteSpan(**c) for c in cite_spans]
        self.ref_spans = [CiteSpan(**c) for c in ref_spans]
        self.section = section


class RefEntry:
    def __init__(self, text: str, latex: any, type: str):
        self.text = text
        self.type = type
        self.latex = latex


class AbstractParagraph:
    def __init__(
            self, text: str, cite_spans: List[dict], ref_spans: List[Dict], section: str
    ):
        self.text = text
        self.cite_spans = [CiteSpan(**c) for c in cite_spans]
        self.ref_spans = [CiteSpan(**c) for c in ref_spans]
        self.section = section


class PaperMetaData:
    title: str
    authors: List[Author]

    def __init__(self, title: str, authors: List[dict]):
        self.title = title
        self.authors = [Author(**a) for a in authors]


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
            metadata: dict,
            abstract: List[dict],
            body_text: List[dict],
            bib_entries: Dict[str, BibEntry],
            ref_entries: Dict[str, RefEntry],
            back_matter: List[dict]
    ):
        self.paper_id = paper_id
        self.metadata = PaperMetaData(**metadata)
        self.abstract = [AbstractParagraph(**a) for a in abstract]
        self.body_text = [Paragraph(**b) for b in body_text]
        self.bib_entries = bib_entries
        self.ref_entries = ref_entries
        self.back_matter = [Paragraph(**b) for b in back_matter]
