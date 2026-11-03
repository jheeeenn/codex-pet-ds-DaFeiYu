"""Apply one shared scale and ground transform per extracted animation row.

Uses only extracted generated pixels; preserves every pose's displacement.
"""
from pathlib import Path
from statistics import median
import json
import sys
from PIL import Image
run=Path(sys.argv[1]).resolve()
target_height=int(sys.argv[2]) if len(sys.argv)>2 else 165
raw=run/'qa/extracted-frames'
out=run/'frames';out.mkdir(exist_ok=True)
manifest=json.loads((raw/'frames-manifest.json').read_text())
transforms=[]
for row in manifest['rows']:
    state=row['state']
    images=[Image.open(p).convert('RGBA') for p in sorted((raw/state).glob('*.png'))]
    boxes=[im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox() for im in images]
    # A single row transform, never an individual pose fit.
    nominal=median(b[3]-b[1] for b in boxes)
    scale=min(1.0,target_height/nominal)
    ground=max(b[3] for b in boxes)
    shift_x=round(96*(1-scale));shift_y=200-round(ground*scale)
    directory=out/state;directory.mkdir(exist_ok=True)
    for i,im in enumerate(images):
        scaled=im.resize((round(192*scale),round(208*scale)),Image.Resampling.NEAREST)
        target=Image.new('RGBA',(192,208));target.alpha_composite(scaled,(shift_x,shift_y))
        target.save(directory/f'{i:02d}.png')
    row['frames']=[str(p) for p in sorted(directory.glob('*.png'))]
    transforms.append({'state':state,'shared_scale':scale,'nominal_source_height':nominal,'source_ground':ground,'offset':[shift_x,shift_y]})
(out/'frames-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(run/'qa/standard-registration.json').write_text(json.dumps({'method':'one shared transform per row; original intra-row motion preserved','target_body_height':target_height,'target_ground':200,'rows':transforms},indent=2)+'\n')
print(json.dumps(transforms,indent=2))
