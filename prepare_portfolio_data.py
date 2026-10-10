import json
import os
import fitz

PROJECTS_JSON = r"web/src/projects.json"
DESCRIPTIONS_JSON = r"representative_descriptions.json"
RENDERS_DIR = r"pdf_renders"
os.makedirs(RENDERS_DIR, exist_ok=True)

with open(PROJECTS_JSON, encoding="utf-8") as f:
    projects = json.load(f)

with open(DESCRIPTIONS_JSON, encoding="utf-8") as f:
    descriptions = json.load(f)

# Priority sorting matching App.tsx
top_projects = [
    "RD Imričko",
    "EDU-TECH KAMPUS",
    "ASOC",
    "Chata na Jankovej Lúke",
    "Obecny dom Limbach",
    "TTP - FaxCopy"
]
demoted_projects = [
    "RD Veľká Paka",
    "RD POD PRIEHRADOU"
]

def sort_key(p):
    name = p['name']
    for idx, tp in enumerate(top_projects):
        if tp in name or name in tp:
            return (0, idx, name)
    for idx, dp in enumerate(demoted_projects):
        if dp in name or name in dp:
            return (2, idx, name)
    return (1, 0, name)

sorted_projects = sorted(projects, key=sort_key)
print("Sorted order:")
for i, p in enumerate(sorted_projects):
    print(f"{i+1:02d}. {p['name']}")

