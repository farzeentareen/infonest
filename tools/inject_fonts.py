from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIP = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" />
"""
n = 0
for p in ROOT.rglob("*.html"):
    if "tools" in p.parts:
        continue
    t = p.read_text(encoding="utf-8")
    if "fonts.googleapis.com" in t:
        continue
    if '<link rel="stylesheet" href="/assets/css/main.css"' in t:
        t = t.replace(
            '<link rel="stylesheet" href="/assets/css/main.css"',
            SNIP + '  <link rel="stylesheet" href="/assets/css/main.css"',
            1,
        )
        p.write_text(t, encoding="utf-8")
        n += 1
print("font links added", n)
