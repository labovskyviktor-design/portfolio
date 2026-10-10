import fitz
import json
import os

with open('web/src/projects.json', encoding='utf-8') as f:
    data = json.load(f)

for p in data[:6]:
    print('===', p['name'], '===')
    for file_info in p.get('files', []):
        pdf_path = os.path.join('web/public', file_info['full'].lstrip('/'))
        if os.path.exists(pdf_path):
            doc = fitz.open(pdf_path)
            page = doc[0]
            w = round(page.rect.width)
            h = round(page.rect.height)
            orientation = "Landscape" if w > h else "Portrait"
            print(f"  {file_info['title']}: {len(doc)} str., {w}x{h} pt ({orientation})")
