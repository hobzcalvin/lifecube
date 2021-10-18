import itertools
import json
import math
import os
from PIL import Image
import random
import requests

imagedir = 'img-'
texturedir = 'docs/textures-'
LIMIT = None
MAX_RES = 4096

# Load cubes that have been added through online interface
new_cubes = []
json_url = 'https://jsonblob.com/api/jsonBlob/a20cf86d-a234-11eb-bcc4-9d908892deec'
try:
    new_cubes = requests.get(json_url).json().get('cubes', [])
except:
    pass

# Load cubes stored in repository
cubes = []
with open('cubes.json', 'r') as infile:
    cubes = json.load(infile).get('cubes', [])

# Append existing and new cubes
cubes = cubes + new_cubes
for c in cubes:
    if 'hashtags' in c:
        # Remove hash
        c['hashtags'] = [h.lstrip('#') for h in c['hashtags']]
        # Remove duplicate hashtags
        c['hashtags'] = list(set(c['hashtags']))
        # Sort hashtag lists so they're always the same order
        c['hashtags'].sort()
# Convert each cube to a string using dumps so they're hashable,
# then use set() to remove duplicates, then reconvert to objects
cubes = [json.loads(c) for c in set([json.dumps(c) for c in cubes])]

# Write cube list back to repository
with open('cubes.json', 'w') as outfile:
    json.dump({'cubes': cubes}, outfile)

# Upload cube list back to online interface
try:
    requests.put(json_url, json.dumps({'cubes': cubes}))
except:
    pass

hashtags = ['thefirstonefailssodothis'] + list(set(itertools.chain.from_iterable(
    [c['hashtags'] for c in cubes])))
print('tags', hashtags, flush=True)

password = os.environ.get('INSTA_PASSWORD', 'foo')
print("using password", password, flush=True)

for hashtag in hashtags:
    cmd = f'instalooter hashtag "{hashtag}" "{imagedir}{hashtag}" --new --template "{{code}}" --traceback --username justgranttestaccount --password {password}'
    os.system(cmd)

for c in cubes:
    name = ','.join(c['hashtags'])
    print('cube', name, flush=True)
    outdir = f'{texturedir}{name}'
    os.makedirs(outdir, exist_ok=True)

    files = []
    for h in c['hashtags']:
        files += [os.path.join(imagedir + h, f) for f in os.listdir(imagedir + h) if f.endswith('.jpg')]
    random.shuffle(files)
    if LIMIT is not None:
        files = files[:LIMIT]
    print('files', len(files), flush=True)

    dims = [math.floor(math.sqrt(len(files)/6))] * 6
    nimg = None
    # For each cube face, increase the number of images per side by 1 until
    # we have at least the total number of available files.
    # This for loop should never run its course, because the break case is
    # guaranteed to be reached when i=5.
    for i in range(6):
        nimg = sum([d**2 for d in dims])
        if nimg >= len(files):
            break
        dims[i] += 1
    print("dims", dims, nimg, flush=True)
    if nimg > len(files):
        files += files[:nimg-len(files)]
        random.shuffle(files)

    for (i,dim) in enumerate(dims):
        dfiles = files[:dim**2]
        files = files[dim**2:]
        size = 0
        for f in dfiles:
            img = Image.open(f)
            # Only use the min of width/height because we crop to make squares
            size = max(min(img.width, img.height), size)
            img.close()
        size = min(math.floor(MAX_RES / dim), size)
        print("dim", i, dim, size, flush=True)

        face = Image.new('RGB', (size*dim, size*dim))
        for (j,f) in enumerate(dfiles):
            img = Image.open(f)
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
        face.save(os.path.join(outdir, f'{name}-{i}.jpg'))

os.system(f'git add cubes.json {texturedir}* {imagedir}*')
