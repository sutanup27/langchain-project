# pip install requests python-dotenv
import requests, math

def openalex_find_author(name, affiliation_hint=None):
    q = {"search": name, "per_page": 25 }
    r = requests.get("https://api.openalex.org/authors", params=q, timeout=30)
    r.raise_for_status()
    candidates = r.json().get("results", [])
    if affiliation_hint:
        # pick the first candidate that mentions the affiliation
        for a in candidates:
            insts = " ".join([ai.get("display_name","") for ai in a.get("last_known_institutions",[])])
            if affiliation_hint.lower() in insts.lower():
                return a
    return candidates[0] if candidates else None

def openalex_author_works(author_id, email_for_politeness="you@example.com", max_pages=5):
    # pull most-cited works first so we can compute h-index quickly
    works = []
    params = {
        "filter": f"author.id:{author_id}",
        "sort": "cited_by_count:desc",
        "per_page": 200,
        "mailto": email_for_politeness
    }
    cursor = "*"
    for _ in range(max_pages):
        r = requests.get("https://api.openalex.org/works", params={**params, "cursor": cursor}, timeout=60)
        r.raise_for_status()
        data = r.json()
        works.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor: break
    return works

def compute_h_and_i10(citation_counts):
    citation_counts = sorted(citation_counts, reverse=True)
    h = max((i+1 for i, c in enumerate(citation_counts) if c >= i+1), default=0)
    i10 = sum(1 for c in citation_counts if c >= 10)
    return h, i10

# --- example usage ---
name = "Sutanu Paul"            # put the author name here
aff_hint = "Hyland"             # optional: affiliation hint to disambiguate

author = openalex_find_author(name, affiliation_hint=None)
if not author:
    raise SystemExit("No author found")

author_id = author["id"]  # e.g., "https://openalex.org/A123456789"
works = openalex_author_works(author_id)

cites = [w.get("cited_by_count", 0) for w in works]
h, i10 = compute_h_and_i10(cites)

profile = {
    "name": author.get("display_name"),
    "openalex_id": author_id,
    "works_count": author.get("works_count"),
    "total_citations": author.get("cited_by_count"),
    "h_index": h,
    "i10_index": i10,
    "top_papers": [
        {
            "title": w.get("display_name"),
            "year": w.get("publication_year"),
            "citations": w.get("cited_by_count", 0),
            "doi": w.get("doi"),
            "pdf": (w.get("primary_location") or {}).get("pdf_url")
        }
        for w in works[:5]
    ],
}

print(profile)
