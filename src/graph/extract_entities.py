from functools import lru_cache
import spacy

from src.ingestion.clean_filings import clean_sec_text
from src.ingestion.extract_narrative import extract_narrative_sections

MAX_CHARS = 200000
SHORT_TEXT_LIMIT = 8000

@lru_cache(maxsize=1)
def _nlp():
    return spacy.load("en_core_web_trf")

def _orgs_from_doc(doc) -> set[str]:
    return {ent.text for ent in doc.ents if ent.label_ == "ORG"}

def extract_organizations(text: str) -> list[str]:
    """
    Full-filing NER over cleaned narrative (expensive, use for audits)
    """
    text = extract_narrative_sections(clean_sec_text(text))
    orgs: set[str] = set()
    nlp = _nlp()
    for i in range(0, len(text), MAX_CHARS):
        doc = nlp(text[i : i+MAX_CHARS])
        orgs.update(_orgs_from_doc(doc))
    return list(orgs)

def extract_organizations_in_span(text: str) -> list[str]:
    """
  NER on a short context window (used by edge extraction)
  Limits false co-mentions from registry substring matching alone
  """
    if not text.strip():
        return []
    nlp = _nlp()
    bounded = text[:SHORT_TEXT_LIMIT]
    doc = nlp(bounded)
    return list(_orgs_from_doc(doc))