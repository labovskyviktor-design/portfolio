import fitz
import os
import glob

PDF_DIR = r"C:\Users\42191\.gemini\antigravity-ide\scratch\portfolio-projektov\data\pdfs"
pdfs = glob.glob(os.path.join(PDF_DIR, "**/*.pdf"), recursive=True)

print(f"Found {len(pdfs)} pdfs. Testing first 3 drawings...")
count = 0
for pdf in pdfs:
    doc = fitz.open(pdf)
    if len(doc) == 0: continue
    w, h = doc[0].rect.width, doc[0].rect.height
    if w >= h or w >= 650: # Drawing
        page = doc[0]
        mask_w = 210 * 2.834
        mask_h = 297 * 2.834
        if page.rotation == 0:
            mask_rect = fitz.Rect(w - mask_w, h - mask_h, w, h)
        elif page.rotation == 90:
            mask_rect = fitz.Rect(w - mask_h, 0, w, mask_w)
        elif page.rotation == 180:
            mask_rect = fitz.Rect(0, 0, mask_w, mask_h)
        elif page.rotation == 270:
            mask_rect = fitz.Rect(0, h - mask_w, mask_h, h)
        else:
            mask_rect = fitz.Rect(w - mask_w, h - mask_h, w, h)
            
        text = page.get_textbox(mask_rect)
        print(f"--- {os.path.basename(pdf)} ---")
        print(text[:200] + "..." if len(text) > 200 else text)
        count += 1
        if count >= 5:
            break
