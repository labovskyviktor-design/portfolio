import os
import fitz
import weasyprint

# Render a drawing to test
doc = fitz.open(r"web/public/projects/RD Imričko/20260907_UK_RD_Imričko_1NP.pdf")
page = doc[0]
target_dim = 2400
scale = target_dim / max(page.rect.width, page.rect.height)
mat = fitz.Matrix(scale, scale)
pix = page.get_pixmap(matrix=mat)
os.makedirs("test_renders", exist_ok=True)
img_path = os.path.abspath("test_renders/imricko_1np.png")
pix.save(img_path)

html = f"""
<!DOCTYPE html>
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
    background: #f8fafc;
    color: #1e293b;
    -webkit-print-color-adjust: exact;
}}
.page {{
    width: 297mm;
    height: 210mm;
    padding: 14mm 16mm 12mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    position: relative;
    background: #ffffff;
}}
/* Header */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3.5mm;
    margin-bottom: 4mm;
}}
.header-left {{
    display: flex;
    flex-direction: column;
    gap: 1.5mm;
}}
.project-num {{
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #0284c7;
    text-transform: uppercase;
}}
.project-title {{
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}}
.header-badges {{
    display: flex;
    gap: 2mm;
}}
.badge {{
    font-size: 8pt;
    font-weight: 600;
    padding: 1.5mm 3.5mm;
    border-radius: 2mm;
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #e2e8f0;
}}
.badge-primary {{
    background: #e0f2fe;
    color: #0369a1;
    border-color: #bae6fd;
}}

/* Main layout: left info, right drawing */
.content-area {{
    display: flex;
    flex: 1;
    gap: 7mm;
    height: 155mm;
}}
.info-col {{
    width: 82mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-size: 8.5pt;
    line-height: 1.45;
}}
.desc-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #0284c7;
    padding: 4mm 4.5mm;
    border-radius: 2mm;
    color: #334155;
    font-size: 8.5pt;
    line-height: 1.45;
    margin-bottom: 3mm;
}}
.spec-group {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 2mm;
    padding: 3mm 4mm;
    margin-bottom: 3mm;
}}
.spec-title {{
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 2mm;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 1mm;
}}
.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 1mm 0;
    border-bottom: 1px dashed #f1f5f9;
}}
.spec-row:last-child {{
    border-bottom: none;
}}
.spec-label {{
    color: #64748b;
    font-weight: 500;
}}
.spec-val {{
    font-weight: 600;
    color: #0f172a;
    text-align: right;
}}
.drawings-list {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2mm;
    padding: 3mm 4mm;
}}
.drawings-list ul {{
    list-style: none;
    padding-left: 0;
}}
.drawings-list li {{
    position: relative;
    padding-left: 4mm;
    margin-bottom: 1.2mm;
    color: #475569;
    font-size: 8pt;
}}
.drawings-list li::before {{
    content: "▪";
    position: absolute;
    left: 0;
    color: #0284c7;
}}

.drawing-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 1px solid #cbd5e1;
    border-radius: 2.5mm;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.drawing-header {{
    background: #f8fafc;
    padding: 2mm 4mm;
    border-bottom: 1px solid #e2e8f0;
    font-size: 7.5pt;
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
    padding: 2mm;
    background: #ffffff;
}}
.drawing-img {{
    max-width: 100%;
    max-height: 140mm;
    object-fit: contain;
}}

/* Footer */
.footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 2.5mm;
    font-size: 7.5pt;
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
<div class="page">
    <div class="header">
        <div class="header-left">
            <span class="project-num">Projekt 01 / Referencia</span>
            <h1 class="project-title">Rodinný dom Slivník (RD Imričko)</h1>
        </div>
        <div class="header-badges">
            <span class="badge badge-primary">Vykurovanie (ÚK)</span>
            <span class="badge">Projekt stavby (PSP)</span>
            <span class="badge">Slivník, okr. Trebišov</span>
        </div>
    </div>
    <div class="content-area">
        <div class="info-col">
            <div>
                <div class="desc-box">
                    Moderný návrh ústredného kúrenia pre novostavbu rodinného domu. Projekt v sebe spája detailný výpočet tepelných strát a ziskov podľa STN EN 12831 s optimalizovaným návrhom zdroja tepla a precíznym dimenzovaním rozvodných potrubí a podlahových vykurovacích okruhov.
                </div>
                <div class="spec-group">
                    <div class="spec-title">Technické parametre</div>
                    <div class="spec-row">
                        <span class="spec-label">Vykurovací systém</span>
                        <span class="spec-val">Teplovodné podlahové</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Výpočtová tepelná strata</span>
                        <span class="spec-val">11,50 kW</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Tepelné zisky objektu</span>
                        <span class="spec-val">5,40 kW</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Vonkajšia výpočt. teplota</span>
                        <span class="spec-val">-13 °C</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Ročná spotreba tepla</span>
                        <span class="spec-val">21,52 MWh/rok</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Normový rámec</span>
                        <span class="spec-val">STN EN 12831, 12828</span>
                    </div>
                </div>
            </div>
            <div class="drawings-list">
                <div class="spec-title">Výkresová dokumentácia</div>
                <ul>
                    <li>Pôdorys rozvodov podlahového vykurovania 1.NP</li>
                    <li>Hydraulická schéma zapojenia a rozdeľovačov</li>
                    <li>Podrobná technická správa a dimenzovanie</li>
                </ul>
            </div>
        </div>
        <div class="drawing-col">
            <div class="drawing-header">
                <span>VÝKRES Č. 01: PÔDORYS ROZVODOV VYKUROVANIA 1.NP</span>
                <span>MIERKA 1:50</span>
            </div>
            <div class="drawing-img-wrap">
                <img src="file:///{img_path.replace(os.sep, '/')}" class="drawing-img" />
            </div>
        </div>
    </div>
    <div class="footer">
        <span class="footer-brand">Ing. Viktor Labovský • Technické zariadenie budov (TZB)</span>
        <span>Autorizovaný projektant • +421 915 341 479 • labovskyviktor@gmail.com</span>
        <span class="page-num">Strana 04</span>
    </div>
</div>
</body>
</html>
"""

weasyprint.HTML(string=html).write_pdf("test_single_page.pdf")
print("Generated test_single_page.pdf successfully!")
