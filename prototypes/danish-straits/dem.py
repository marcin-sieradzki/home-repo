import math, subprocess, os, numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
def txy(lat,lon,z):
    n=2**z; return (lon+180)/360*n, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n
def get(z,x,y):
    f=f"tiles/{z}_{x}_{y}.png"
    if not os.path.exists(f): subprocess.run(["curl","-sf","--retry","3","-o",f,f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],check=True)
    a=np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    return a[...,0]*256+a[...,1]+a[...,2]/256-32768
def crop(N,S,W,E,z):
    x0,y0=txy(N,W,z); x1,y1=txy(S,E,z)
    tx=list(range(int(x0),int(x1)+1)); ty=list(range(int(y0),int(y1)+1))
    with ThreadPoolExecutor(16) as ex:
        tiles={(x,y):r for (x,y),r in zip([(x,y) for y in ty for x in tx], ex.map(lambda p:get(z,*p),[(x,y) for y in ty for x in tx]))}
    m=np.concatenate([np.concatenate([tiles[(x,y)] for x in tx],1) for y in ty],0)
    px0=int((x0-tx[0])*256); py0=int((y0-ty[0])*256); px1=int((x1-tx[0])*256); py1=int((y1-ty[0])*256)
    return m[py0:py1,px0:px1]
