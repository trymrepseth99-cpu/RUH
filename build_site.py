import json,base64,datetime,os
from compat import compat
FOLDER="LnsIpb4xfmjasr9s7ae5xugtLI2x4Kaj"
d=json.load(open("ruh.json",encoding="utf-8"))
for x in d:
    x.pop("id",None);x.pop("wf",None)
logo="data:image/png;base64,"+base64.b64encode(open("logo.png","rb").read()).decode()
t=open("tv.tpl.html",encoding="utf-8").read()
t=t.replace("<title>RUH-tavle Campus Diakonhjemmet</title>",'<title>RUH-tavle</title><meta name="robots" content="noindex,nofollow">',1)
t=t.replace("__LOGO__",logo).replace("__DATA__",json.dumps(d,ensure_ascii=False,separators=(",",":"))).replace("__DATE__",datetime.date.today().strftime("%d.%m.%Y"))
t=compat(t)
os.makedirs(FOLDER,exist_ok=True)
open(FOLDER+"/index.html","w",encoding="utf-8").write(t)
print("ok",len(t))

FOLDER2="I34P4eh17y95xuDE5FtIT4IBUk0tV8JW"
o=open("oversikt.tpl.html",encoding="utf-8").read()
o=o.replace("<title>RUH-oversikt Campus Diakonhjemmet</title>",'<title>RUH-oversikt</title><meta name="robots" content="noindex,nofollow">',1)
o=o.replace("__LOGO__",logo).replace("__DATA__",json.dumps(d,ensure_ascii=False,separators=(",",":"))).replace("__DATE__",datetime.date.today().strftime("%d.%m.%Y"))
os.makedirs(FOLDER2,exist_ok=True)
open(FOLDER2+"/index.html","w",encoding="utf-8").write(o)
print("oversikt ok",len(o))
