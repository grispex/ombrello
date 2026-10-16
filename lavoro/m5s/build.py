import json,sys
FONTI={
"P22":("m5s-programma-politiche-2022","2022-08","annunciata","nazionale"),
"E24":("m5s-programma-europee-2024","2024-05","annunciata","europeo"),
"A":("m5s-nova2026-ambiente-energia-casa","2026-09","annunciata","nazionale"),
"B":("m5s-nova2026-giustizia-esteri","2026-09","annunciata","nazionale"),
"C":("m5s-nova2026-sanita-lavoro","2026-09","annunciata","nazionale"),
"G":("m5s-nova2026-patto-generazione","2026-09","annunciata","nazionale"),
}
def build(items,out):
    res=[]
    for it in items:
        s,cit,sint,aree,sott,conc=it[:6]
        ex=it[6] if len(it)>6 else {}
        f,d,st,amb=FONTI.get(s,(s,)+("",)*3) if s in FONTI else (s,ex.get("data"),ex.get("stato","annunciata"),ex.get("ambito","nazionale"))
        r={"partiti":["m5s"],"sintesi":sint,"citazione":cit,"fonte":f,"data":ex.get("data",d),"aree":aree.split(),"sottotema":sott,"concretezza":conc,"stato":ex.get("stato",st),"ambito":ex.get("ambito",amb)}
        for k in ("destinatari","parametri","copertura","note","attuale","punto"):
            if k in ex: r[k]=ex[k]
        res.append(r)
    json.dump(res,open(out,"w"),ensure_ascii=False,indent=0)
