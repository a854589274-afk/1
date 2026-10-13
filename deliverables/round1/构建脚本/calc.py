import numpy as np, math
from scipy.stats import studentized_range
# ALT example
A=[48.7,2.35,124.2,2.14]; B=[46.5,2.43,117.4,2.06]
for i,(ma,ca,mb,cb) in enumerate([(A[0],A[1],B[0],B[1]),(A[2],A[3],B[2],B[3])]):
    m=(ma+mb)/2; cv=math.sqrt((ca**2+cb**2)/2)
    print(f"L{i+1}: m总={m:.3f} CV合并={cv:.4f} range={m*0.8:.2f}-{m*1.2:.2f}")
s1A=[45.4,46.3,46.7]; s1B=[44.1,45.9,44.6]; s2A=[126.7,125.5,126.2]; s2B=[124.5,122.7,123.8]
for a,b in [(s1A,s1B),(s2A,s2B)]:
    ma,mb=np.mean(a),np.mean(b); ra,rb=round(ma,1),round(mb,1)
    print(f"means {ma:.4f} {mb:.4f} -> R raw={(ma-mb)/((ma+mb)/2)*100:.3f}% ; R rounded={(ra-rb)/((ra+rb)/2)*100:.3f}% ; tot={(ra+rb)/2}")
# interpolation critical for k=2,n=3 at CV 2.39 using table 4.53/6.80
print("interp n=3:", 4.53+0.39*(6.80-4.53), " n=2:", 8.60+0.39*(12.90-8.60))
# Table A.1 check
cols=[1,2,3,4,5,6,7,8,9,10,15,20,25]
def crit(k,n,cv):
    df = k*(n-1) if n>1 else k-1
    return studentized_range.ppf(0.95,k,df)/math.sqrt(n)*cv
import re
txt=open('work/wst407.txt',encoding='utf-8').read()
rows=[]
for line in txt.splitlines():
    p=[x.strip() for x in line.split('|')]
    if len(p)==15 and p[0].isdigit() and p[1].isdigit():
        try: rows.append((int(p[0]),int(p[1]),[float(x) for x in p[2:]]))
        except: pass
print("rows parsed",len(rows))
bad=[];tot=0
prev_k=None
for idx,(k,n,vals) in enumerate(rows):
    for c,v in zip(cols,vals):
        tot+=1
        f=crit(k,n,c)
        if abs(f-v)>0.0151:
            bad.append((k,n,c,v,round(f,2)))
print("cells",tot,"mismatch",len(bad))
for b in bad: print(b)
