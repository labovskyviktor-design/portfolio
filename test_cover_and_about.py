import os
import weasyprint

profile_img = os.path.abspath("web/public/profile-photo.png").replace(os.sep, "/")

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
    background: #0b1329;
    color: #ffffff;
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
    font-size: 14pt;
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
    padding: 14mm 16mm 12mm 16mm;
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
    padding-bottom: 3.5mm;
    margin-bottom: 5mm;
}}
.about-header-title {{
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}}
.about-header-tag {{
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0284c7;
}}
.about-content {{
    display: flex;
    flex: 1;
    gap: 8mm;
    height: 155mm;
}}
.about-sidebar {{
    width: 78mm;
    display: flex;
    flex-direction: column;
    gap: 4mm;
}}
.about-photo-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 3mm;
    padding: 5mm;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.about-photo {{
    width: 38mm;
    height: 38mm;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #0284c7;
    margin-bottom: 3mm;
}}
.about-photo-name {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
}}
.about-photo-role {{
    font-size: 8pt;
    font-weight: 600;
    color: #0284c7;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 1mm;
}}
.about-info-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 3mm;
    padding: 3.5mm 4.5mm;
    font-size: 8pt;
    line-height: 1.45;
}}
.about-info-title {{
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 2mm;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 1mm;
}}
.about-info-row {{
    display: flex;
    justify-content: space-between;
    padding: 1.2mm 0;
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
    padding: 4mm 5mm;
    font-size: 8.8pt;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 4mm;
}}
.about-pillars-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4mm;
    margin-bottom: 4mm;
}}
.pillar-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #0284c7;
    border-radius: 2.5mm;
    padding: 3.5mm 4mm;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}}
.pillar-title {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2mm;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 1mm;
}}
.pillar-list {{
    list-style: none;
    padding: 0;
    font-size: 7.6pt;
    line-height: 1.45;
    color: #475569;
}}
.pillar-list li {{
    position: relative;
    padding-left: 3.5mm;
    margin-bottom: 1.2mm;
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
    padding: 3.5mm 5mm;
}}
.stages-title {{
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #475569;
    margin-bottom: 2mm;
}}
.stages-badges {{
    display: flex;
    gap: 3mm;
}}
.stage-pill {{
    flex: 1;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 2mm;
    padding: 2mm 3mm;
    font-size: 7.5pt;
    font-weight: 600;
    color: #1e293b;
    text-align: center;
}}
.stage-pill span {{
    display: block;
    font-size: 6.8pt;
    color: #64748b;
    font-weight: 400;
    margin-top: 0.5mm;
}}
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
}}
.page-num {{
    font-weight: 600;
    color: #0284c7;
}}
</style>
</head>
<body>

<!-- STRANA 1: KRYCIA STRANA -->
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

<!-- STRANA 2: O MNE / PROFIL PROJEKTANTA -->
<div class="about-page">
    <div class="about-header">
        <div class="about-header-title">O Mne & Profil Projektanta</div>
        <div class="about-header-tag">Ing. Viktor Labovský • TZB Inžiniering</div>
    </div>
    <div class="about-content">
        <div class="about-sidebar">
            <div class="about-photo-card">
                <img src="file:///{profile_img}" class="about-photo" />
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

</body>
</html>
"""

weasyprint.HTML(string=html).write_pdf("test_cover_and_about.pdf")
print("Generated test_cover_and_about.pdf successfully!")
