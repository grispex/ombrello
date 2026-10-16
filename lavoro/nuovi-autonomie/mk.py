"""Costruisce blocchi JSON di proposte da una spec compatta.
Uso: python3 -I mk.py <partito> <spec.txt> <outprefix>
Spec: direttive '@fonte id', '@stato x', '@ambito x', '@punto x', '@data x'
Riga: L | start | end | sintesi | aree(,) | sottotema | conc[E] | [punto] | [dest(,)]
"""
import sys, json, re, os
BASE="/home/user/ombrello"
partito, spec, out = sys.argv[1:4]
fonte=stato=ambito=punto=data=None
join=False
cache={}
blocks=[]; err=0
for n,raw in enumerate(open(spec,encoding="utf-8"),1):
    raw=raw.rstrip("\n")
    if not raw.strip() or raw.startswith("#"): continue
    if raw.startswith("@"):
        k,v=raw[1:].split(" ",1); v=v.strip()
        if k=="fonte": fonte=v
        elif k=="stato": stato=v
        elif k=="ambito": ambito=v
        elif k=="punto": punto=v
        elif k=="data": data=v
        elif k=="join": join=(v=="1")
        continue
    raw=raw.replace(" | | "," | - | ").replace(" | | "," | - | ")
    f=[("" if x.strip()=="-" else x.strip()) for x in raw.split(" | ")]
    while len(f)<9: f.append("")
    L,st,en,sint,aree,sott,conc,pt,dest=f[:9]
    if fonte not in cache:
        _t=open(os.path.join(BASE,"corpus",partito,fonte+".txt"),encoding="utf-8").read()
        cache[fonte]=_t.split("\n")
        cache[fonte+"#j"]=re.sub(r"\s*\n\s*"," ",re.sub(r"(?<=[a-zäöüß])-\n(?=[a-zäöüß])","",_t))
    lines=cache[fonte]
    line=cache[fonte+"#j"] if join else lines[int(L)-1]
    line=re.sub(r"^\s*[-•]\s+","",line).strip()
    try:
        i=line.index(st) if st else 0
        if en:
            j=line.index(en,i)+len(en)
        else:
            j=len(line)
            if j-i>650:
                k=line.find(". ",i)
                if k>0: j=k+1
    except ValueError:
        print(f"spec riga {n}: snippet non trovato: {st!r}/{en!r} in linea {L}"); err+=1; continue
    cit=line[i:j].strip()
    if len(cit)>650:
        print(f"spec riga {n}: citazione lunga {len(cit)}"); err+=1; continue
    amb=ambito or "nazionale"
    if conc.endswith("E"): amb="europeo"; conc=conc[:-1]
    p={"partiti":[partito],"sintesi":sint,"citazione":cit,"fonte":fonte,"punto":pt or punto,"aree":[a.strip() for a in aree.split(",")],"sottotema":sott,"concretezza":int(conc),"stato":stato or "annunciata","ambito":amb}
    if data: p["data"]=data
    if dest: p["destinatari"]=[d.strip() for d in dest.split(",")]
    blocks.append(p)
for k in range(0,len(blocks),35):
    json.dump(blocks[k:k+35],open(f"{out}_{k//35+1}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(blocks),"proposte in",(len(blocks)+34)//35,"blocchi; errori",err)
