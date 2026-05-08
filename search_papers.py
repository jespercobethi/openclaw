import urllib.request
import urllib.parse
import json
import time

queries = [
    "wind turbine pitch multi-motor synchronous control PMSM",
    "wind pitch permanent magnet synchronous motor model predictive control",
    "wind turbine pitch servo system multi-motor coordination",
    "large wind turbine pitch motor synchronous control strategy"
]

all_papers = []

for q in queries:
    encoded_q = urllib.parse.quote(q)
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_q}&year=2022-2026&limit=5&fields=title,year,abstract,authors,externalIds'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            for paper in data.get('data', []):
                title = paper.get('title', 'N/A')
                year = paper.get('year', 'N/A')
                authors = ', '.join([a.get('name','') for a in paper.get('authors', [])][:3])
                abstract = paper.get('abstract', '') or ''
                doi = paper.get('externalIds', {}).get('DOI', '')
                all_papers.append({
                    'title': title,
                    'year': year,
                    'authors': authors,
                    'abstract': abstract[:300],
                    'doi': doi
                })
    except Exception as e:
        print(f'Error for query "{q[:30]}...": {e}')
    time.sleep(3)

# Deduplicate by title
seen = set()
unique = []
for p in all_papers:
    if p['title'] not in seen:
        seen.add(p['title'])
        unique.append(p)

# Sort by year descending
unique.sort(key=lambda x: x.get('year') or 0, reverse=True)

print(f"Found {len(unique)} unique papers:\n")
for i, p in enumerate(unique, 1):
    print(f"--- Paper {i} ---")
    print(f"Title: {p['title']}")
    print(f"Year: {p['year']}")
    print(f"Authors: {p['authors']}")
    if p['doi']:
        print(f"DOI: {p['doi']}")
    if p['abstract']:
        print(f"Abstract: {p['abstract']}")
    print()
