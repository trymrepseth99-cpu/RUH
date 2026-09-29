import json,sys,time,os,urllib.request,threading
def find(o):
    if isinstance(o,dict):
        if 'DALUX_API_KEY' in o: return o['DALUX_API_KEY']
        for v in o.values():
            r=find(v)
            if r: return r
key=os.environ['DALUX_API_KEY']; P='7657559992'
def get(url):
    for a in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'X-API-KEY':key}),timeout=60))
        except Exception as e:
            print('retry',e,flush=True); time.sleep(2)
    raise
def run(name,url,keep):
    out=[];n=0;t=time.time();seen=set()
    while url:
        d=get(url)
        if not d['items'] or url in seen: break
        seen.add(url); n+=len(d['items'])
        out+= [keep(i) for i in d['items']]
        url=next((l['href'] for l in d.get('links',[]) if l['rel']=='nextPage'),None)
        print(name,n,round(time.time()-t),flush=True)
    json.dump(out,open(name+'.json','w',encoding='utf-8'),ensure_ascii=False)
def kt(t): return t['data']
def kc(c): return c
th=[threading.Thread(target=run,args=('tasks',f'https://field.dalux.com/service/api/5.1/projects/{P}/tasks?limit=100',kt)),
    threading.Thread(target=run,args=('changes',f'https://field.dalux.com/service/api/1.0/projects/{P}/tasks/changes?limit=1000&since=2024-01-01T00:00:00Z',kc))]
[t.start() for t in th];[t.join() for t in th]
print('DONE')
