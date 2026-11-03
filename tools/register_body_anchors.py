"""Register generated pixels to a common planted shoe anchor, without drawing.

Tail exposure changes silhouette centroids. Shoe-based registration keeps the
body planted while the tail moves. Locomotion/jump retain intra-row foot motion.
"""
from pathlib import Path
from statistics import median
import argparse,json
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--frames-root');p.add_argument('--atlas');p.add_argument('--row-strip');p.add_argument('--output');p.add_argument('--json-out',required=True);p.add_argument('--target-x',type=float,default=98)
a=p.parse_args();pending=[];records=[]

def anchor(im):
    alpha=im.getchannel('A');box=alpha.point(lambda v:255 if v>16 else 0).getbbox()
    if box is None:raise ValueError('Blank sprite')
    xs=[x+0.5 for y in range(max(box[1],box[3]-8),box[3]) for x in range(im.width) if alpha.getpixel((x,y))>16]
    return sum(xs)/len(xs)

def shifted(im,dx,label):
    box=im.getbbox()
    if box[0]+dx<3 or box[2]+dx>189:raise ValueError(f'{label} anchor translation would clip or approach edge: bbox={box}, dx={dx}')
    out=Image.new('RGBA',im.size);out.alpha_composite(im,(dx,0));records.append({'frame':label,'anchor_before':anchor(im),'offset_x':dx,'anchor_after':anchor(out),'bbox_after':out.getbbox()});return out

if a.frames_root:
    root=Path(a.frames_root)
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():continue
        files=sorted(directory.glob('*.png'));ims=[Image.open(f).convert('RGBA') for f in files]
        centers=[anchor(im) for im in ims]
        row_dx=round(a.target_x-median(centers))
        for f,im,center in zip(files,ims,centers):
            dx=row_dx if directory.name in {'running-right','running-left','jumping'} else round(a.target_x-center)
            pending.append((shifted(im,dx,f'{directory.name}/{f.name}'),f))
elif a.row_strip:
    original=Image.open(a.row_strip).convert('RGBA')
    if original.size!=(1536,208):raise ValueError('Registered look row must be1536x208')
    output=Image.new('RGBA',original.size)
    for col in range(8):
        im=original.crop((col*192,0,(col+1)*192,208));im=shifted(im,round(a.target_x-anchor(im)),f'look-row/{col}');output.alpha_composite(im,(col*192,0))
    pending.append((output,Path(a.output or a.row_strip)))
elif a.atlas:
    output=Image.open(a.atlas).convert('RGBA')
    if output.size!=(1536,2288):raise ValueError('Need v2 atlas')
    for row in [9,10]:
        for col in range(8):
            box=(col*192,row*208,(col+1)*192,(row+1)*208);im=output.crop(box)
            im=shifted(im,round(a.target_x-anchor(im)),f'look-{row}/{col}');output.paste(im,box)
    pending.append((output,Path(a.output or a.atlas)))
else:raise ValueError('Provide frames-root, row-strip or atlas')
for im,path in pending:im.save(path)
Path(a.json_out).write_text(json.dumps({'ok':True,'method':'shared shoe-anchor target; row-wide translation preserves locomotion and jump foot motion','target_x':a.target_x,'pixels_redrawn':False,'frames':records},indent=2)+'\n')
print(json.dumps({'ok':True,'registered_frames':len(records),'target_x':a.target_x}))
