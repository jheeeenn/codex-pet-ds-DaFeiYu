"""Render supplemental motion proof from the exact final encoded Pets atlas."""
from pathlib import Path
import json
import subprocess
import sys
from PIL import Image, ImageDraw
import imageio_ffmpeg

run = Path(sys.argv[1]).resolve()
atlas_path = run / 'final/spritesheet-extended.png'
atlas = Image.open(atlas_path).convert('RGBA')
out = run / 'previews'
out.mkdir(exist_ok=True)
rows = [('idle',[280,110,110,140,140,320]),('running-right',[120]*7+[220]),('running-left',[120]*7+[220]),('waving',[140]*3+[280]),('jumping',[140]*4+[280]),('failed',[140]*7+[240]),('waiting',[150]*5+[260]),('running',[120]*5+[220]),('review',[150]*5+[280])]

def cell(row,col):
    return atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))

def panel(sprite,label,scale=2):
    canvas=Image.new('RGB',(192,232),(227,227,245))
    canvas.paste(sprite,(0,24),sprite)
    ImageDraw.Draw(canvas).text((8,7),label,fill=(37,42,76))
    return canvas.resize((192*scale,232*scale),Image.Resampling.NEAREST)

def gif(images,durations,path):
    images[0].save(path,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=2,optimize=False)

# Persist cropped final-byte cells for bundled per-state preview renderer.
final_frames=run/'final/frames'
all_frames=[];all_durations=[]
for row,(name,durations) in enumerate(rows):
    directory=final_frames/name;directory.mkdir(parents=True,exist_ok=True)
    for col,duration in enumerate(durations):
        sprite=cell(row,col);sprite.save(directory/f'{col:02d}.png')
        all_frames.append(panel(sprite,f'{name}  {col+1}/{len(durations)}'))
        all_durations.append(duration)
gif(all_frames,all_durations,out/'all-states.gif')
transition=[(0,0,400)]+[(4,col,d) for col,d in enumerate(rows[4][1])]+[(0,col,d) for col,d in enumerate(rows[0][1])]
gif([cell(r,c) for r,c,d in transition],[d for r,c,d in transition],out/'idle-jump-idle.gif')
angles=['000','022.5','045','067.5','090','112.5','135','157.5','180','202.5','225','247.5','270','292.5','315','337.5']
gif([panel(cell(9+i//8,i%8),'look '+angle+' deg') for i,angle in enumerate(angles)],[180]*16,out/'look-loop.gif')
proof=[(0,0,'Idle / 0 ms'),(3,1,'Wave / 140 ms'),(4,2,'Jump peak / 280 ms'),(5,4,'Reaction / 560 ms')]
stills=Image.new('RGB',(192*4,232),(227,227,245))
for i,(r,c,label) in enumerate(proof):stills.paste(panel(cell(r,c),label,1),(i*192,0))
stills.save(out/'motion-stills.png')
# Constant-rate MP4 copy, repeating frames according to the GIF timing.
encoder=imageio_ffmpeg.get_ffmpeg_exe()
proc=subprocess.Popen([encoder,'-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','384x464','-r','50','-i','-','-an','-vcodec','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'all-states.mp4')],stdin=subprocess.PIPE)
for frame,duration in zip(all_frames,all_durations):
    for _ in range(max(1,round(duration/20))):proc.stdin.write(frame.tobytes())
proc.stdin.close()
if proc.wait():raise SystemExit('Video encoding failed')
(run/'qa/deliverables.json').write_text(json.dumps({'source':str(atlas_path),'all_state_frames':len(all_frames),'look_frames':16,'outputs':[str(p) for p in sorted(out.iterdir())]},indent=2)+'\n')
print('Rendered all-state GIF and MP4, transition GIF, look GIF, final frame crops, and four labeled stills.')
