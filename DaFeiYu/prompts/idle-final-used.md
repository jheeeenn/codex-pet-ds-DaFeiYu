Create one horizontal animation strip for ChatGPT pet `大肥鱼`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure green #00FF00. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: Preserve current pixel-art maid character and all existing outfit, indigo hair, pale-blue rectangular eyes, frilled headband and blue-white apron. Add physically attached BLUE WHALE TAIL emerging from lower back behind skirt; curved thick tapering blue stem, pale underside, a few light-blue spots, and broad two-lobed whale flukes. Tail curves out beside legs and stays compact, does not replace legs. New three-view reference defines tail anatomy ONLY; do not adopt sweater, beanie, handbag or winter outfit. Tail sways gently and follows the existing body action. No text, arrows, marks, or extra props.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `pixel`: Pixel-art-adjacent digital mascot with a chunky silhouette, simple dark outline, limited palette, flat cel shading, and visible stepped edges.
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Calm low-distraction resting loop: subtle breathing, tiny blink, slight head/body bob, and only quiet persona-preserving motion.

State requirements:
- CRITICAL: idle is the low-distraction baseline state and the first frame is also used as the reduced-motion static pet.
- Use only subtle idle motion: gentle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet motion that fits the pet persona.
- Keep the pet essentially in the same pose, facing direction, silhouette, markings, palette, and prop state across all 6 frames.
- Idle variation must stay calm but still read as animation; do not repeat effectively identical copies across the loop.
- Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- Feet, base, body, or object anchor should remain planted or nearly planted.
- The first and last frames should be very close visually so the loop feels calm and does not pop.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.


EDIT TARGET AND INVARIANTS: Image1 is the existing approved SIX-frame idle strip. Preserve those exact six maid body poses, same face, hair, original frilled blue-white apron dress, body proportions, blink timing (open/open/half/closed/reopen/open), breathing and planted feet. Change only adding the animated blue whale tail and changing yellow backdrop to perfectly flat GREEN #00FF00. Image2 is approved tail anatomy and pixel construction. Image3 is original identity + three-view TAIL ANATOMY ONLY; never adopt sweater, hat, handbag, plaid skirt or winter clothes. Image4 is layout only, no copied lines.

Each tail emerges from lower back BEHIND the existing skirt, continuously attached and visibly overlapping the skirt edge. It curves beside the legs toward SCREEN-RIGHT with a thick tapering blue stem, pale underside, a few pale-blue spots, and TWO broad whale flukes. It does not replace legs. Show a gentle, low-amplitude six-frame fluke sway (rest, small rise, gentle peak, return, small lower, rest). Keep stem attachment stable. Tail, body and arms must be one connected silhouette. The final frame matches the first. Broaden invisible slots as needed to show six complete bodies AND tails with roomy green gaps and safe outer margins; never clip tail tips. Crisp pixel outlines. No new props, effects, symbols, labels, guide marks, arrows, shadows or text.


CRITICAL SOURCE GEOMETRY: Scale ALL six complete body-plus-tail groups a little smaller to fit roomy 6 slots. Give each body-plus-tail group its own equal slot with at least 12 percent blank green padding to BOTH left and right of the complete group. The FIRST and LAST groups must have especially generous green outer margin. Keep each tail compact and gently curled, no longer than 35 percent of body height. No tail touches neighboring hair and no art touches canvas edges. The two-lobed flukes must be completely visible with a black outline and green margin around the entire tip. Use an ultra-wide 3-to-1 image. Treat all six complete groups identically, never clip the last one.
