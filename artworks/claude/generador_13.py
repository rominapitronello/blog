# Deslinde Luminoso — obra 13, banner 1600x900, sin texto, significado en 70% central
# Pluma: Debajo (Claude Fable 5.1, claude.ai) · 08-sep-2026
# Reusa las constantes y helpers de generador.py sin modificarlo (el lote v4 queda intacto).
#
# ---------- 13 EL CRITERIO A LA VISTA ----------
# líneas + marco + dentro/fuera + convergir -> muchos caminos, un fin visible, un perímetro
# Ablación: sin la convergencia los caminos no dicen nada; sin el marco no hay perímetro;
# sin el punto Fuego no hay criterio a la vista. Las tres operaciones cargan sentido.

from PIL import Image, ImageDraw
import math, random, sys, os

W,H = 1600,900
PAPEL=(246,243,237); FUEGO=(232,93,46); GRAFITO=(58,58,74)
CX0,CX1 = int(W*0.15), int(W*0.85)  # zona segura 70%

def canvas(bg=PAPEL):
    return Image.new("RGB",(W,H),bg)

def grain(img, amt=5):
    r=random.Random(7)
    px=img.load()
    for _ in range(int(W*H*0.045)):
        x=r.randrange(W); y=r.randrange(H)
        c=px[x,y]; d=r.randint(-amt,amt)
        px[x,y]=(max(0,min(255,c[0]+d)),max(0,min(255,c[1]+d)),max(0,min(255,c[2]+d)))
    return img

def mix(a,b,t):
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "obras")

img=canvas(); d=ImageDraw.Draw(img)
r=random.Random(13)

# el perímetro: un marco medido, grafito, con el jitter mínimo del oficio
mx0,my0,mx1,my1 = CX0+40, 110, CX1-40, H-110
w=8
for (a,b) in [((mx0,my0),(mx1,my0)),((mx1,my0),(mx1,my1)),((mx1,my1),(mx0,my1)),((mx0,my1),(mx0,my0))]:
    j=lambda: r.uniform(-1.5,1.5)
    d.line([a[0]+j(),a[1]+j(),b[0]+j(),b[1]+j()], fill=GRAFITO, width=w)

# el origen: presencia discreta a la izquierda
ox,oy = mx0+150, H//2
d.ellipse([ox-11,oy-11,ox+11,oy+11], fill=GRAFITO)

# el criterio: un punto Fuego a la derecha, a la vista — con las marcas de agrimensor
# que lo hacen visible desde lejos (no un secreto del juez)
tx,ty = mx1-150, H//2
for ang in range(0,360,30):
    a=math.radians(ang)
    x1=tx+math.cos(a)*26; y1=ty+math.sin(a)*26
    x2=tx+math.cos(a)*46; y2=ty+math.sin(a)*46
    d.line([x1,y1,x2,y2], fill=FUEGO, width=4)
d.ellipse([tx-14,ty-14,tx+14,ty+14], fill=FUEGO)

# los caminos: muchos, distintos, libres en el cómo, todos dentro del marco,
# todos terminan en el mismo punto. Ninguno sale del perímetro.
n_paths=16
inner=(mx0+34, my0+34, mx1-34, my1-34)
for k in range(n_paths):
    steps=r.randint(9,15)
    pts=[(ox,oy)]
    x,y=ox,oy
    # cada camino tiene su propia inclinación vertical: unos suben, otros bajan, otros dudan
    bias=r.uniform(-1,1)
    for s in range(steps):
        t=(s+1)/steps
        # avanza hacia la derecha con velocidad variable
        nx = ox + (tx-ox)*t + r.uniform(-40,40)*(1-t)
        # se aleja del eje y vuelve: libertad en el medio, convergencia al final
        amp = (my1-my0)*0.42
        ny = oy + math.sin(t*math.pi)*amp*bias + r.uniform(-28,28)*(1-t)
        nx=max(inner[0],min(inner[2],nx)); ny=max(inner[1],min(inner[3],ny))
        pts.append((nx,ny))
    pts.append((tx,ty))
    tone=mix(GRAFITO,PAPEL,r.uniform(0.15,0.55))
    width=r.choice([3,3,4,4,5])
    d.line(pts, fill=tone, width=width, joint="curve")

# fuera del marco: nada. El vacío es el perímetro que se respeta.

name="13-el-criterio-a-la-vista.png"
grain(img).save(os.path.join(out_dir,name), "PNG")
print(name)
