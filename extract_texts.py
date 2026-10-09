import fitz
import os
import json

PDF_DIR = r"C:\Users\42191\.gemini\antigravity-ide\scratch\portfolio-projektov\data\pdfs"

def get_text_from_ts():
    ts_texts = {}
    for root, dirs, files in os.walk(PDF_DIR):
        for f in files:
            if f.lower().endswith('.pdf'):
                path = os.path.join(root, f)
                try:
                    doc = fitz.open(path)
                    if len(doc) == 0: continue
                    w0, h0 = doc[0].rect.width, doc[0].rect.height
                    is_portrait_a4 = w0 < h0 and w0 < 650
                    if is_portrait_a4 and 'audit' not in f.lower():
                        text = ""
                        # Prečítame prvé 3 strany z každej technickej správy
                        for i in range(min(3, len(doc))):
                            text += doc[i].get_text() + "\n"
                        # Uložíme prvých 1500 znakov
                        ts_texts[f] = text[:1500]
                except Exception as e:
                    print(f"Error {f}: {e}")
    with open("ts_texts.json", "w", encoding="utf-8") as out:
        json.dump(ts_texts, out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_text_from_ts()
    print("Done")
