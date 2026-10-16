import json
FONTI={"P22":("ev-avs-programma-politiche-2022","2022-08","annunciata","nazionale"),
"E24":("ev-avs-programma-europee-2024","2024-05","annunciata","europeo")}
def build(items,out,partiti=("ev","si")):
    res=[]
    for it in items:
        s,cit,sint,aree,sott,conc=it[:6]
        ex=it[6] if len(it)>6 else {}
        f,d,st,amb=FONTI[s]
        r={"partiti":list(ex.get("partiti",partiti)),"sintesi":sint,"citazione":cit,"fonte":f,"data":d,"aree":aree.split(),"sottotema":sott,"concretezza":conc,"stato":st,"ambito":amb}
        for k in ("destinatari","parametri","copertura","note","attuale","punto"):
            if k in ex:r[k]=ex[k]
        res.append(r)
    json.dump(res,open(out,"w"),ensure_ascii=False,indent=0)
