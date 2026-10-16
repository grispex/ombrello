import sys; sys.path.insert(0,'/home/user/ombrello/lavoro/avs')
import json
def mk(f,cit,sint,aree,sott,conc,partiti,data,**ex):
    r={"partiti":partiti,"sintesi":sint,"citazione":cit,"fonte":f,"data":data,"aree":aree.split(),"sottotema":sott,"concretezza":conc,"stato":"annunciata","ambito":"nazionale"}
    r.update(ex);return r
L=[
mk("ev-comunicato-patrimoniale-2026-10","la proposta che abbiamo avanzato sulla ‘restituzione fiscale’, che contiene un’imposta sulle grandissime ricchezze a partire dai 5,4 milioni di euro","Introdurre un'imposta sulle grandissime ricchezze a partire da 5,4 milioni di euro ('restituzione fiscale')","fisco","Patrimoni, successioni ed extraprofitti",4,["ev","si"],"2026-10-16",parametri=[{"cosa":"soglia imposta sulle grandi ricchezze","valore":"5,4 milioni di euro"}],note="Pagella Politica e Money.it riferiscono soglie leggermente diverse (5 milioni); in un emendamento alla manovra 2026 AVS aveva proposto 1,3% oltre 2 milioni. Nel programma 2022 la soglia era 5 milioni con aliquota fino al 2% oltre 50 milioni."),
mk("ev-pagella-restituzione-fiscale-2026","Al suo posto, verrebbe introdotta una funzione di calcolo continua.","Sostituire gli scaglioni IRPEF con una funzione continua di calcolo dell'imposta (modello tedesco)","fisco","IRPEF e aliquote",3,["ev","si"],"2026-07",note="FONTE SECONDARIA (Pagella Politica): la proposta e' descritta dai media e l'atto originale non e' stato reperito. Sostituisce nella sostanza la proposta del programma 2022 (no tax area a 12.000 euro, aliquota fino al 65%)."),
mk("ev-comunicato-manovra-difesa-2026-10","Daremo battaglia in Parlamento, emendamento per emendamento, per spostare risorse dalle armi agli ospedali, ai medici, agli infermieri, alla difesa del territorio dalla crisi climatica e alle bollette di chi è in difficoltà.","Spostare risorse dalle spese per armamenti a ospedali, personale sanitario, difesa del territorio e bollette","conti-pubblici sanita difesa","Spesa militare e obiettivi NATO",2,["ev"],"2026-10-16",note="FONTE: dichiarazione di Angelo Bonelli (tipo F), non un atto."),
]
json.dump(L,open('/home/user/ombrello/lavoro/avs/q4.json','w'),ensure_ascii=False)
