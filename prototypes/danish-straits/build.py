import numpy as np, json, heapq, math
from PIL import Image
from scipy import ndimage as nd
LAND=0.0
def enc(m,path):
    h=np.clip(np.round((m+1000)*10),0,65535).astype(np.uint16)
    rgb=np.zeros(m.shape+(3,),np.uint8); rgb[...,0]=h>>8; rgb[...,1]=h&255
    Image.fromarray(rgb).save(path,optimize=True)
def astar(cost,a,b):
    H,W=cost.shape; INF=1e18; g=np.full((H,W),INF); g[a]=0; prev={}; pq=[(0,a)]
    nb=[(-1,0,1),(1,0,1),(0,-1,1),(0,1,1),(-1,-1,1.414),(-1,1,1.414),(1,-1,1.414),(1,1,1.414)]
    while pq:
        f,(r,c)=heapq.heappop(pq)
        if (r,c)==b: break
        gc=g[r,c]
        for dr,dc,l in nb:
            rr,cc=r+dr,c+dc
            if 0<=rr<H and 0<=cc<W and cost[rr,cc]<1e9:
                ng=gc+l*cost[rr,cc]
                if ng<g[rr,cc]:
                    g[rr,cc]=ng; prev[(rr,cc)]=(r,c)
                    heapq.heappush(pq,(ng+math.hypot(rr-b[0],cc-b[1]),(rr,cc)))
    p=[b]
    while p[-1]!=a: p.append(prev[p[-1]])
    return p[::-1]
def clean(m):
    hp=m-nd.gaussian_filter(m,1.5); rough=np.sqrt(np.maximum(nd.uniform_filter(hp**2,5),0))
    cand=(m<4)&(rough<0.08)|(m<0.4)
    cand=nd.binary_opening(cand,structure=np.ones((5,5)))|(m<-0.5)
    lab,n=nd.label(cand); keep=np.unique(lab[(m<-1)&cand]); keep=keep[keep>0]
    water=np.isin(lab,keep)
    water=~nd.binary_opening(~water,structure=np.ones((2,2)))
    out=m.copy(); out[water]=np.minimum(m[water],-0.5); out[~water]=np.maximum(m[~water],0.5)
    return out
def costmap(m,clear):
    water=m<LAND
    d=nd.distance_transform_edt(water)
    depth=np.clip(-m,0,None)
    c=1+6*np.exp(-depth/8)+12*np.exp(-d/clear)
    c[d<2]=400
    bridge=nd.binary_closing(water,structure=np.ones((7,7)))&~water
    c[bridge]=15
    return c
def snap(m,rc):
    water=(m<LAND)&(nd.distance_transform_edt(m<LAND)>=3)
    idx=np.argwhere(water); k=np.argmin(((idx-np.array(rc))**2).sum(1)); return tuple(idx[k])
def smooth(path,s,step):
    p=np.array(path,float)
    p[:,0]=nd.gaussian_filter1d(p[:,0],s,mode='nearest'); p[:,1]=nd.gaussian_filter1d(p[:,1],s,mode='nearest')
    return p[::step]
out={}
# overview
ov=np.load('ov_raw.npy'); H,W=ov.shape; ov=ov[:H//2*2,:W//2*2].reshape(H//2,2,W//2,2).mean((1,3)); ov=np.where(ov<0.4,np.minimum(ov,-0.5),np.maximum(ov,0.5))
enc(ov,'out/overview.png')
OB=dict(n=57.9,s=54.45,w=7.9,e=13.2)
out['overview']=dict(file='overview.png',w=ov.shape[1],h=ov.shape[0],bounds=[OB['n'],OB['s'],OB['w'],OB['e']])
def ll2rc(B,shape,la,lo): return (int((B['n']-la)/(B['n']-B['s'])*shape[0]), int((lo-B['w'])/(B['e']-B['w'])*shape[1]))
def rc2ll(B,shape,r,c): return [round(B['n']-r/shape[0]*(B['n']-B['s']),5), round(B['w']+c/shape[1]*(B['e']-B['w']),5)]
cost=costmap(ov,4)
ROUTES={ # ambient traffic, lat/lon waypoints
 "skagerrak-oresund":[(57.75,8.2),(57.85,10.7),(56.9,11.3),(56.1,12.55),(55.6,12.75),(54.95,13.1)],
 "t-route":[(57.80,10.9),(56.6,11.25),(55.9,11.0),(55.3,11.05),(54.75,10.95),(54.55,11.35)],
 "goteborg-frederikshavn":[(57.65,11.6),(57.44,10.62)],
 "aarhus-kattegat":[(56.15,10.3),(56.3,10.9),(56.6,11.6)],
 "lillebaelt":[(55.75,10.15),(55.55,9.78),(55.45,9.75),(55.1,9.95),(54.8,10.2)],
 "north-sea":[(57.0,8.05),(56.2,7.95),(55.3,8.0)],
 "kiel-copenhagen":[(54.5,10.6),(54.6,11.8),(55.0,12.4),(55.5,12.75)],
}
out['routes']={}
for k,wps in ROUTES.items():
    pts=[snap(ov,ll2rc(OB,ov.shape,*w)) for w in wps]
    path=[]
    for a,b in zip(pts,pts[1:]): seg=astar(cost,a,b); path+=seg if not path else seg[1:]
    sp=smooth(path,4,3)
    out['routes'][k]=[rc2ll(OB,ov.shape,r,c) for r,c in sp]
    print(k,len(sp))
# patches
info=json.load(open('patches.json'))
ENDS={"oresund":[(0.42,0.01),(0.5,0.99)],"storebaelt":[(0.55,0.01),(0.5,0.99)],"lillebaelt":[(0.75,0.02),(0.3,0.99)],"skagen":[(0.02,0.25),(0.98,0.9)]}
out['patches']={}
for k,B in info.items():
    m=clean(np.load(f'p_{k}.npy'))
    small=m[::2,::2]; c=costmap(small,8)
    a=snap(small,(int(ENDS[k][0][1]*small.shape[0]),int(ENDS[k][0][0]*small.shape[1])))
    b=snap(small,(int(ENDS[k][1][1]*small.shape[0]),int(ENDS[k][1][0]*small.shape[1])))
    path=astar(c,a,b); landc=[(r,cc) for r,cc in path if small[r,cc]>=LAND]; print(k,'land cells',len(landc))
    yy,xx=np.mgrid[0:m.shape[0],0:m.shape[1]]
    for r,cc in landc:
        R,C=2*r,2*cc; sl=(slice(max(0,R-14),R+15),slice(max(0,C-14),C+15))
        disk=(yy[sl]-R)**2+(xx[sl]-C)**2<=12**2; m[sl][disk]=-4.0
    enc(m,f'out/patch-{k}.png'); p=smooth(path,10,4)
    route=[rc2ll(B,small.shape,r,cc) for r,cc in p]
    out['patches'][k]=dict(file=f'patch-{k}.png',w=m.shape[1],h=m.shape[0],bounds=[B['n'],B['s'],B['w'],B['e']],route=route)
    print(k,len(route))
json.dump(out,open('out/meta.json','w'))
