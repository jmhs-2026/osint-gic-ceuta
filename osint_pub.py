import sys,os,json,base64,datetime,re
from zoneinfo import ZoneInfo
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
d64=base64.b64decode;e64=lambda b:base64.b64encode(b).decode()
p,sec,rep=sys.argv[1],sys.argv[2],sys.argv[3]
D=json.load(open(p,encoding="utf-8"));L=D["sections"].setdefault(sec,[])
if rep=="--last":
    print(L[0]["t"] if L else "ninguno");sys.exit()
r=json.load(open(rep,encoding="utf-8"))
# La hora la pone siempre el script (hora real de Madrid), no el informe
_n=datetime.datetime.now(ZoneInfo("Europe/Madrid"));_tx=_n.strftime("%d/%m, %H:%M")
r["actualizado"]=_n.isoformat(timespec="seconds");r["actualizadoTexto"]=_tx
if r.get("titulo"):
    r["titulo"]=(re.sub(r"\(\d{1,2}/\d{1,2},?\s*\d{1,2}:\d{2}\)","(%s)"%_tx,r["titulo"]) if re.search(r"\(\d{1,2}/\d{1,2},?\s*\d{1,2}:\d{2}\)",r["titulo"]) else r["titulo"]+" (%s)"%_tx)
pub=serialization.load_der_public_key(d64(D["pub"]))
k=AESGCM.generate_key(256);iv=os.urandom(12)
ek=pub.encrypt(k,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
it={"t":r.get("actualizado",datetime.datetime.now().astimezone().isoformat()),"ek":e64(ek),"iv":e64(iv),"ct":e64(AESGCM(k).encrypt(iv,json.dumps(r,ensure_ascii=False).encode(),None))}
D["sections"][sec]=([it]+L)[:(1 if sec=="novedades" else 40)]
json.dump(D,open(p,"w",encoding="utf-8"),ensure_ascii=False);print("OK",sec,len(D["sections"][sec]),"informes")
