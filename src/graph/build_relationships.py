from extract_entities import extract_organizations
from company_registry import normalize_company_name

def build_relationships(text):
    orgs = extract_organizations(text)
    normalized = []

    for org in orgs:
        ticker = normalize_company_name(org)
        if ticker:
            normalized.append(ticker)
    
    edges = []

    for i in range(len(normalized)):
        for j in range(i+1, len(normalized)):
            edges.append((normalized[i], normalized[j]))
    
    return edges