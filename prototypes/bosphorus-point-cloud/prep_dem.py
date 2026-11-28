import numpy as np, json
from PIL import Image
from scipy import ndimage as nd
m=np.load('dem/crop.npy')
# downsample x2 (area mean)
H,W=m.shape; m=m[:H//2*2,:W//2*2].reshape(H//2,2,W//2,2).mean((1,3))
m=nd.gaussian_filter(m,0.6)
water=m<1.2
lab,n=nd.label(water); sizes=nd.sum(water,lab,range(1,n+1)); main=lab==(1+np.argmax(sizes))
dist=nd.distance_transform_edt(main)
H,W=m.shape; print(H,W, main.mean())
center=[]
for r in range(H):
    row=dist[r]
    if row.max()<3: continue
    center.append([r,float(np.argmax(row)),float(row.max())])
c=np.array(center); c[:,1]=nd.gaussian_filter1d(c[:,1],12)
pts=c[::6,:3].round(1).tolist()
h=np.clip(np.round(m*10),0,65535).astype(np.uint16); h[~main & (m<1.2)]=12  # small inland water: keep at ~1.2m
h[main]=0
rgb=np.zeros((H,W,3),np.uint8); rgb[...,0]=h>>8; rgb[...,1]=h&255
Image.fromarray(rgb).save('proto/heights.png')
json.dump({"w":W,"h":H,"cellMeters":29.4,"centerline":pts},open('proto/meta.json','w'))
print(len(pts))
