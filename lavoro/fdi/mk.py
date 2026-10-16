import json,subprocess,sys
CD=["fdi","lega","fi","nm","udc","coraggio-italia","italia-al-centro"]
def run(rows, fontemap, default_partiti=None, label="x"):
    out=[]
    for r in rows:
        f,punto,aree,sub,conc,stato,amb,sint,cit=r[:9]
        extra=r[9] if len(r)>9 else {}
        d=dict(partiti=extra.pop("partiti",default_partiti or ["fdi"]),sintesi=sint,citazione=cit,fonte=fontemap.get(f,f),punto=punto,aree=aree.split(","),sottotema=sub,concretezza=conc,stato=stato,ambito=amb)
        d.update(extra); out.append(d)
    p=f"lavoro/fdi/{label}.json"
    json.dump(out,open(p,"w"),ensure_ascii=False,indent=0)
    print(subprocess.run(["python3","-I","strumenti/aggiungi.py","proposte","fdi",p],capture_output=True,text=True).stdout)
