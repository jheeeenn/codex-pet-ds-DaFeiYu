"""Match one coherent source row's physical scale to its mirrored-angle family.

This only resizes the complete generated source strip with one uniform factor;
all generated pixels, pose order, spacing and relative anatomy are preserved.
The bundled atlas assembler still applies the common final registration.
"""
from pathlib import Path
from statistics import median
import argparse
import json
import sys
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--row-9',required=True)
parser.add_argument('--row-10',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--json-out',required=True)
parser.add_argument('--chroma-key',required=True)
parser.add_argument('--skill-scripts',required=True)
args=parser.parse_args()
sys.path.insert(0,args.skill_scripts)
from extract_strip_frames import remove_chroma_background,component_frame_groups,component_bounds,parse_hex_color
key=parse_hex_color(args.chroma_key)

def geometries(path):
    im=Image.open(path).convert('RGBA')
    cut=remove_chroma_background(im,key,96.0)
    groups=component_frame_groups(cut,8)
    if groups is None or len(groups)!=8:raise SystemExit('Need 8 complete connected pose groups per source row')
    boxes=[component_bounds(group) for group in groups]
    return im,boxes

first,box9=geometries(args.row_9)
second,box10=geometries(args.row_10)
# Equal pitch at opposite horizontal yaw:22.5↔337.5,...157.5↔202.5.
pairs=[(i,8-i) for i in range(1,8)]
ratios=[(box9[i][3]-box9[i][1])/(box10[j][3]-box10[j][1]) for i,j in pairs]
factor=median(ratios)
if not 0.75<=factor<=1.25:raise SystemExit(f'Source scale mismatch requires visual repair, factor={factor}')
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
new_size=(round(second.width*factor),round(second.height*factor))
second.resize(new_size,Image.Resampling.NEAREST).save(out)
report={'ok':True,'method':'single uniform complete-source scale from median matched-pitch opposite-yaw heights','row9':args.row_9,'row10':args.row_10,'output':str(out),'source_size':list(second.size),'output_size':list(new_size),'shared_source_scale_factor':factor,'pairs':[{'row9_index':i,'row10_index':j,'height_ratio':ratio} for (i,j),ratio in zip(pairs,ratios)],'row9_boxes':box9,'row10_boxes':box10,'pixels_redrawn':False}
Path(args.json_out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'ok':True,'factor':factor,'output':str(out)}))
