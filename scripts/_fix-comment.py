import pathlib

root = pathlib.Path(r"c:\repos\moverstudio.online")
bad = "/* Self-hosted fonts \u0432\u0402\u201d no external dependencies */"
good = "/* Self-hosted fonts - no external dependencies */"
count = 0
for f in root.rglob("*.html"):
    t = f.read_text(encoding="utf-8")
    if bad in t:
        f.write_text(t.replace(bad, good), encoding="utf-8", newline="")
        count += 1
print(f"fixed: {count}")
