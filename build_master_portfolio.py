import os
import json
import re
import fitz
import weasyprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_JSON = os.path.join(BASE_DIR, "web", "src", "projects.json")
DESCRIPTIONS_JSON = os.path.join(BASE_DIR, "representative_descriptions.json")
PROFILE_IMG = os.path.join(BASE_DIR, "web", "public", "profile-photo.png").replace(os.sep, "/")
RENDERS_DIR = os.path.join(BASE_DIR, "pdf_renders")
OUTPUT_PDF = os.path.join(BASE_DIR, "Portfolio_Projektov_TZB_Viktor_Labovsky.pdf")

os.makedirs(RENDERS_DIR, exist_ok=True)

with open(PROJECTS_JSON, encoding="utf-8") as f:
    raw_projects = json.load(f)

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

sorted_projects = sorted(raw_projects, key=sort_key)

def render_drawing(file_info):
    pdf_rel = file_info['full'].lstrip('/')
    pdf_path = os.path.join(BASE_DIR, "web", "public", pdf_rel)
    if not os.path.exists(pdf_path):
        return None, 1.0
    
    clean_id = "".join(c if c.isalnum() else "_" for c in file_info['id'])
    out_img = os.path.join(RENDERS_DIR, f"{clean_id}.png")
    
    if os.path.exists(out_img):
        try:
            doc = fitz.open(pdf_path)
            rect = doc[0].rect
            aspect = rect.width / max(1.0, rect.height)
            return out_img, aspect
        except Exception:
            pass

    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        rect = page.rect
        aspect = rect.width / max(1.0, rect.height)
        target_dim = 2400
        scale = target_dim / max(rect.width, rect.height)
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        pix.save(out_img)
        return out_img, aspect
    except Exception as e:
        print(f"Error rendering {pdf_path}: {e}")
        return None, 1.0

def clean_drawing_title(raw_title):
    t = raw_title.lower()
    if "strecha" in t or "strechy" in t:
        return "Pôdorys strechy – osadenie zdroja tepla"
    if "1np" in t or "1.np" in t or "prízemia" in t or "1. np" in t:
        return "Pôdorys rozvodov 1.NP (Prízemie)"
    if "2np" in t or "2.np" in t or "2. np" in t:
        return "Pôdorys rozvodov 2.NP"
    if "3np" in t or "3.np" in t:
        return "Pôdorys rozvodov 3.NP"
    if "4np" in t or "4.np" in t:
        return "Pôdorys rozvodov 4.NP"
    if "pp" in t or "1pp" in t or "podzemného" in t:
        return "Pôdorys 1.PP (Suterén)"
    if "pôdorys" in t or "podorys" in t:
        return "Pôdorys rozvodov a inštalácií"
    if "zapojenia" in t or "zapojenie" in t:
        return "Hydraulická schéma zapojenia zdroja tepla"
    if "rozvodov" in t:
        return "Hydraulická schéma hlavných rozvodov"
    if "schéma" in t or "schema" in t:
        return "Schéma zapojenia sústavy"
    if "rez" in t:
        return "Technický rez vedenia trás ZTI"
    if "výkaz" in t or "vykaz" in t:
        return "Výkaz materiálu a špecifikácia prvkov"
    if "situacia" in t or "sit" in t:
        return "Koordinačná situácia stavby"
    if "ttp" in t:
        return "Posúdenie fragmentu konštrukcie"
    
    clean = re.sub(r'^\d{6,8}[_\s]', '', raw_title)
    clean = clean.replace('_', ' ').strip()
    return clean.capitalize()

# Rich project metadata map
METADATA_MAP = {
    "EDU-TECH KAMPUS PÚCHOV": {
        "display_name": "EDU-TECH KAMPUS PÚCHOV",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Horné Kočkovce, Púchov",
        "investor": "Trenčianska univerzita A. Dubčeka",
        "system": "Vzduchové a radiátorové vykurovanie",
        "source": "Tepelné čerpadlo na streche objektu",
        "loss": "241,9 kW",
        "temp": "-13 °C",
        "annual": "231 vykurovacích dní",
        "norms": "STN EN 12831, STN EN 17248, STN 73 0540",
    },
    "RD Imričko": {
        "display_name": "Rodinný dom Slivník (RD Imričko)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Slivník, okr. Trebišov",
        "investor": "Súkromný investor",
        "system": "Teplovodné podlahové vykurovanie",
        "source": "Tepelné čerpadlo vzduch/voda",
        "loss": "11,50 kW (zisky 5,40 kW)",
        "temp": "-13 °C",
        "annual": "21,52 MWh/rok",
        "norms": "STN EN 12831-1, STN EN 12828+A1",
    },
    "ASOC – Administratívno-skladové a obchodné centrum": {
        "display_name": "ASOC – Administratívno-skladové centrum",
        "category": "Zdravotechnika (ZTI)",
        "stage": "Projekt stavby (PSP)",
        "location": "Bratislava",
        "investor": "Komerčný developer",
        "system": "Vnútorný vodovod, kanalizácia, strechy",
        "source": "Verejný vodovod, areálová sieť",
        "loss": "Vysokokapacitná distribúcia ZTI",
        "temp": "+10 °C min. teplota trás",
        "annual": "Priemyselné zaťaženie",
        "norms": "STN EN 806, STN EN 12056",
    },
    "Chata na Jankovej Lúke Štrbské Pleso": {
        "display_name": "Chata na Jankovej Lúke, Štrbské Pleso",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (DSP)",
        "location": "Štrbské Pleso, Vysoké Tatry",
        "investor": "Rekreačné zariadenie",
        "system": "Nízkoteplotné vykurovanie s rýchlym nábehom",
        "source": "Automatizovaný centrálny zdroj",
        "loss": "Dimenzované na horské podmienky",
        "temp": "-15 °C (oblastná výpočtová)",
        "annual": "Zvýšená tepelná akumulácia",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "Obecny dom Limbach": {
        "display_name": "Obecný dom Limbach – Nadstavba",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Limbach, okr. Pezinok",
        "investor": "Obec Limbach",
        "system": "Nízkoteplotné konvekčné (50/40°C)",
        "source": "Tepelné čerpadlo vzduch/voda Viessmann",
        "loss": "5,35 kW",
        "temp": "-11 °C",
        "annual": "11,62 MWh/rok (ÚK + TV)",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "TTP - FaxCopy": {
        "display_name": "TTP – FAXCOPY Domkárska, Bratislava",
        "category": "Tepelná technika (TTP)",
        "stage": "Odborný posudok (TTP)",
        "location": "Domkárska 15, Bratislava",
        "investor": "FAXCOPY a.s.",
        "system": "Tepelnotechnické posúdenie konštrukcií",
        "source": "Posudok obalového plášťa budovy",
        "loss": "Posúdenie U_max, R_min a hygieny",
        "temp": "-11 °C ext. / +20 °C int.",
        "annual": "Prevencia kondenzácie a plesní",
        "norms": "STN 73 0540-2+Z1+Z2",
    },
    "Kaviareň Nivy": {
        "display_name": "Kaviareň Nivy Bratislava (Nivy Centrum)",
        "category": "Zdravotechnika (ZTI)",
        "stage": "Realizačný projekt (RP)",
        "location": "Nivy Centrum, Bratislava",
        "investor": "Gastro nájomca",
        "system": "Vnútorný vodovod a kanalizácia baru",
        "source": "Filtrovaná a zmäkčená pitná voda",
        "loss": "Gastro technológia, tuková kanalizácia",
        "temp": "Príprava TÚV a cirkulácia",
        "annual": "Vysoká frekvencia odberu",
        "norms": "STN EN 806, STN EN 12056",
    },
    "KAVIAREN KLASIKO": {
        "display_name": "Kaviareň Klasiko OC Polus, Bratislava",
        "category": "Zdravotechnika (ZTI)",
        "stage": "Realizačný projekt (RP)",
        "location": "OC Polus (VIVO!), Bratislava",
        "investor": "Klasico CAFE",
        "system": "Rozvody vody a kanalizácie zázemia",
        "source": "Centrálna sieť nákupného centra",
        "loss": "Pripojenie kávovarov, umývačiek, drezov",
        "temp": "Hygienické normy gastro",
        "annual": "Plynulá obchodná prevádzka",
        "norms": "STN EN 806, STN EN 12056",
    },
    "Unimpex vinarske centrum": {
        "display_name": "Vinárske centrum UNIMPEX Svätý Jur",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Na Pažiti, Svätý Jur",
        "investor": "Unimpex Bratislava s.r.o.",
        "system": "Nízkoteplotné podlahové kúrenie (45/35°C)",
        "source": "Projektovaný zdroj tepla s odvodom spalín",
        "loss": "31,10 kW",
        "temp": "-11 °C",
        "annual": "Zónová regulácia prevádzky",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "ADM Komarnianska": {
        "display_name": "ADM Komárňanská – Hospodársky objekt",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Komárňanská ul., Bratislava",
        "investor": "MEDISYNER SK s.r.o.",
        "system": "Teplovodné podlahové vykurovanie (45/35°C)",
        "source": "Lokálny vysokoúčinný zdroj",
        "loss": "7,60 kW",
        "temp": "-11 °C",
        "annual": "Optimalizácia prevádzkových nákladov",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "Byt Zamocka 16 BA": {
        "display_name": "Byt Zámocká 16, Bratislava (Podkrovie)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Zámocká 16, Bratislava (Staré Mesto)",
        "investor": "Súkromný vlastník bytu",
        "system": "Podlahové vykurovanie zložitého podkrovia",
        "source": "Centrálny zdroj tepla (CZT)",
        "loss": "Individuálne hydraulické vetvy",
        "temp": "-11 °C",
        "annual": "Regulácia Uponor",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD VALUL": {
        "display_name": "Rodinný dom Chorvátsky Grob (RD VALUL)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Chorvátsky Grob",
        "investor": "Súkromný investor",
        "system": "Teplovodné podlahové vykurovanie",
        "source": "Tepelné čerpadlo vzduch/voda",
        "loss": "Nízkoenergetický štandard A0",
        "temp": "-11 °C",
        "annual": "Vysoká účinnosť COP",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD FIGA": {
        "display_name": "Rodinný dom Vinohrady (RD FIGA)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Vinohrady, Bratislava III",
        "investor": "Súkromný investor",
        "system": "Podlahové (45/35°C) + konvekčné kúrenie",
        "source": "Tepelné čerpadlo vzduch/voda Viessmann",
        "loss": "9,64 kW",
        "temp": "-11 °C",
        "annual": "19,26 MWh/rok (ÚK + TV)",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD BARICICOVA": {
        "display_name": "Rodinný dom Kuchyňa (Baričičova)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Obec Kuchyňa, okr. Malacky",
        "investor": "Súkromný investor",
        "system": "Teplovodné podlahové vykurovanie",
        "source": "Kompaktné tepelné čerpadlo",
        "loss": "Optimalizované kladačské plány",
        "temp": "-11 °C",
        "annual": "Vyregulovaná nízkoteplotná sústava",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD Senec Gajdosik": {
        "display_name": "Rodinný dom Senec (Gajdošík)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Senec",
        "investor": "Súkromný investor",
        "system": "Podlahové vykurovanie (45/35°C) + rebríky",
        "source": "Tepelné čerpadlo Viessmann Vitocal",
        "loss": "6,00 kW",
        "temp": "-11 °C",
        "annual": "12,10 MWh/rok (ÚK + TV)",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "OV MS Novy svet": {
        "display_name": "Materská škola Nový Svet",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Obec Nový Svet, okr. Senec",
        "investor": "Obec Nový Svet",
        "system": "Ústredné vykurovanie predškolského objektu",
        "source": "Ekologický zdroj tepla",
        "loss": "Rovnomerné plošné rozloženie teplôt",
        "temp": "-11 °C",
        "annual": "Bezpečná prevádzka pre deti",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "Chata zlata hora": {
        "display_name": "Rekreačná chata Zlatá hora, Stupava",
        "category": "Vykurovanie + ZTI",
        "stage": "Projekt stavby (PSP)",
        "location": "Stupava, Zlatá hora",
        "investor": "Súkromný investor",
        "system": "Podlahové kúrenie Heatflow + studňa",
        "source": "Priamovýhrevné fólie, lokálna žumpa",
        "loss": "Nezávislé zásobovanie chaty",
        "temp": "Zónové priestorové termostaty",
        "annual": "Bezúdržbová prevádzka",
        "norms": "STN EN 12831, STN EN 806",
    },
    "Chata ZLABY": {
        "display_name": "Rekreačná chata Žľaby, Košice",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Košice-Sever, rekreačná oblasť",
        "investor": "Súkromný investor",
        "system": "Elektrické podlahové fólie Heatflow 110W/m²",
        "source": "Elektrické fólie + kúpeľňový rebrík",
        "loss": "3,90 kW",
        "temp": "-13 °C",
        "annual": "9,09 MWh/rok (ÚK + TV)",
        "norms": "STN EN 12831",
    },
    "TTP - Matyšák": {
        "display_name": "TTP – Výrobná hala Víno Matyšák, Pezinok",
        "category": "Tepelná technika (TTP)",
        "stage": "Odborný posudok (TTP)",
        "location": "Pezinok",
        "investor": "Víno Matyšák s.r.o.",
        "system": "Posúdenie obalových konštrukcií haly",
        "source": "Analýza teplovýmenných plôch",
        "loss": "Súčiniteľ prechodu tepla U konštrukcií",
        "temp": "Priemyselné normové kritériá",
        "annual": "Hygienické a energetické hodnotenie",
        "norms": "STN 73 0540-2+Z1+Z2",
    },
    "ZCH Vrakuňa - lesopark": {
        "display_name": "Záhradná chata Vrakuňa - lesopark",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Bratislava - Vrakuňa",
        "investor": "Súkromný investor",
        "system": "Elektrické podlahové fólie Heatflow 110W/m²",
        "source": "Elektrické fólie bez plynovej prípojky",
        "loss": "2,90 kW (výpočtový výkon 4,50 kW)",
        "temp": "-11 °C",
        "annual": "Lokálna digitálna regulácia",
        "norms": "STN EN 12831",
    },
    "Byt Bjornsonova": {
        "display_name": "Byt Björnsonova, Bratislava",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Björnsonova ul., Bratislava",
        "investor": "Vlastník bytu",
        "system": "Rekonštrukcia vykurovacieho systému bytu",
        "source": "Prepočet a napojenie na centrálny zdroj",
        "loss": "Zníženie energetickej náročnosti",
        "temp": "-11 °C",
        "annual": "Vyregulovanie tepelnej pohody",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD HVZD": {
        "display_name": "Rodinný dom Hviezdoslavov (RD HVZD)",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Hviezdoslavov, okr. Dunajská Streda",
        "investor": "Súkromný investor",
        "system": "Teplovodné podlahové vykurovanie",
        "source": "Tepelné čerpadlo Viessmann Vitocal (7,5 kW)",
        "loss": "5,43 kW",
        "temp": "-11 °C",
        "annual": "11,67 MWh/rok (ÚK + TV)",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD PODBI": {
        "display_name": "Rodinný dom Podbiel (RD PODBI)",
        "category": "Vykurovanie + ZTI",
        "stage": "Projekt stavby (PSP)",
        "location": "Podbiel, Orava",
        "investor": "Súkromný investor",
        "system": "Teplovodné konvekčné kúrenie + ZTI",
        "source": "Doskové vykurovacie telesá s nízkou zotrvačnosťou",
        "loss": "Okamžitý reakčný výkon",
        "temp": "-15 °C (oravská oblasť)",
        "annual": "Presné hydraulické dimenzovanie",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD POD PRIEHRADOU": {
        "display_name": "Rodinný dom Pod priehradou, Kuchyňa",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Kuchyňa, Pod priehradou",
        "investor": "Súkromný investor",
        "system": "Nízkoteplotné podlahové vykurovanie",
        "source": "Ekologické tepelné čerpadlo",
        "loss": "Celoročná spoľahlivá prevádzka",
        "temp": "-11 °C",
        "annual": "Úsporné obehové čerpadlá",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "RD Veľká Paka": {
        "display_name": "Rodinný dom Veľká Paka",
        "category": "Vykurovanie (ÚK)",
        "stage": "Projekt stavby (PSP)",
        "location": "Veľká Paka, okr. Dunajská Streda",
        "investor": "Súkromný investor",
        "system": "Podlahové vykurovanie a rozvody ZTI",
        "source": "Vysokoúčinný nízkoteplotný zdroj",
        "loss": "Kompletný domový okruh vody a tepla",
        "temp": "-11 °C",
        "annual": "Nízke prevádzkové náklady bungalovu",
        "norms": "STN EN 12828, STN EN 12831",
    },
    "ZTI Export": {
        "display_name": "Komplexné rozvody ZTI – Distribúcia vody",
        "category": "Zdravotechnika (ZTI)",
        "stage": "Projekt stavby (PSP)",
        "location": "Bratislavský kraj",
        "investor": "Rezidenčný a občiansky sektor",
        "system": "Vnútorný vodovod a sanitárna kanalizácia",
        "source": "Verejný vodovod, akumulácia TÚV",
        "loss": "Hydraulické dimenzovanie svetlostí DN",
        "temp": "Požiarna voda a cirkulácia TÚV",
        "annual": "Spločňovacie normové štandardy",
        "norms": "STN EN 806, STN EN 12056",
    }
}

HTML_HEADER = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: 297mm 210mm;
    margin: 0;
}}
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #ffffff;
    color: #1e293b;
    -webkit-print-color-adjust: exact;
}}

/* ==================== COVER PAGE ==================== */
.cover-page {{
    width: 297mm;
    height: 210mm;
    padding: 22mm 24mm 18mm 24mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    position: relative;
    background: radial-gradient(circle at 80% 20%, #1e293b 0%, #0b1329 70%, #060913 100%);
    overflow: hidden;
}}
.cover-grid {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 15mm 15mm;
    pointer-events: none;
}}
.cover-accent-line {{
    position: absolute;
    top: 0;
    left: 24mm;
    width: 45mm;
    height: 4px;
    background: #38bdf8;
}}
.cover-top {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.cover-category-tag {{
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 2mm 5mm;
    border-radius: 2mm;
}}
.cover-year {{
    font-size: 10pt;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 2px;
}}
.cover-middle {{
    position: relative;
    z-index: 2;
    margin: auto 0;
}}
.cover-title-label {{
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 3mm;
}}
.cover-main-title {{
    font-size: 38pt;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1.08;
    color: #ffffff;
    margin-bottom: 4mm;
    text-transform: uppercase;
}}
.cover-main-title span {{
    color: #38bdf8;
}}
.cover-subtitle {{
    font-size: 13.5pt;
    font-weight: 400;
    color: #cbd5e1;
    letter-spacing: 0.5px;
    margin-bottom: 8mm;
    max-width: 220mm;
    line-height: 1.4;
}}
.cover-tags-bar {{
    display: flex;
    gap: 3mm;
    flex-wrap: wrap;
}}
.cover-tag {{
    font-size: 8.5pt;
    font-weight: 600;
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 2mm 4.5mm;
    border-radius: 2mm;
    letter-spacing: 0.5px;
}}
.cover-bottom {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding-top: 6mm;
}}
.cover-author-block {{
    display: flex;
    flex-direction: column;
}}
.cover-author-name {{
    font-size: 18pt;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.5px;
}}
.cover-author-role {{
    font-size: 9.5pt;
    font-weight: 500;
    color: #38bdf8;
    letter-spacing: 1px;
    margin-top: 1mm;
}}
.cover-contact-list {{
    display: flex;
    gap: 8mm;
    font-size: 9pt;
    color: #94a3b8;
}}
.cover-contact-item {{
    display: flex;
    align-items: center;
    gap: 2mm;
}}
.cover-contact-item strong {{
    color: #ffffff;
}}

/* ==================== ABOUT ME PAGE ==================== */
.about-page {{
    width: 297mm;
    height: 210mm;
    padding: 11mm 15mm 9mm 15mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    position: relative;
    background: #ffffff;
    color: #1e293b;
}}
.about-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 2.5mm;
    margin-bottom: 3.5mm;
}}
.about-header-title {{
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}}
.about-header-tag {{
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0284c7;
}}
.about-content {{
    display: flex;
    flex: 1;
    gap: 7mm;
    height: 164mm;
}}
.about-sidebar {{
    width: 76mm;
    display: flex;
    flex-direction: column;
    gap: 3mm;
}}
.about-photo-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.5mm;
    padding: 3.5mm;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.about-photo {{
    width: 36mm;
    height: 36mm;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #0284c7;
    margin-bottom: 2mm;
}}
.about-photo-name {{
    font-size: 12pt;
    font-weight: 800;
    color: #0f172a;
}}
.about-photo-role {{
    font-size: 7.5pt;
    font-weight: 600;
    color: #0284c7;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 0.5mm;
}}
.about-info-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.5mm;
    padding: 2.8mm 3.8mm;
    font-size: 7.6pt;
    line-height: 1.4;
}}
.about-info-title {{
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 1.2mm;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.6mm;
}}
.about-info-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.8mm 0;
    border-bottom: 1px dashed #f1f5f9;
}}
.about-info-row:last-child {{
    border-bottom: none;
}}
.about-main {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.about-intro-card {{
    background: #f8fafc;
    border-left: 4px solid #0284c7;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    border-radius: 2.5mm;
    padding: 3.2mm 4.2mm;
    font-size: 8.2pt;
    line-height: 1.45;
    color: #334155;
    margin-bottom: 3mm;
}}
.about-pillars-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 3.2mm;
    margin-bottom: 3mm;
}}
.pillar-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #0284c7;
    border-radius: 2.5mm;
    padding: 3mm 3.5mm;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}}
.pillar-title {{
    font-size: 8pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1.5mm;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.6mm;
}}
.pillar-list {{
    list-style: none;
    padding: 0;
    font-size: 7.2pt;
    line-height: 1.4;
    color: #475569;
}}
.pillar-list li {{
    position: relative;
    padding-left: 3.2mm;
    margin-bottom: 0.8mm;
}}
.pillar-list li::before {{
    content: "▪";
    position: absolute;
    left: 0;
    color: #0284c7;
}}
.about-stages-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.5mm;
    padding: 2.8mm 4mm;
}}
.stages-title {{
    font-size: 7.4pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #475569;
    margin-bottom: 1.5mm;
}}
.stages-badges {{
    display: flex;
    gap: 2mm;
}}
.stage-pill {{
    flex: 1;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 2mm;
    padding: 1.5mm 2.2mm;
    font-size: 7pt;
    font-weight: 600;
    color: #1e293b;
    text-align: center;
}}
.stage-pill span {{
    display: block;
    font-size: 6.2pt;
    color: #64748b;
    font-weight: 400;
    margin-top: 0.3mm;
}}

/* ==================== TOC PAGE ==================== */
.toc-page {{
    width: 297mm;
    height: 210mm;
    padding: 10mm 15mm 9mm 15mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    background: #ffffff;
}}
.toc-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 3.5mm 8mm;
    flex: 1;
    height: 168mm;
}}
.toc-section {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2mm;
    padding: 2.5mm 4mm;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}}
.toc-sec-title {{
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #0369a1;
    border-bottom: 1px solid #bae6fd;
    padding-bottom: 1mm;
    margin-bottom: 1.5mm;
    display: flex;
    justify-content: space-between;
}}
.toc-items {{
    display: flex;
    flex-direction: column;
    gap: 0.8mm;
}}
.toc-row {{
    display: flex;
    align-items: baseline;
    font-size: 7pt;
    line-height: 1.25;
}}
.toc-num {{
    width: 5mm;
    font-weight: 700;
    color: #0284c7;
}}
.toc-name {{
    font-weight: 600;
    color: #0f172a;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 78mm;
}}
.toc-meta {{
    font-size: 6.2pt;
    color: #64748b;
    margin-left: 2mm;
    white-space: nowrap;
}}
.toc-dots {{
    flex: 1;
    border-bottom: 1px dotted #cbd5e1;
    margin: 0 1.5mm;
    height: 1px;
}}
.toc-page-num {{
    font-weight: 700;
    color: #0284c7;
    width: 12mm;
    text-align: right;
    white-space: nowrap;
}}

/* ==================== PROJECT PAGE ==================== */
.project-page {{
    width: 297mm;
    height: 210mm;
    padding: 10mm 15mm 8mm 15mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    position: relative;
    background: #ffffff;
}}
.header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 2mm;
    margin-bottom: 2.5mm;
}}
.header-left {{
    display: flex;
    flex-direction: column;
    gap: 0.6mm;
}}
.project-num {{
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #0284c7;
    text-transform: uppercase;
}}
.project-title {{
    font-size: 15pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.4px;
}}
.header-badges {{
    display: flex;
    gap: 2mm;
}}
.badge {{
    font-size: 7.2pt;
    font-weight: 600;
    padding: 1.2mm 2.8mm;
    border-radius: 1.8mm;
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #e2e8f0;
    white-space: nowrap;
}}
.badge-primary {{
    background: #e0f2fe;
    color: #0369a1;
    border-color: #bae6fd;
}}
.content-area {{
    display: flex;
    flex: 1;
    gap: 5mm;
    height: 164mm;
    max-height: 164mm;
}}
.info-col {{
    width: 78mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-size: 8pt;
    line-height: 1.4;
    height: 164mm;
}}
.desc-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #0284c7;
    padding: 2.6mm 3.4mm;
    border-radius: 2mm;
    color: #334155;
    font-size: 7.6pt;
    line-height: 1.4;
    margin-bottom: 2mm;
}}
.spec-group {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 2mm;
    padding: 2.2mm 3.2mm;
    margin-bottom: 2mm;
}}
.spec-title {{
    font-size: 6.8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 1.2mm;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.6mm;
}}
.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.6mm 0;
    border-bottom: 1px dashed #f1f5f9;
}}
.spec-row:last-child {{
    border-bottom: none;
}}
.spec-label {{
    color: #64748b;
    font-weight: 500;
    font-size: 7.1pt;
}}
.spec-val {{
    font-weight: 600;
    color: #0f172a;
    text-align: right;
    font-size: 7.1pt;
}}
.drawings-list {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2mm;
    padding: 2mm 3.2mm;
}}
.drawings-list ul {{
    list-style: none;
    padding-left: 0;
}}
.drawings-list li {{
    position: relative;
    padding-left: 3.2mm;
    margin-bottom: 0.6mm;
    color: #475569;
    font-size: 7.1pt;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.drawings-list li::before {{
    content: "▪";
    position: absolute;
    left: 0;
    color: #0284c7;
}}
.drawings-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 164mm;
    gap: 2mm;
}}
.drawing-card {{
    display: flex;
    flex-direction: column;
    border: 1px solid #cbd5e1;
    border-radius: 2mm;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}}
.drawing-card-single {{
    height: 164mm;
}}
.drawing-card-double {{
    height: 80mm;
}}
.drawing-header {{
    background: #f8fafc;
    padding: 1.2mm 2.8mm;
    border-bottom: 1px solid #e2e8f0;
    font-size: 6.6pt;
    font-weight: 600;
    color: #475569;
    display: flex;
    justify-content: space-between;
}}
.drawing-img-wrap {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.2mm;
    background: #ffffff;
    overflow: hidden;
}}
.drawing-img {{
    max-width: 100%;
    object-fit: contain;
}}

/* Universal Footer */
.footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 2mm;
    font-size: 7.2pt;
    color: #64748b;
}}
.footer-brand {{
    font-weight: 700;
    color: #0f172a;
    letter-spacing: 0.3px;
}}
.page-num {{
    font-weight: 600;
    color: #0284c7;
}}
</style>
</head>
<body>
"""

HTML_PAGES = []

# ==================== STRANA 1: KRYCIA STRANA ====================
HTML_PAGES.append(f"""
<div class="cover-page">
    <div class="cover-grid"></div>
    <div class="cover-accent-line"></div>
    <div class="cover-top">
        <span class="cover-category-tag">Portfólio Projektovej Dokumentácie</span>
        <span class="cover-year">2026</span>
    </div>
    <div class="cover-middle">
        <div class="cover-title-label">Technické zabezpečenie & Inžiniering budov</div>
        <h1 class="cover-main-title">PROJEKTY <span>TZB</span></h1>
        <p class="cover-subtitle">
            Komplexná projektová dokumentácia vykurovania, chladenia, zdravotnej techniky a tepelnotechnických posúdení stavieb pre rezidenčný, občiansky a komerčný sektor.
        </p>
        <div class="cover-tags-bar">
            <span class="cover-tag">VYKUROVANIE (ÚK)</span>
            <span class="cover-tag">ZDRAVOTECHNIKA (ZTI)</span>
            <span class="cover-tag">TEPELNOTECHNICKÉ POSÚDENIA (TTP)</span>
            <span class="cover-tag">PROJEKTY PRE STAVEBNÉ POVOLENIE (PSP)</span>
            <span class="cover-tag">REALIZAČNÉ PROJEKTY (RP)</span>
        </div>
    </div>
    <div class="cover-bottom">
        <div class="cover-author-block">
            <span class="cover-author-name">Ing. Viktor Labovský</span>
            <span class="cover-author-role">Autorizovaný / Samostatný projektant TZB</span>
        </div>
        <div class="cover-contact-list">
            <div class="cover-contact-item">
                <span>Tel:</span>
                <strong>+421 915 341 479</strong>
            </div>
            <div class="cover-contact-item">
                <span>E-mail:</span>
                <strong>labovskyviktor@gmail.com</strong>
            </div>
            <div class="cover-contact-item">
                <span>Lokalita:</span>
                <strong>Bratislava / Celé Slovensko</strong>
            </div>
        </div>
    </div>
</div>
""")

# ==================== STRANA 2: O MNE ====================
HTML_PAGES.append(f"""
<div class="about-page">
    <div class="about-header">
        <div class="about-header-title">O Mne & Profil Projektanta</div>
        <div class="about-header-tag">Ing. Viktor Labovský • TZB Inžiniering</div>
    </div>
    <div class="about-content">
        <div class="about-sidebar">
            <div class="about-photo-card">
                <img src="file:///{PROFILE_IMG}" class="about-photo" />
                <div class="about-photo-name">Ing. Viktor Labovský</div>
                <div class="about-photo-role">Projektant TZB</div>
            </div>
            <div class="about-info-box">
                <div class="about-info-title">Kontaktné údaje</div>
                <div class="about-info-row">
                    <span style="color:#64748b;">Telefón:</span>
                    <span style="font-weight:600;">+421 915 341 479</span>
                </div>
                <div class="about-info-row">
                    <span style="color:#64748b;">E-mail:</span>
                    <span style="font-weight:600;">labovskyviktor@gmail.com</span>
                </div>
                <div class="about-info-row">
                    <span style="color:#64748b;">Pôsobnosť:</span>
                    <span style="font-weight:600;">Bratislava & celá SR</span>
                </div>
                <div class="about-info-row">
                    <span style="color:#64748b;">Spolupráca:</span>
                    <span style="font-weight:600;">Ateliéry, HIP, Klienti</span>
                </div>
            </div>
            <div class="about-info-box">
                <div class="about-info-title">Softvérové vybavenie</div>
                <div class="about-info-row">
                    <span style="color:#64748b;">CAD platformy:</span>
                    <span style="font-weight:600;">AutoCAD, CADKON</span>
                </div>
                <div class="about-info-row">
                    <span style="color:#64748b;">Výpočty TZB:</span>
                    <span style="font-weight:600;">TechCON, Protech</span>
                </div>
                <div class="about-info-row">
                    <span style="color:#64748b;">Normové analýzy:</span>
                    <span style="font-weight:600;">STN EN 12831, 73 0540</span>
                </div>
            </div>
        </div>
        <div class="about-main">
            <div>
                <div class="about-intro-card">
                    Poskytujem profesionálne projektové a inžinierske služby v oblasti technických zariadení budov (TZB). Moja práca spája detailné výpočty, moderné energeticky úsporné technológie a striktné dodržiavanie technických noriem STN EN. Každý projekt je spracovaný s maximálnym dôrazom na minimalizáciu prevádzkových nákladov, bezproblémové stavebné konanie a precíznu koordináciu s ostatnými profesiami a realizačnými firmami.
                </div>
                <div class="about-pillars-grid">
                    <div class="pillar-card">
                        <div class="pillar-title">1. Vykurovanie & Chladenie (ÚK)</div>
                        <ul class="pillar-list">
                            <li>Teplovodné podlahové, stenové a stropné nízkoteplotné vykurovanie</li>
                            <li>Tepelné čerpadlá (vzduch-voda, zem-voda) a hybridné zdroje</li>
                            <li>Presné výpočty tepelných strát a potrieb tepla podľa STN EN 12831</li>
                            <li>Hydraulické vyregulovanie, vyvažovacie ventily a zónová regulácia</li>
                        </ul>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-title">2. Zdravotechnika (ZTI)</div>
                        <ul class="pillar-list">
                            <li>Vnútorný vodovod – pitná, teplá a úžitková voda, cirkulácia a úprava</li>
                            <li>Vnútorná a areálová kanalizácia (splašková a dažďová)</li>
                            <li>Odvodnenie striech, retencia, vsakovanie a hospodárenie s vodou</li>
                            <li>Špeciálne inštalácie pre gastro prevádzky, obchodné centrá a lapače tukov</li>
                        </ul>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-title">3. Tepelná technika (TTP)</div>
                        <ul class="pillar-list">
                            <li>Tepelnotechnické posúdenie konštrukcií podľa STN 73 0540-2+Z1+Z2</li>
                            <li>Hodnotenie súčiniteľov prechodu tepla U a tepelného odporu R</li>
                            <li>Hygienické posúdenie povrchovej teploty a eliminácia rizika plesní</li>
                            <li>Kompletné podklady pre energetické certifikáty budov a audity</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="about-stages-box">
                <div class="stages-title">Spracovávané stupne projektovej dokumentácie</div>
                <div class="stages-badges">
                    <div class="stage-pill">
                        DÚR / Štúdia
                        <span>Koncepčný návrh & bilancia potrieb</span>
                    </div>
                    <div class="stage-pill">
                        PSP / DSP
                        <span>Projekt pre stavebné povolenie</span>
                    </div>
                    <div class="stage-pill">
                        RP (Realizačný projekt)
                        <span>Podrobné výkresy a výkaz výmer</span>
                    </div>
                    <div class="stage-pill">
                        Autorský dozor
                        <span>Dohľad a konzultácie pri výstavbe</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="footer">
        <span class="footer-brand">Ing. Viktor Labovský • Technické zariadenie budov (TZB)</span>
        <span>Autorizovaný projektant • +421 915 341 479 • labovskyviktor@gmail.com</span>
        <span class="page-num">Strana 02</span>
    </div>
</div>
""")

# ==================== STRANA 3: OBSAH PORTFÓLIA ====================
HTML_PAGES.append(f"""
<div class="toc-page">
    <div class="header">
        <div class="header-title">Obsah Portfólia Projektov</div>
        <div class="header-tag">Prehľad dokumentácie TZB</div>
    </div>
    <div class="toc-grid">
        <!-- SEKCIA 1 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>I. Inžinierske stavby & Občianska vybavenosť</span>
                <span style="font-size:6.5pt; color:#64748b;">(ÚK / ZTI)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">01</span>
                    <span class="toc-name">EDU-TECH KAMPUS PÚCHOV (Pôdorysy podlaží a strechy)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 05</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">02</span>
                    <span class="toc-name">EDU-TECH KAMPUS PÚCHOV (Hydraulické schémy)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 06</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">03</span>
                    <span class="toc-name">ASOC – Administratívno-skladové centrum</span>
                    <span class="toc-meta">ZTI</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 07</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">04</span>
                    <span class="toc-name">Obecný dom Limbach – Nadstavba</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 09</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">05</span>
                    <span class="toc-name">Vinárske centrum UNIMPEX Svätý Jur</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 26</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">06</span>
                    <span class="toc-name">ADM Komárňanská – Hospodársko-admin. objekt</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 11</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">07</span>
                    <span class="toc-name">Materská škola Nový Svet</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 18</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 2 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>II. Rezidenčná výstavba – Rodinné domy & Byty</span>
                <span style="font-size:6.5pt; color:#64748b;">(ÚK / Podlahové vykurovanie)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">08</span>
                    <span class="toc-name">Rodinný dom Slivník (RD Imričko)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 04</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">09</span>
                    <span class="toc-name">Rodinný dom Chorvátsky Grob (RD VALUL)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 24</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">10</span>
                    <span class="toc-name">Rodinný dom Vinohrady (RD FIGA)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 20</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">11</span>
                    <span class="toc-name">Rodinný dom Kuchyňa (Baričičova)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 19</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">12</span>
                    <span class="toc-name">Rodinný dom Senec (Gajdošík)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 23</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">13</span>
                    <span class="toc-name">Rodinný dom Hviezdoslavov (RD HVZD)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 21</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">14</span>
                    <span class="toc-name">Rodinný dom Podbiel (RD PODBI)</span>
                    <span class="toc-meta">ZTI + ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 22</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">15</span>
                    <span class="toc-name">Rodinný dom Pod priehradou, Kuchyňa</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 30</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">16</span>
                    <span class="toc-name">Rodinný dom Veľká Paka</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 29</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">17</span>
                    <span class="toc-name">Byt Zámocká 16, Bratislava (Podkrovný byt)</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 13</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">18</span>
                    <span class="toc-name">Byt Björnsonova, Bratislava</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 12</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 3 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>III. Rekreačné objekty & Horské chaty</span>
                <span style="font-size:6.5pt; color:#64748b;">(Vykurovanie & ZTI)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">19</span>
                    <span class="toc-name">Chata na Jankovej Lúke Štrbské Pleso</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 08</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">20</span>
                    <span class="toc-name">Rekreačná chata Zlatá hora, Stupava</span>
                    <span class="toc-meta">ÚK + ZTI</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 15</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">21</span>
                    <span class="toc-name">Rekreačná chata Žľaby, Košice</span>
                    <span class="toc-meta">El. kúrenie</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 14</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">22</span>
                    <span class="toc-name">Záhradná chata Vrakuňa - lesopark</span>
                    <span class="toc-meta">ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 27</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 4 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>IV. Zdravotechnika (ZTI) & Tepelná technika (TTP)</span>
                <span style="font-size:6.5pt; color:#64748b;">(Gastro / Energetika)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">23</span>
                    <span class="toc-name">TTP – FAXCOPY Domkárska, Bratislava</span>
                    <span class="toc-meta">TTP</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 10</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">24</span>
                    <span class="toc-name">Kaviareň Nivy Bratislava (Nivy Centrum)</span>
                    <span class="toc-meta">ZTI (RP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 17</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">25</span>
                    <span class="toc-name">Kaviareň Klasiko OC Polus, Bratislava</span>
                    <span class="toc-meta">ZTI (RP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 16</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">26</span>
                    <span class="toc-name">TTP – Výrobná hala Víno Matyšák, Pezinok</span>
                    <span class="toc-meta">TTP</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 25</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">27</span>
                    <span class="toc-name">Komplexné rozvody ZTI – Distribúcia vody</span>
                    <span class="toc-meta">ZTI</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page-num">Strana 28</span>
                </div>
            </div>
        </div>
    </div>
    <div class="footer">
        <span class="footer-brand">Ing. Viktor Labovský • Technické zariadenie budov (TZB)</span>
        <span>Autorizovaný projektant • +421 915 341 479 • labovskyviktor@gmail.com</span>
        <span class="page-num">Strana 03</span>
    </div>
</div>
""")

# ==================== STRANY PROJEKTOV (STRANY 4 AŽ 30) ====================
PROJECT_ORDER = [
    ("RD Imričko", 4, None),
    ("EDU-TECH KAMPUS PÚCHOV", 5, "part1"),
    ("EDU-TECH KAMPUS PÚCHOV", 6, "part2"),
    ("ASOC – Administratívno-skladové a obchodné centrum", 7, None),
    ("Chata na Jankovej Lúke Štrbské Pleso", 8, None),
    ("Obecny dom Limbach", 9, None),
    ("TTP - FaxCopy", 10, None),
    ("ADM Komarnianska", 11, None),
    ("Byt Bjornsonova", 12, None),
    ("Byt Zamocka 16 BA", 13, None),
    ("Chata ZLABY", 14, None),
    ("Chata zlata hora", 15, None),
    ("KAVIAREN KLASIKO", 16, None),
    ("Kaviareň Nivy", 17, None),
    ("OV MS Novy svet", 18, None),
    ("RD BARICICOVA", 19, None),
    ("RD FIGA", 20, None),
    ("RD HVZD", 21, None),
    ("RD PODBI", 22, None),
    ("RD Senec Gajdosik", 23, None),
    ("RD VALUL", 24, None),
    ("TTP - Matyšák", 25, None),
    ("Unimpex vinarske centrum", 26, None),
    ("ZCH Vrakuňa - lesopark", 27, None),
    ("ZTI Export", 28, None),
    ("RD Veľká Paka", 29, None),
    ("RD POD PRIEHRADOU", 30, None)
]

print(f"Total project page configurations: {len(PROJECT_ORDER)}")

for proj_id, page_num, special_part in PROJECT_ORDER:
    proj = next(p for p in raw_projects if p['name'] == proj_id or p['id'] == proj_id)
    meta = METADATA_MAP.get(proj['name'], {
        "display_name": proj['name'],
        "category": proj.get('profession', 'TZB'),
        "stage": proj.get('stage', 'Projekt stavby (PSP)'),
        "location": "Slovenská republika",
        "investor": "Súkromný investor",
        "system": "Technické zabezpečenie budov",
        "source": "Projektovaný zdroj",
        "loss": "Podľa výpočtu STN EN",
        "temp": "-11 °C",
        "annual": "Optimalizovaná spotreba",
        "norms": "STN EN 12828, STN EN 12831"
    })
    
    desc = descriptions.get(proj['name'], proj.get('description', 'Projektová dokumentácia technického zariadenia budov.'))
    files = proj.get('files', [])
    
    # Select drawing(s)
    drawings = []
    if proj['name'] == "EDU-TECH KAMPUS PÚCHOV":
        if special_part == "part1":
            f1 = next((f for f in files if "1NP" in f['title']), files[0])
            f2 = next((f for f in files if "STRECHA" in f['title']), files[4])
            drawings = [f1, f2]
        else:
            f1 = next((f for f in files if "rozvodov" in f['title']), files[5])
            f2 = next((f for f in files if "zapojenia" in f['title']), files[7])
            drawings = [f1, f2]
    else:
        p_file = None
        s_file = None
        for f in files:
            ft = f['title'].lower()
            if ("pôdorys" in ft or "podorys" in ft or "1np" in ft or "pd" in ft) and not p_file:
                p_file = f
            elif ("schéma" in ft or "schema" in ft or "zapojenia" in ft or "rez" in ft) and not s_file:
                s_file = f
        
        if p_file and s_file:
            drawings = [p_file, s_file]
        elif len(files) >= 2:
            drawings = [files[0], files[1]]
        elif len(files) == 1:
            drawings = [files[0]]
            
    # Render drawings
    rendered_cards_html = []
    is_double = len(drawings) > 1
    card_class = "drawing-card-double" if is_double else "drawing-card-single"
    max_img_h = "68mm" if is_double else "146mm"
    
    for idx, d in enumerate(drawings):
        img_path, aspect = render_drawing(d)
        c_title = clean_drawing_title(d['title'])
        d_label = f"VÝKRES Č. {idx+1:02d}: {c_title.upper()}"
        d_type = "MIERKA 1:50" if "pôdorys" in c_title.lower() else "TECHNICKÁ DOKUMENTÁCIA"
        
        img_src = f"file:///{img_path.replace(os.sep, '/')}" if img_path else ""
        rendered_cards_html.append(f"""
            <div class="drawing-card {card_class}">
                <div class="drawing-header">
                    <span>{d_label}</span>
                    <span>{d_type}</span>
                </div>
                <div class="drawing-img-wrap">
                    <img src="{img_src}" class="drawing-img" style="max-height:{max_img_h};" />
                </div>
            </div>
        """)
        
    drawings_html_block = "\n".join(rendered_cards_html)
    
    p_title = meta['display_name']
    if special_part == "part1":
        p_title += " (Pôdorysy podlaží a strechy)"
    elif special_part == "part2":
        p_title += " (Hydraulické schémy rozvodov)"
        
    page_html = f"""
<div class="project-page">
    <div class="header">
        <div class="header-left">
            <span class="project-num">Projekt {page_num - 3:02d} / Referenčná dokumentácia</span>
            <h1 class="project-title">{p_title}</h1>
        </div>
        <div class="header-badges">
            <span class="badge badge-primary">{meta['category']}</span>
            <span class="badge">{meta['stage']}</span>
            <span class="badge">{meta['location']}</span>
        </div>
    </div>
    <div class="content-area">
        <div class="info-col">
            <div>
                <div class="desc-box">
                    {desc}
                </div>
                <div class="spec-group">
                    <div class="spec-title">Technické parametre stavby</div>
                    <div class="spec-row">
                        <span class="spec-label">Navrhovaný systém</span>
                        <span class="spec-val">{meta['system']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Zdroj energie / tepla</span>
                        <span class="spec-val">{meta['source']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Tepelná strata / výkon</span>
                        <span class="spec-val">{meta['loss']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Výpočtová teplota</span>
                        <span class="spec-val">{meta['temp']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Ročná bilancia</span>
                        <span class="spec-val">{meta['annual']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Normový rámec</span>
                        <span class="spec-val">{meta['norms']}</span>
                    </div>
                </div>
            </div>
            <div class="drawings-list">
                <div class="spec-title">Prílohy v projekte ({len(files)} výkresov)</div>
                <ul>
                    {"".join(f"<li>{clean_drawing_title(f['title'])}</li>" for f in files[:4])}
                </ul>
            </div>
        </div>
        <div class="drawings-col">
            {drawings_html_block}
        </div>
    </div>
    <div class="footer">
        <span class="footer-brand">Ing. Viktor Labovský • Technické zariadenie budov (TZB)</span>
        <span>Autorizovaný projektant • +421 915 341 479 • labovskyviktor@gmail.com</span>
        <span class="page-num">Strana {page_num:02d}</span>
    </div>
</div>
"""
    HTML_PAGES.append(page_html)

HTML_FOOTER = """
</body>
</html>
"""

FULL_HTML = HTML_HEADER + "\n".join(HTML_PAGES) + HTML_FOOTER

HTML_DEBUG_PATH = os.path.join(BASE_DIR, "portfolio_book.html")
with open(HTML_DEBUG_PATH, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated full HTML ({len(HTML_PAGES)} pages). Writing PDF with WeasyPrint to {OUTPUT_PDF}...")
weasyprint.HTML(string=FULL_HTML).write_pdf(OUTPUT_PDF)
print(f"SUCCESS: Generated {OUTPUT_PDF}")
