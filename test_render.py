import os
import json
import fitz  # PyMuPDF
from PIL import Image

# Directories
PROJECTS_JSON = r"web/src/projects.json"
DESCRIPTIONS_JSON = r"representative_descriptions.json"
RENDERS_DIR = r"pdf_renders"
os.makedirs(RENDERS_DIR, exist_ok=True)

with open(PROJECTS_JSON, encoding="utf-8") as f:
    projects = json.load(f)

print(f"Loaded {len(projects)} projects.")

# Test rendering top 3 projects drawings
for p in projects[:3]:
    p_name = p['name']
    print(f"Testing render for: {p_name}")
    for i, file_info in enumerate(p.get('files', [])[:2]):
        pdf_path = os.path.join("web/public", file_info['full'].lstrip('/'))
        if os.path.exists(pdf_path):
            doc = fitz.open(pdf_path)
            page = doc[0]
            # 160 DPI is great balance of sharpness and file size
            pix = page.get_pixmap(dpi=160)
            clean_id = "".join(c if c.isalnum() else "_" for c in file_info['id'])
            out_img = os.path.join(RENDERS_DIR, f"{clean_id}.png")
            pix.save(out_img)
            print(f"  Rendered {out_img} ({pix.width}x{pix.height})")

print("Rendering test finished successfully.")
