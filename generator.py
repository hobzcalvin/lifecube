import math
import os
from PIL import Image
import random

HASHTAG = 'lifecubeproject'
LIMIT = 25
MAX_RES = 8192

imagedir = f'images-{HASHTAG}'
#TODO: --fast-update? For each target, stop when encountering the first already-downloaded picture. This flag is recommended when you use Instaloader to update your personal Instagram archive.
#os.system(f'instaloader "#{HASHTAG}" --no-videos --no-metadata-json --no-captions --no-profile-pic --dirname-pattern="{imagedir}"')

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

for dim in dims:
    dfiles = files[:dim**2]
    files = files[dim**2:]
    maxdim = 0
    for i in range(len(dfiles)):
        dfiles[i] = Image.open(os.path.join(imagedir, dfiles[i]))
        # Only use the min of width/height because we crop to make squares
        maxdim = max(min(dfiles[i].width, dfiles[i].height), maxdim)
    size = min(MAX_RES, maxdim * dim)
    print("dim", dim, size)
