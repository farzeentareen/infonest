from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
n = 0
for p in ROOT.rglob("*.html"):
    if "tools" in p.parts:
        continue
    t = p.read_text(encoding="utf-8")
    orig = t
    t = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*', "\n", t)
    t = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin\s*/>\s*', "\n", t)
    t = re.sub(r'\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+"\s*/>\s*', "\n", t)
    t = re.sub(
        r'\s*<!-- Google AdSense Verification -->\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-2344063334800709" crossorigin="anonymous"></script>\s*',
        "\n",
        t,
    )
    t = re.sub(
        r'\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-2344063334800709" crossorigin="anonymous"></script>\s*',
        "\n",
        t,
    )
    if 'google-adsense-account' not in t and '</title>' in t.lower() or 'google-adsense-account' not in t:
        if 'google-adsense-account' not in t:
            t = t.replace(
                '<link rel="icon"',
                '  <meta name="google-adsense-account" content="ca-pub-2344063334800709" />\n  <link rel="icon"',
                1,
            )
            if 'google-adsense-account' not in t:
                t = re.sub(
                    r'(<meta charset="UTF-8"\s*/>)',
                    r'\1\n  <meta name="google-adsense-account" content="ca-pub-2344063334800709" />',
                    t,
                    count=1,
                    flags=re.I,
                )
    if t != orig:
        p.write_text(t, encoding="utf-8")
        n += 1
print("updated", n)
