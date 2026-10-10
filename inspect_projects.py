import json
import os

with open('web/src/projects.json', encoding='utf-8') as f:
    projects = json.load(f)

print(f"Total projects in JSON: {len(projects)}")
for i, p in enumerate(projects):
    name = p.get('name', 'Bez názvu')
    prof = p.get('profession', 'N/A')
    stage = p.get('stage', 'N/A')
    desc = p.get('description', '')
    files = p.get('files', [])
    valid_pdfs = 0
    valid_thumbs = 0
    for f in files:
        full_path = os.path.join('web/public', f['full'].lstrip('/'))
        thumb_path = os.path.join('web/public', f['thumb'].lstrip('/'))
        if os.path.exists(full_path):
            valid_pdfs += 1
        if os.path.exists(thumb_path):
            valid_thumbs += 1
    print(f"[{i+1:02d}] {name} | {prof} | {stage} | files: {len(files)} (PDFs ok: {valid_pdfs}, thumbs ok: {valid_thumbs}) | desc len: {len(desc)}")
