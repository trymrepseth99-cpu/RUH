import json,urllib.request
from collections import Counter,defaultdict
exec(open('fetch2.py').read().split('def run')[0])
comp={}
url=f'https://field.dalux.com/service/api/3.1/projects/{P}/companies?limit=500'
seen=set()
while url and url not in seen:
    seen.add(url);d=get(url)
    for i in d['items']:
        x=i.get('data',i);comp[x.get('companyId')]=x.get('name')
    url=next((l['href'] for l in d.get('links',[]) if l['rel']=='nextPage'),None)
    if not d['items']:break
print(len(comp))
t=json.load(open('tasks.json',encoding='utf-8'));c=json.load(open('changes.json',encoding='utf-8'))
ruh={x['taskId']:x for x in t if x.get('type',{}).get('name')=='RUH'}
ch=defaultdict(list)
for x in c:
    if x['taskId'] in ruh: ch[x['taskId']].append(x)
out=[]
for id,x in ruh.items():
    L=sorted(ch[id],key=lambda z:z['timestamp'])
    st=None;closed=None;resp=None;dl=None
    for z in L:
        s=z.get('fields',{}).get('status')
        if s: st=s.lower()
        if z['action']=='complete' or (s and s.lower()=='closed'): closed=z['timestamp']
        if st!='closed': closed=None
        f=z.get('fields',{})
        if 'deadline' in f: dl=f['deadline'].get('value')
    u={i['name']:i['values'] for i in x.get('userDefinedFields',{}).get('items',[])}
    def ref(n):
        v=u.get(n)
        return (v[0].get('reference',{}).get('value') or v[0].get('text')) if v else None
    fv=u.get('Direkte involvert firma')
    cid=fv[0].get('relation',{}).get('companyId') if fv else None
    out.append(dict(id=id,nr=x['number'],tittel=x['subject'],opprettet=x['created'][:10],
      status=st or 'open',lukket=closed[:10] if closed else None,frist=dl[:10] if dl else None,
      wf=x.get('workflow',{}).get('name'),klass=ref('Klassifisering'),risiko=ref('Risikoområde (Tapspotensial)'),
      tiltak=ref('Status tiltak'),fokus=ref('Fokusområde'),firma=comp.get(cid) or ('Ukjent' if not cid else cid)))
json.dump(out,open('ruh.json','w',encoding='utf-8'),ensure_ascii=False)
for k in ['status','klass','risiko','tiltak','fokus','firma','wf']:
    print(k,Counter(o[k] for o in out).most_common(12))
print(min(o['opprettet'] for o in out),max(o['opprettet'] for o in out))
