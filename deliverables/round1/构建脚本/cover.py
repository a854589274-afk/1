import math, sys
NAVY='#1F3A5F'; TEAL='#148F8A'; ORANGE='#E8833A'
W,H=1920,1080
out=[]
a=out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2E8F99" stop-opacity="0.55"/><stop offset="100%" stop-color="#2E8F99" stop-opacity="0"/></radialGradient>
<radialGradient id="bgl" cx="70%" cy="45%" r="60%"><stop offset="0%" stop-color="#27486F"/><stop offset="100%" stop-color="#1F3A5F"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0B1A2C" flood-opacity="0.45"/></filter>
<linearGradient id="line" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#3FC1B8" stop-opacity="0.35"/><stop offset="100%" stop-color="#3FC1B8" stop-opacity="0.95"/></linearGradient>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#bgl)"/>')
CX,CY=1350,330
# faint concentric rings
for r,op in [(140,.10),(230,.07),(330,.05),(450,.035)]:
    a(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#3FC1B8" stroke-opacity="{op}" stroke-width="2"/>')
# faint dot grid on right
for i in range(0,14):
    for j in range(0,9):
        x=880+i*75; y=110+j*95
        if x<W-30: a(f'<circle cx="{x}" cy="{y}" r="2" fill="#FFFFFF" fill-opacity="0.06"/>')
# floor platform
a('<ellipse cx="1350" cy="935" rx="560" ry="70" fill="#183150" fill-opacity="0.9"/>')
a('<ellipse cx="1350" cy="925" rx="520" ry="52" fill="#24456E" fill-opacity="0.7"/>')

def tubes(x,y,n,w=9,h=30,gap=6,orange_idx=None):
    s=[]
    for k in range(n):
        tx=x+k*(w+gap)
        cap=ORANGE if k==orange_idx else NAVY
        s.append(f'<rect x="{tx}" y="{y}" width="{w}" height="{h}" rx="3" fill="#FFFFFF" fill-opacity="0.95"/>')
        s.append(f'<rect x="{tx}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" rx="3" fill="#C94A3F" fill-opacity="0.55"/>')
        s.append(f'<rect x="{tx-1}" y="{y-6}" width="{w+2}" height="8" rx="2" fill="{cap}"/>')
    return ''.join(s)

def screen(x,y,w,h):
    pts=[]
    for k in range(9):
        px=x+10+k*(w-20)/8; py=y+h*0.62-math.sin(k*0.9)*h*0.18-k*h*0.02
        pts.append(f'{px:.1f},{py:.1f}')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{TEAL}"/>'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

def carousel(cx,cy,r):
    s=[f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#D3DDE7"/>',f'<circle cx="{cx}" cy="{cy}" r="{r*0.72}" fill="#BCCADA"/>']
    for k in range(10):
        ang=k*36*math.pi/180
        s.append(f'<circle cx="{cx+r*0.86*math.cos(ang):.1f}" cy="{cy+r*0.86*math.sin(ang):.1f}" r="{r*0.11:.1f}" fill="{NAVY}" fill-opacity="0.75"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.22}" fill="{TEAL}"/>')
    return ''.join(s)

tops=[]
def analyzer(bx,by,variant,scale=1.0):
    g=[f'<g transform="translate({bx},{by}) scale({scale})" filter="url(#sh)">']
    if variant=='tall':
        w,h=170,250
        g.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="16" fill="#E9EFF5"/>')
        g.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="38" rx="16" fill="#D5DFE9"/>')
        g.append(screen(-w/2+18,-h+56,w-36,64))
        g.append(carousel(0,-h+168,34))
        g.append(f'<rect x="{-w/2+14}" y="-46" width="{w-28}" height="30" rx="6" fill="#C9D5E1"/>')
        g.append(f'<circle cx="{w/2-20}" cy="{-h+19}" r="6" fill="{ORANGE}"/>')
    elif variant=='wide':
        w,h=250,160
        g.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="16" fill="#E9EFF5"/>')
        g.append(f'<rect x="{-w/2}" y="{-h-40}" width="{w*0.55}" height="48" rx="12" fill="#D5DFE9"/>')
        g.append(screen(w/2-100,-h+18,82,58))
        g.append(carousel(-w/2+60,-h+70,40))
        g.append(tubes(-w/2+20,-40,8,orange_idx=3))
        g.append(f'<circle cx="{w/2-22}" cy="-28" r="6" fill="{TEAL}"/>')
        h=h+40
    elif variant=='module':
        w,h=270,190
        for k,dx in enumerate([-w/2, 0]):
            g.append(f'<rect x="{dx+2}" y="{-h}" width="{w/2-4}" height="{h}" rx="14" fill="#E9EFF5"/>')
            g.append(carousel(dx+w/4,-h+62,30))
            g.append(f'<rect x="{dx+18}" y="{-h+112}" width="{w/2-40}" height="22" rx="5" fill="#C9D5E1"/>')
        g.append(f'<rect x="{-w/2-30}" y="-70" width="{w+60}" height="70" rx="12" fill="#D5DFE9"/>')
        g.append(tubes(-w/2-14,-58,14,orange_idx=9))
        g.append(screen(-48,-h-52,96,44))
        g.append(f'<rect x="-6" y="{-h-10}" width="12" height="12" fill="#C9D5E1"/>')
        h=h+52
    elif variant=='compact':
        w,h=150,150
        g.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="18" fill="#E9EFF5"/>')
        g.append(f'<path d="M {-w/2+10} {-h+8} Q 0 {-h-46} {w/2-10} {-h+8} Z" fill="#D5DFE9"/>')
        g.append(screen(-w/2+16,-h+22,w-32,50))
        g.append(tubes(-w/2+18,-50,6,orange_idx=None))
        g.append(f'<circle cx="{w/2-18}" cy="-24" r="6" fill="{ORANGE}"/>')
        h=h+30
    elif variant=='hood':
        w,h=190,210
        g.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="16" fill="#E9EFF5"/>')
        g.append(f'<rect x="{-w/2+12}" y="{-h-26}" width="{w-24}" height="34" rx="10" fill="#D5DFE9" fill-opacity="0.9"/>')
        g.append(carousel(-30,-h+70,40))
        g.append(screen(26,-h+30,w/2-40,70))
        g.append(tubes(-w/2+20,-52,9,orange_idx=6))
        g.append(f'<rect x="{-w/2+14}" y="-14" width="{w-28}" height="6" rx="3" fill="#C9D5E1"/>')
        h=h+26
    g.append('</g>')
    tops.append((bx, by-h*scale+4))
    return ''.join(g)

units=[(940,872,'compact',0.95),(1775,872,'wide',0.88),(1118,908,'tall',0.92),(1582,908,'hood',0.92),(1350,930,'module',0.86)]
body=[analyzer(*u) for u in units]
# data lines first (behind analyzers)
for i,(tx,ty) in enumerate(tops):
    c1x=tx; c1y=ty-150; c2x=CX+(tx-CX)*0.25; c2y=CY+140
    d=f'M {tx:.1f} {ty:.1f} C {c1x:.1f} {c1y:.1f}, {c2x:.1f} {c2y:.1f}, {CX} {CY+18}'
    a(f'<path d="{d}" fill="none" stroke="url(#line)" stroke-width="4" stroke-linecap="round"/>')
    a(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.5" stroke-dasharray="2 14" stroke-linecap="round"/>')
    a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="7" fill="#3FC1B8"/>')
    # data packets along curve
    for t in (0.3,0.62):
        x=(1-t)**3*tx+3*(1-t)**2*t*c1x+3*(1-t)*t*t*c2x+t**3*CX
        y=(1-t)**3*ty+3*(1-t)**2*t*c1y+3*(1-t)*t*t*c2y+t**3*(CY+18)
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#3FC1B8"/>')
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#3FC1B8" fill-opacity="0.2"/>')
# convergence point
a(f'<circle cx="{CX}" cy="{CY}" r="120" fill="url(#glow)"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="44" fill="{TEAL}" fill-opacity="0.35"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="28" fill="{TEAL}"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="28" fill="none" stroke="#FFFFFF" stroke-opacity="0.7" stroke-width="3"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="10" fill="{ORANGE}"/>')
out.extend(body)
a('</svg>')
open(sys.argv[1],'w').write('\n'.join(out))
