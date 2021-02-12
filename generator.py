import math
import os
from PIL import Image
import random

HASHTAG = 'lifecubeproject'
LIMIT = None
MAX_RES = 4096

imagedir = f'images-{HASHTAG}'
outdir = f'textures-{HASHTAG}'
os.makedirs(outdir, exist_ok=True)
os.system(f'instaloader "#{HASHTAG}" --fast-update --no-videos --no-metadata-json --no-captions --no-profile-pic --dirname-pattern="{imagedir}"')

files = [f for f in os.listdir(imagedir) if f.endswith('.jpg')]
random.shuffle(files)
if LIMIT is not None:
    files = files[:LIMIT]
print('files', len(files))

dims = [math.floor(math.sqrt(len(files)/6))] * 6
nimg = None
for i in range(5):
    nimg = sum([d**2 for d in dims])
    if nimg >= len(files):
        break
    dims[i] += 1
print("dims", dims, nimg)
if nimg > len(files):
    files += files[:nimg-len(files)]
    random.shuffle(files)

for (i,dim) in enumerate(dims):
    dfiles = files[:dim**2]
    files = files[dim**2:]
    size = 0
    for f in dfiles:
        img = Image.open(os.path.join(imagedir, f))
        # Only use the min of width/height because we crop to make squares
        size = max(min(img.width, img.height), size)
        img.close()
    size = min(math.floor(MAX_RES / dim), size)
    print("dim", i, dim, size)

    face = Image.new('RGB', (size*dim, size*dim))
    for (j,f) in enumerate(dfiles):
        img = Image.open(os.path.join(imagedir, f))
        if img.width != size or img.height != size:
            src_size = min(img.width, img.height)
            x = 0
            y = 0
            if img.width > src_size:
                x = (img.width-src_size) // 2
            if img.height > src_size:
                y = (img.height-src_size) // 2
            img = img.resize((size, size), Image.LANCZOS,
                             (x, y, x+src_size, y+src_size))
        row = j // dim
        col = j - row*dim
        face.paste(img, (row*size, col*size))
        img.close()
    face.save(os.path.join(outdir, f'{HASHTAG}-{i}.jpg'))
