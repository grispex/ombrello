import json,subprocess,sys
def run(partito,fonte,partiti,data,out,items,stato="annunciata",ambito="nazionale"):
    L=[]
    for it in items:
        s,c,p,a,sub,k=it[:6]; kw=it[6] if len(it)>6 else {}
        d={"partiti":partiti,"sintesi":s,"citazione":c,"fonte":fonte,"punto":p,"aree":a.split(),"sottotema":sub,"concretezza":k,"stato":kw.pop("stato",stato),"ambito":kw.pop("ambito",ambito)}
        d.update(kw); L.append(d)
    json.dump(L,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    r=subprocess.run(["python3","-I","strumenti/aggiungi.py","proposte",partito,out],cwd="/home/user/ombrello",capture_output=True,text=True)
    print(r.stdout,r.stderr)
