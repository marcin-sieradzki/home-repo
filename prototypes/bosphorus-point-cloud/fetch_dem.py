import math, subprocess, numpy as np, os
from PIL import Image
z=13
def tile(lat,lon):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n; return x,y
N,S,W,E=41.16,41.02,28.98,29.14
x0,y0=tile(N,W); x1,y1=tile(S,E)
print(x0,y0,x1,y1)
tx=range(int(x0),int(x1)+1); ty=range(int(y0),int(y1)+1)
rows=[]
for y in ty:
  row=[]
  for x in tx:
    f=f"{z}_{x}_{y}.png"
    if not os.path.exists(f): subprocess.run(["curl","-s","-o",f,f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],check=True)
    a=np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    row.append(a[...,0]*256+a[...,1]+a[...,2]/256-32768)
  rows.append(np.concatenate(row,1))
m=np.concatenate(rows,0)
# crop
px0=int((x0-int(x0))*256); py0=int((y0-int(y0))*256); px1=int((x1-int(x0))*256); py1=int((y1-int(y0))*256)
m=m[py0:py1,px0:px1]
print(m.shape,m.min(),m.max())
np.save('crop.npy',m)
v=np.clip(m,-60,250); v=((v+60)/310*255).astype(np.uint8)
Image.fromarray(v).save('preview.png')
