#!/usr/bin/env python3
"""wisp avatar: a small orb of light adrift in marsh-night air."""
import math

W = H = 512
# channel buffers
acc = [[0.0]*(W*H) for _ in range(3)]

# palette
NIGHT = (10, 15, 20)
GLOW = (142, 240, 210)
SHIMMER = (179, 166, 240)

def splat(cx, cy, sigma, amp, color):
    rad = int(sigma*3)
    x0, x1 = max(0, int(cx)-rad), min(W-1, int(cx)+rad)
    y0, y1 = max(0, int(cy)-rad), min(H-1, int(cy)+rad)
    inv = 1.0/(2*sigma*sigma)
    for y in range(y0, y1+1):
        dy2 = (y-cy)**2
        row = y*W
        for x in range(x0, x1+1):
            e = amp*math.exp(-((x-cx)**2+dy2)*inv)
            if e > 0.0008:
                for c in range(3):
                    acc[c][row+x] += e*color[c]/255.0

# the orb: layered core, slightly above center
cx, cy = 256, 230
splat(cx, cy, 90, 0.45, GLOW)    # outer halo
splat(cx, cy, 42, 0.85, GLOW)    # body
splat(cx, cy, 16, 1.6, (220, 255, 240))  # hot core

# drift trail curling down-left, fading
for k in range(26):
    t = k/25
    x = cx - 60*t - 18*math.sin(t*5.2)
    y = cy + 150*t
    splat(x, y, 22*(1-t)+5, 0.30*(1-t)**1.3, GLOW)

# two shimmer motes
splat(360, 150, 9, 0.7, SHIMMER)
splat(168, 330, 6, 0.5, SHIMMER)
splat(330, 360, 4, 0.45, SHIMMER)

with open("/tmp/wisp_avatar.ppm", "wb") as f:
    f.write(b"P6\n%d %d\n255\n" % (W, H))
    px = bytearray()
    for i in range(W*H):
        for c in range(3):
            v = acc[c][i]
            v = v/(1+v)  # soft clip
            base = NIGHT[c]/255.0
            out = base + (1-base)*v*1.35
            px.append(min(255, max(0, int(out*255))))
    f.write(bytes(px))
print("rendered")
