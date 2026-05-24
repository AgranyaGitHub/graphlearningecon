import spacy

nlp = spacy.load("en_core_web_sm")

def extract_organizations(text):
    doc = nlp(text)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            orgs.append(ent.text)
    
    return list(set(orgs))