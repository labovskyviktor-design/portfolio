# Projektová pamäť

## 1. Súčasné ciele
- [x] Vyriešiť preskočenú TypeScript kontrolu pri Vite builde (odstránenie cache errorov z predošlého dňa).
- [x] Vytvoriť profesionálnu reprezentačnú PDF knihu portfólia (krycia strana, profil projektanta, obsah, 26 projektov s výkresmi).
- [ ] Pokračovať vo vývoji UI a prispôsobení portfólia (napr. ďalšie projekty, úpravy dát).

## 2. Kľúčové rozhodnutia a ich zdôvodnenie
- **Formát PDF portfólia**: Zvolený formát A4 na šírku (Landscape, 297x210 mm) – najvhodnejší pre prezentáciu technických CAD výkresov (pôdorysy, rozvody, schémy) na monitoroch, tabletoch aj pri tlači.
- **Technológia generovania PDF**: Kombinácia `PyMuPDF` (`fitz`) pre renderovanie pôvodných vektorových výkresov do ostrých rastrových podkladov (max 2400 px, antialiasing) a `WeasyPrint` pre layout s pixel-perfect CSS `@page`.
- **Štruktúra PDF (30 strán)**:
  - Strana 01: Krycia strana (reprezentatívny tmavý technický dizajn, modré akcenty, kontakty)
  - Strana 02: O mne & Profil projektanta (fotografia, zameranie na 3 piliere TZB: ÚK, ZTI, TTP, stupne PD, softvér)
  - Strana 03: Obsah portfólia (kategorizovaný prehľad 4 oblastí s presným linkovaním strán 04 až 30)
  - Strany 04–30: Všetkých 26 projektov (vrátane 2-stranového rozdelenia pre univerzitný Kampus Púchov).
- Vygenerovaný súbor: `Portfolio_Projektov_TZB_Viktor_Labovsky.pdf` (cca 30.4 MB).

## 3. Známe problémy
- (žiadne aktuálne známe problémy)

## 4. Naučené lekcie
- Frontend aplikácia (Vite/React) sa nachádza v podadresári [web/](file:///c:/Users/42191/.gemini/antigravity-ide/scratch/portfolio-projektov/web), vývojový server sa spúšťa tam (`cd web && npm run dev`).
- Generátor PDF knižky sa nachádza v koreňovom priečinku: [build_master_portfolio.py](file:///c:/Users/42191/.gemini/antigravity-ide/scratch/portfolio-projektov/build_master_portfolio.py).
