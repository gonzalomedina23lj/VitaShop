#!/usr/bin/env python3
"""Normalize authorized public catalogue extraction and build static product routes."""
import csv
import html
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1])
image_dir = Path(sys.argv[2])
products = json.loads(source.read_text())
asset_dir = root / 'dist' / 'assets' / 'products'
asset_dir.mkdir(parents=True, exist_ok=True)
invalid = []
gallery_missing = []
for p in products:
    local = []
    # Gallery indices are embedded in filenames and keep the source order.
    files = sorted(image_dir.glob(p['id'] + '-*.webp'), key=lambda f: int(f.stem.rsplit('-',1)[1]))
    for f in files:
        try:
            with Image.open(f) as image:
                if min(image.size) < 50:
                    invalid.append(str(f))
                    continue
                image.verify()
            if f.resolve() != (asset_dir / f.name).resolve():
                shutil.copyfile(f, asset_dir / f.name)
            local.append('assets/products/' + f.name)
        except Exception as exc:
            invalid.append(str(f) + ': ' + str(exc))
    if not local:
        local = ['assets/image-pending.svg']
        p['imagePending'] = True
    p['sourceImage'] = p.get('gallery', [p['image']])[0]
    p['sourceGallery'] = p.pop('gallery', [])
    p['localGallery'] = local
    p['image'] = local[0]
    p['stockQuantity'] = None
    p['sku'] = None
    p['sourceAvailability'] = 'in_stock' if p['available'] else 'out_of_stock'
    p['retrievedAt'] = '2026-10-12'
    p.pop('enriched', None)
    if len(local) < len(p['sourceGallery']):
        gallery_missing.append({'id':p['id'],'source':len(p['sourceGallery']),'local':len(local)})

assert len(products)==332
assert len({p['id'] for p in products})==332
assert all(p['price']>0 and p['name'] and p['url'] for p in products)
assert all('description' in p and 'categories' in p for p in products)
payload = {'store':'VitaShop','source':'https://vitashop.com.ar/','retrievedAt':'2026-10-12','mode':'review','count':len(products),'products':products}
(root/'dist/assets/catalogue.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
with (root/'catalogue-public.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['id','name','price','compare','available','description','url','image','categories','stockQuantity','sku'])
    writer.writeheader()
    for p in products:
        row={k:p.get(k) for k in writer.fieldnames}
        row['categories']=' > '.join(row['categories'])
        writer.writerow(row)

template=(root/'dist/index.html').read_text()
for p in products:
    slug=urlparse(p['url']).path.rstrip('/').split('/')[-1]
    folder=root/'dist/productos'/slug
    folder.mkdir(parents=True,exist_ok=True)
    page=template.replace('<body data-base="./">',f'<body data-base="../../" data-product="{html.escape(slug,quote=True)}">')
    page=page.replace('<title>VitaShop · Suplementos y vitaminas</title>',f'<title>{html.escape(p["name"])} · VitaShop</title>')
    page=page.replace('href="assets/favicon.svg"','href="../../assets/favicon.svg"').replace('href="style.css"','href="../../style.css"')
    for script in ['store-core.js','app.js']:
        page=page.replace('src="'+script+'"','src="../../'+script+'"')
    folder.joinpath('index.html').write_text(page)

report={'products':len(products),'publiclyAvailable':sum(p['available'] for p in products),'localMainImages':sum(not p.get('imagePending') for p in products),'mainImagesPending':[{'id':p['id'],'name':p['name']} for p in products if p.get('imagePending')],'localGalleryImages':sum(len(p['localGallery']) for p in products if not p.get('imagePending')),'originalGalleryImageUrls':sum(len(p['sourceGallery']) for p in products),'additionalGalleryPhotosNotDownloaded':gallery_missing,'invalidImages':invalid,'privateDatabaseMigrated':False,'livePayments':False,'liveShippingQuotes':False}
(root/'migration-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['additionalGalleryPhotosNotDownloaded','invalidImages','mainImagesPending']},ensure_ascii=False))
