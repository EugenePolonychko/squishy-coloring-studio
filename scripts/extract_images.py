import base64, pathlib, re
p=pathlib.Path("index.html")
html=p.read_text(encoding="utf-8")
m=re.search(r'const\s+sceneImages\s*=\s*\[(.*?)\];',html,re.S)
if not m:
    raise SystemExit("Could not find sceneImages; index.html unchanged")
uris=re.findall(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)',m.group(1))
if len(uris)!=12:
    raise SystemExit(f"Expected 12 embedded illustrations; found {len(uris)}. No changes made.")
folder=pathlib.Path("images")
folder.mkdir(exist_ok=True)
paths=[]
for i,(ext,payload) in enumerate(uris,1):
    ext="jpg" if ext=="jpeg" else ext
    name=f"scene-{i:02d}.{ext}"
    (folder/name).write_bytes(base64.b64decode(payload,validate=True))
    paths.append("./images/"+name)
replacement="const sceneImages="+str(paths).replace("'",'"')+";"
html=html[:m.start()]+replacement+html[m.end():]
if "name=\"viewport\"" not in html:
    html=html.replace("<head>","<head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1,maximum-scale=1\">",1)
p.write_text(html,encoding="utf-8")
print("Split 12 images; optimized HTML size:",len(html))
