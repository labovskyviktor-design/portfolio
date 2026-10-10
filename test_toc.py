import weasyprint

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {
    size: 297mm 210mm;
    margin: 0;
}
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #ffffff;
    color: #1e293b;
    -webkit-print-color-adjust: exact;
}
.page {
    width: 297mm;
    height: 210mm;
    padding: 13mm 16mm 11mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
    margin-bottom: 4.5mm;
}
.header-title {
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}
.header-tag {
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0284c7;
}
.toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6mm 10mm;
    flex: 1;
    height: 156mm;
}
.toc-section {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.5mm;
    padding: 3.5mm 4.5mm;
    display: flex;
    flex-direction: column;
}
.toc-sec-title {
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0369a1;
    border-bottom: 1.5px solid #bae6fd;
    padding-bottom: 1.5mm;
    margin-bottom: 2mm;
    display: flex;
    justify-content: space-between;
}
.toc-items {
    display: flex;
    flex-direction: column;
    gap: 1.4mm;
}
.toc-row {
    display: flex;
    align-items: baseline;
    font-size: 7.8pt;
    line-height: 1.35;
    padding: 0.5mm 0;
    border-bottom: 1px dashed #f1f5f9;
}
.toc-row:last-child {
    border-bottom: none;
}
.toc-num {
    width: 6mm;
    font-weight: 700;
    color: #0284c7;
}
.toc-name {
    font-weight: 600;
    color: #0f172a;
    flex: 1;
}
.toc-meta {
    font-size: 6.8pt;
    color: #64748b;
    margin: 0 3mm;
}
.toc-dots {
    flex: 1;
    border-bottom: 1px dotted #cbd5e1;
    margin: 0 2mm;
    height: 1px;
}
.toc-page {
    font-weight: 700;
    color: #0284c7;
    width: 14mm;
    text-align: right;
}
.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 2.5mm;
    font-size: 7.5pt;
    color: #64748b;
}
.footer-brand {
    font-weight: 700;
    color: #0f172a;
}
.page-num {
    font-weight: 600;
    color: #0284c7;
}
</style>
</head>
<body>
<div class="page">
    <div class="header">
        <div class="header-title">Obsah Portfólia Projektov</div>
        <div class="header-tag">Prehľad dokumentácie TZB</div>
    </div>
    <div class="toc-grid">
        <!-- SEKCIA 1 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>I. Inžinierske stavby & Občianska vybavenosť</span>
                <span style="font-size:7pt; color:#64748b;">(ÚK / ZTI)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">01</span>
                    <span class="toc-name">EDU-TECH KAMPUS PÚCHOV (Pôdorysy podlaží a strechy)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 04</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">02</span>
                    <span class="toc-name">EDU-TECH KAMPUS PÚCHOV (Hydraulické schémy)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 05</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">03</span>
                    <span class="toc-name">ASOC – Administratívno-skladové a obchodné centrum</span>
                    <span class="toc-meta">Zdravotechnika (ZTI)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 07</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">04</span>
                    <span class="toc-name">Obecný dom Limbach – Nadstavba</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 09</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">05</span>
                    <span class="toc-name">Vinárske centrum UNIMPEX Svätý Jur</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 13</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">06</span>
                    <span class="toc-name">ADM Komárňanská – Hospodársko-admin. objekt</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 14</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">07</span>
                    <span class="toc-name">Materská škola Nový Svet</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 20</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 2 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>II. Rezidenčná výstavba – Rodinné domy & Byty</span>
                <span style="font-size:7pt; color:#64748b;">(ÚK / Podlahové vykurovanie)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">08</span>
                    <span class="toc-name">Rodinný dom Slivník (RD Imričko)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 06</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">09</span>
                    <span class="toc-name">Byt Zámocká 16, Bratislava (Podkrovný byt)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 15</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">10</span>
                    <span class="toc-name">Rodinný dom Chorvátsky Grob (RD VALUL)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 16</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">11</span>
                    <span class="toc-name">Rodinný dom Vinohrady (RD FIGA)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 17</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">12</span>
                    <span class="toc-name">Rodinný dom Kuchyňa (Baričičova)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 18</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">13</span>
                    <span class="toc-name">Rodinný dom Senec (Gajdošík)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 19</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">14</span>
                    <span class="toc-name">Byt Björnsonova, Bratislava</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 25</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">15</span>
                    <span class="toc-name">Rodinný dom Hviezdoslavov (RD HVZD)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 26</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">16</span>
                    <span class="toc-name">Rodinný dom Podbiel (RD PODBI)</span>
                    <span class="toc-meta">ZTI + ÚK</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 27</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">17</span>
                    <span class="toc-name">Rodinný dom Pod priehradou, Kuchyňa</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 28</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">18</span>
                    <span class="toc-name">Rodinný dom Veľká Paka</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 29</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 3 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>III. Rekreačné objekty & Horské chaty</span>
                <span style="font-size:7pt; color:#64748b;">(Vykurovanie & ZTI)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">19</span>
                    <span class="toc-name">Chata na Jankovej Lúke Štrbské Pleso (Vysoké Tatry)</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 08</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">20</span>
                    <span class="toc-name">Rekreačná chata Zlatá hora, Stupava</span>
                    <span class="toc-meta">Vykurovanie + ZTI</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 21</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">21</span>
                    <span class="toc-name">Rekreačná chata Žľaby, Košice</span>
                    <span class="toc-meta">Elektrické kúrenie</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 22</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">22</span>
                    <span class="toc-name">Záhradná chata Vrakuňa - lesopark</span>
                    <span class="toc-meta">Vykurovanie (ÚK)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 24</span>
                </div>
            </div>
        </div>

        <!-- SEKCIA 4 -->
        <div class="toc-section">
            <div class="toc-sec-title">
                <span>IV. Zdravotechnika (ZTI) & Tepelná technika (TTP)</span>
                <span style="font-size:7pt; color:#64748b;">(Gastro / Posudky)</span>
            </div>
            <div class="toc-items">
                <div class="toc-row">
                    <span class="toc-num">23</span>
                    <span class="toc-name">TTP – FAXCOPY Domkárska, Bratislava</span>
                    <span class="toc-meta">Posúdenie (TTP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 10</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">24</span>
                    <span class="toc-name">Kaviareň Nivy Bratislava (Nivy Centrum)</span>
                    <span class="toc-meta">Gastro ZTI (RP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 11</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">25</span>
                    <span class="toc-name">Kaviareň Klasiko OC Polus, Bratislava</span>
                    <span class="toc-meta">Gastro ZTI (RP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 12</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">26</span>
                    <span class="toc-name">TTP – Výrobná hala Víno Matyšák, Pezinok</span>
                    <span class="toc-meta">Posúdenie (TTP)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 23</span>
                </div>
                <div class="toc-row">
                    <span class="toc-num">27</span>
                    <span class="toc-name">Komplexné rozvody ZTI – Distribúcia a kanalizácia</span>
                    <span class="toc-meta">Zdravotechnika (ZTI)</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">Strana 30</span>
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
</body>
</html>
"""

weasyprint.HTML(string=html).write_pdf("test_toc.pdf")
print("Generated test_toc.pdf successfully!")
