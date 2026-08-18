from pathlib import Path

root = Path(__file__).resolve().parents[1]
n = 0
for p in root.rglob("*.html"):
    t = p.read_text(encoding="utf-8")
    orig = t
    t = t.replace('href="/author/alex-morgan/"', 'href="/about/"')
    t = t.replace("View all articles", "About InfoNest")
    t = t.replace('author-avatar-placeholder">AM', 'author-avatar-placeholder">IN')
    t = t.replace(
        "</div>\n        \n          <h2 id=\"practical-framework\">",
        "\n          <h2 id=\"practical-framework\">",
    )
    if t != orig:
        p.write_text(t, encoding="utf-8")
        n += 1
print("updated", n)
