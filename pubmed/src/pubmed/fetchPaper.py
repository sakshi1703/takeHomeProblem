import requests
import pandas as pd
import argparse
from typing import List, Dict, Optional

PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_paper_ids(query: str) -> List[str]:
    """Fetch PubMed IDs for a given query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 50,
        "retmode": "json"
    }
    response = requests.get(PUBMED_API, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """Fetch details for a list of PubMed IDs."""
    if not paper_ids:
        return []
    
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    response = requests.get(FETCH_API, params=params)
    response.raise_for_status()
    data = response.json()
    
    papers = []
    for paper_id in paper_ids:
        summary = data.get("result", {}).get(paper_id, {})
        papers.append({
            "PubmedID": paper_id,
            "Title": summary.get("title", "N/A"),
            "Publication Date": summary.get("pubdate", "N/A"),
            "Authors": summary.get("authors", []),  # Needs filtering
        })
    
    return papers

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Filter out academic authors and identify company affiliations."""
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        
        for author in paper["Authors"]:
            affiliation = author.get("affiliation", "")
            if affiliation and "university" not in affiliation.lower():
                non_academic_authors.append(author.get("name", "Unknown"))
                company_affiliations.append(affiliation)
        
        paper["Non-academic Authors"] = ", ".join(non_academic_authors)
        paper["Company Affiliations"] = ", ".join(set(company_affiliations))
    
    return papers
