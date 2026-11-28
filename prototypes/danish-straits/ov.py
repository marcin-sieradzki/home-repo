from dem import *
N,S,W,E=57.9,54.45,7.9,13.2
m=crop(N,S,W,E,9)
print(m.shape,m.min(),m.max())
np.save('ov_raw.npy',m)
v=np.clip(m,-80,150); Image.fromarray(((v+80)/230*255).astype(np.uint8)).save('ov_preview.png')
