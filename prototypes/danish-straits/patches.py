from dem import *
import json, math
P={"oresund":(56.03,12.66),"storebaelt":(55.33,11.03),"lillebaelt":(55.50,9.74),"skagen":(57.73,10.62)}
info={}
for k,(la,lo) in P.items():
    dla=10/111.0; dlo=10/(111.32*math.cos(math.radians(la)))
    N,S,W,E=la+dla,la-dla,lo-dlo,lo+dlo
    m=crop(N,S,W,E,13)
    H,W_=m.shape; m=m[:H//2*2,:W_//2*2].reshape(H//2,2,W_//2,2).mean((1,3))
    np.save(f'p_{k}.npy',m); info[k]=dict(n=N,s=S,w=W,e=E,shape=m.shape)
    v=np.clip(m,-30,60); Image.fromarray(((v+30)/90*255).astype(np.uint8)).save(f'p_{k}.png')
    print(k,m.shape,m.min(),m.max())
json.dump(info,open('patches.json','w'))
