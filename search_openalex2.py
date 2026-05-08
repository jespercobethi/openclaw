import urllib.request
import urllib.parse
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

queries = [
    "multi-motor synchronous control wind turbine pitch system",
    "dual motor pitch control wind turbine PMSM",
    "model predictive control pitch angle wind turbine generator",
    "wind turbine pitch permanent magnet synchronous motor optimization",
    "active disturbance rejection control wind pitch motor",
    "deviation coupling multi-motor wind energy"
]

all_papers = []

for q in queries:
    encoded_q = urllib.parse.quote(q)
    url = f'https://api.openalex.org/works?search={encoded_q}&filter=from_publication_date:2022-01-01&sort=relevance_score:desc&per_page=5'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            for work in data.get('results', []):
                title = work.get('title', 'N/A')
                year = work.get('publication_year', 'N/A')
                authors = ', '.join([a.get('author', {}).get('display_name', '') for a in work.get('authorships', [])][:3])
                doi = work.get('doi', '')
                abstract_inv = work.get('abstract_inverted_index', {})
                if abstract_inv:
                    word_positions = []
                    for word, positions in abstract_inv.items():
                        for pos in positions:
                            word_positions.append((pos, word))
                    word_positions.sort()
                    abstract = ' '.join([w for _, w in word_positions[:80]]) + '...'
                else:
                    abstract = ''
                all_papers.append({
                    'title': title,
                    'year': year,
                    'authors': authors,
                    'abstract': abstract,
                    'doi': doi or ''
                })
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(1)

seen = set()
unique = []
for p in all_papers:
    t = (p['title'] or '').lower().strip()
    if t and t not in seen:
        seen.add(t)
        unique.append(p)

unique.sort(key=lambda x: x.get('year') or 0, reverse=True)

relevant = []
for p in unique:
    title_lower = (p['title'] or '').lower()
    abstract_lower = (p['abstract'] or '').lower()
    combined = title_lower + ' ' + abstract_lower
    keywords = ['pitch', 'wind turbine', 'wind energy', 'permanent magnet', 'pmsm', 'synchronous motor', 'servo', 'multi-motor', 'predictive control', 'synchronization', 'torque control', 'mpc', 'adrc', 'disturbance', 'coupling']
    score = sum(1 for kw in keywords if kw in combined)
    if score >= 2:
        relevant.append((score, p))

relevant.sort(key=lambda x: x[0], reverse=True)

print(f"Found {len(relevant)} relevant papers:\n")
for score, p in relevant[:15]:
    print(f"[Relevance: {score}] ---")
    print(f"Title: {p['title']}")
    print(f"Year: {p['year']}")
    print(f"Authors: {p['authors']}")
    if p['doi']:
        print(f"DOI: {p['doi']}")
    if p['abstract']:
        print(f"Abstract: {p['abstract'][:250]}")
    print()
