import weasyprint

html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: A4; margin: 20mm; }
body { font-family: sans-serif; color: #111; }
h1 { color: #0284c7; }
</style>
</head>
<body>
<h1>Portfólio Projektov TZB - Ing. Viktor Labovský</h1>
<p>Test slovenských znakov: Ľščťžýáíéúäô / Dôraz na kvalitu</p>
</body>
</html>
"""

weasyprint.HTML(string=html_content).write_pdf("test_output.pdf")
print("Successfully generated test_output.pdf")
