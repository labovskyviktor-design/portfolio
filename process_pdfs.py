import os
import zipfile
import fitz  # PyMuPDF
from PIL import Image
import json
import re
from pathlib import Path

# Config
PDF_DIR = r"C:\Users\42191\.gemini\antigravity-ide\scratch\portfolio-projektov\data\pdfs"
WEB_PUB_DIR = r"C:\Users\42191\.gemini\antigravity-ide\scratch\portfolio-projektov\web\public\projects"
JSON_OUT = r"C:\Users\42191\.gemini\antigravity-ide\scratch\portfolio-projektov\web\src\projects.json"

def clean_project_name(raw_name):
    name = raw_name
    # Remove dates like 20260317_, 26_04_, or 251021 (with space or underscore)
    name = re.sub(r'^\d{8}[_\s]', '', name)
    name = re.sub(r'^\d{6}[_\s]', '', name)
    name = re.sub(r'^\d{2}_\d{2}[_\s]', '', name)
    
    name = name.replace('_', ' ')
    
    # Remove trailing .pdf or pdf
    name = re.sub(r'\.?pdf$', '', name, flags=re.IGNORECASE)
    
    # Remove common tags including TS, PSP, expedicia
    words_to_remove = ['UK', 'ÚK', 'export', 'exp', 'expedicia', 'ZTI', 'DSP', 'PSP', 'NEEDIT', 'final', 'TS', 'RP E11 07']
    for word in words_to_remove:
        name = re.sub(rf'\b{word}\b', '', name, flags=re.IGNORECASE)
        
    name = name.strip(' -_').strip()
    
    # Fallback if name becomes empty or is a generic folder
    if not name or name.lower() in ['needit', 'ostatne', 'vykresy', 'export']:
        return raw_name.replace('_', ' ').strip()
        
    name = re.sub(r'\s+', ' ', name)
    return name

def extract_zips(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith('.zip'):
                zip_path = os.path.join(root, f)
                extract_dir = os.path.join(root, f[:-4])
                if not os.path.exists(extract_dir):
                    os.makedirs(extract_dir)
                    print(f"Extracting {zip_path} to {extract_dir}")
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_dir)
                    except Exception as e:
                        print(f"Failed to extract {zip_path}: {e}")

def get_project_name(filepath, pdf_dir):
    rel_path = os.path.relpath(filepath, pdf_dir)
    top_level = rel_path.split(os.sep)[0]
    
    generic_folders = ['export', 'needit', 'dsp', 'uk', 'ostatne', 'vykresy', 'úk export']
    if top_level.lower() in generic_folders:
        filename = Path(filepath).stem
        parts = filename.split('-')
        if len(parts) > 1:
            base = parts[0]
        else:
            base = filename.rsplit('_', 1)[0]
        base = re.sub(r'^TS_', '', base, flags=re.IGNORECASE)
        return clean_project_name(base)
    else:
        return clean_project_name(top_level)

def extract_metadata(filepaths, extracted_texts="", proj_name=""):
    # Analýza celých ciest k súborom + vytiahnutý text z rozpisek
    combined = (" ".join(filepaths) + " " + extracted_texts).lower()
    
    profesie = []
    if any(k in combined for k in ['zti', 'zdravotechni', 'kanalizácia', 'vodovod']):
        profesie.append("Zdravotechnika (ZTI)")
    if any(k in combined for k in ['úk', 'uk', 'vykurovanie', 'ústredné']):
        profesie.append("Vykurovanie (ÚK)")
    
    if any(k in combined for k in ['audit', 'ttp', 'posudok', 'certifikát']):
        profesie = ["TTP"]
        
    profesia = " + ".join(profesie) if profesie else "Nezaradené"
        
    if 'kaviaren' in proj_name.lower() or 'kaviareň' in proj_name.lower() or 'klasiko' in proj_name.lower():
        stupen = "Realizačný projekt (RP)"
    elif 'audit' in profesia.lower():
        stupen = ""
    else:
        stupen = "Projekt stavby"
        
    return profesia, stupen

PROJECT_MAPPING = {
    "ROZPRAVKOVA KAVIAREN": "Kaviareň Nivy",
    "KAVIAREN NIVY": "Kaviareň Nivy",
    "262526": "Chata Zlatá hora",
    "260528 Chata zlata hora": "Chata Zlatá hora",
    "KAMPUS": "EDU-TECH KAMPUS PÚCHOV",
    "KAMPUS PUCHOV": "EDU-TECH KAMPUS PÚCHOV",
    "ASOC": "ASOC – Administratívno-skladové a obchodné centrum",
    "260619 ASOC": "ASOC – Administratívno-skladové a obchodné centrum",
    "Audit faxcopy": "TTP - FaxCopy",
    "Audit MATYŠAK": "TTP - Matyšák",
}

def process_pdfs():
    os.makedirs(WEB_PUB_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    
    # 1. Group files by project name
    grouped_files = {}
    for root, dirs, files in os.walk(PDF_DIR):
        for f in files:
            if f.lower().endswith('.pdf'):
                filepath = os.path.join(root, f)
                
                file_stem_lower = Path(f).stem.lower()
                ignore_kws = ['titul', 'obal', 'stit', 'štít', 'titok', 'faktura', 'faktúra', 'obsah', 'zoznam', 'priloh', 'zp.pdf']
                if any(kw in file_stem_lower for kw in ignore_kws) or f.lower() == '20260313_rd_valul_uk-zp.pdf':
                    continue
                    
                proj_name = get_project_name(filepath, PDF_DIR)
                if not proj_name:
                    proj_name = "Nezaradené"
                
                # Aplikovanie manuálneho mapovania a zlúčenia
                mapped_name = proj_name
                lower_proj = proj_name.lower()
                for k, v in sorted(PROJECT_MAPPING.items(), key=lambda x: len(x[0]), reverse=True):
                    if k.lower() in lower_proj:
                        mapped_name = v
                        break
                proj_name = mapped_name
                            
                if proj_name not in grouped_files:
                    grouped_files[proj_name] = []
                grouped_files[proj_name].append(filepath)

    # 2. Process each project
    projects_data = []
    
    try:
        with open('representative_descriptions.json', 'r', encoding='utf-8') as f:
            representative_descs = json.load(f)
    except Exception:
        representative_descs = {}
    
    for project_name, filepaths in grouped_files.items():
        print(f"Processing project: {project_name}")
        project_pub_dir = os.path.join(WEB_PUB_DIR, project_name)
        os.makedirs(project_pub_dir, exist_ok=True)
        
        project_files = []
        cover_image = None
        extracted_texts = ""
        project_description = representative_descs.get(project_name, "")
        
        for pdf_path in filepaths:
            f = os.path.basename(pdf_path)
            # Make rel_path simpler since we grouped dynamically
            base_name = Path(f).stem.replace(os.sep, "_")
            
            try:
                doc = fitz.open(pdf_path)
                if len(doc) == 0:
                    continue
                    
                w0, h0 = doc[0].rect.width, doc[0].rect.height
                is_portrait_a4 = w0 < h0 and w0 < 650
                
                out_pdf_name = f"{base_name}.pdf"
                thumb_name = f"{base_name}_thumb.webp"
                out_pdf_path = os.path.join(project_pub_dir, out_pdf_name)
                
                if is_portrait_a4:
                    # Vyradíme všetky A4 dokumenty z portfólia (technické správy)
                    # okrem energetických auditov a posudkov, ktoré sú čisto textové.
                    if 'audit' not in project_name.lower() and 'ttp' not in project_name.lower() and 'audit' not in f.lower() and 'ttp' not in f.lower():
                        continue
                        
                    file_type = "pdf"
                else:
                    mask_w = 180 * 2.834
                    mask_h = 80 * 2.834
                    for page in doc:
                        w, h = page.rect.width, page.rect.height
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
                            
                        # Extrakt textu z rozpisky predtým, než ju prekryjeme
                        try:
                            t = page.get_textbox(mask_rect)
                            if t: extracted_texts += " " + t
                        except:
                            pass
                            
                        page.draw_rect(mask_rect, color=(1, 1, 1), fill=(1, 1, 1))
                        
                    file_type = "drawing"
                    
                # Hromadné začiernenie (zabielenie) mien vo všetkých dokumentoch (A4 aj výkresy)
                names_to_redact = [
                    "Norbert Jokay", "Norber Jokay", "Samuel Fila", 
                    "N. Jokay", "N.Jokay", "S. Fila", "S.Fila", "Jokay",
                    "Norbert Jókay", "Norber Jókay", "N. Jókay", "N.Jókay", "Jókay"
                ]
                for page in doc:
                    for name_to_hide in names_to_redact:
                        # fitz.search_for je defaultne case-insensitive
                        instances = page.search_for(name_to_hide)
                        for inst in instances:
                            # Pridáme malý padding aby sme mali istotu že text je úplne prekrytý
                            inst.x0 -= 1
                            inst.y0 -= 1
                            inst.x1 += 1
                            inst.y1 += 1
                            page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                            
                doc.save(out_pdf_path)
                    
                pix_thumb = doc[0].get_pixmap(dpi=30)
                mode = "RGBA" if pix_thumb.alpha else "RGB"
                img_thumb = Image.frombytes(mode, [pix_thumb.width, pix_thumb.height], pix_thumb.samples)
                img_thumb.thumbnail((400, 400))
                img_thumb.save(os.path.join(project_pub_dir, thumb_name), "WEBP", quality=70)
                
                file_info = {
                    "id": base_name,
                    "title": Path(f).stem,
                    "full": f"/projects/{project_name}/{out_pdf_name}",
                    "thumb": f"/projects/{project_name}/{thumb_name}",
                    "type": file_type
                }
                project_files.append(file_info)
                
                if not cover_image and file_type == "drawing":
                    cover_image = file_info["thumb"]
                elif not cover_image:
                    cover_image = file_info["thumb"]
                    
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                
        profesia, stupen = extract_metadata(filepaths, extracted_texts, project_name)
        
        if project_files:
            # Usporiadanie súborov: výkresy (drawing) ako prvé, okrem auditov
            if 'audit' not in project_name.lower() and 'ttp' not in project_name.lower() and 'audit' not in profesia.lower() and 'ttp' not in profesia.lower():
                def sort_key(x):
                    t = x['title'].lower()
                    is_podorys = any(word in t for word in ['podorys', 'pôdorys', 'pódorys', '1np', '2np', '1.np', '2.np'])
                    is_schema = any(word in t for word in ['schema', 'schéma', 'rez'])
                    return (not is_podorys, is_schema, x['type'] == 'pdf', x['title'])
                project_files.sort(key=sort_key)
            else:
                project_files.sort(key=lambda x: x['title'])
                
            projects_data.append({
                "id": project_name,
                "name": project_name,
                "profession": profesia,
                "stage": stupen,
                "description": project_description,
                "cover": project_files[0]["thumb"] if project_files else None,
                "files": project_files
            })
            
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(projects_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_zips(PDF_DIR)
    process_pdfs()
    print("Done processing PDFs.")
