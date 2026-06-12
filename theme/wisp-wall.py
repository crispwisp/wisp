#!/usr/bin/env python3
"""Procedural will-o'-the-wisp wallpaper. Pure stdlib -> PPM."""
import math, random, sys

W, H = 1920, 1200
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/wisp.ppm"
TWIN = len(sys.argv) > 3 and sys.argv[3] == "twin"

rng = random.Random(SEED)

# float buffers, additive light model
R = [0.0] * (W * H)
G = [0.0] * (W * H)
B = [0.0] * (W * H)

# ---- base gradient: marsh night air, never pure black ----
top = (0x06 / 255, 0x09 / 255, 0x0f / 255)
bot = (0x0c / 255, 0x15 / 255, 0x19 / 255)
for y in range(H):
    t = y / (H - 1)
    t2 = t * t
    r0 = top[0] + (bot[0] - top[0]) * t2
    g0 = top[1] + (bot[1] - top[1]) * t2
    b0 = top[2] + (bot[2] - top[2]) * t2
    row = y * W
    for x in range(W):
        i = row + x
        R[i] = r0; G[i] = g0; B[i] = b0

# ---- value-noise mist, heavier low, tinted cold sage ----
def noise_grid(gw, gh):
    return [[rng.random() for _ in range(gw + 1)] for _ in range(gh + 1)]

def smooth(t):
    return t * t * (3 - 2 * t)

octaves = [(noise_grid(6, 4), 0.6), (noise_grid(14, 9), 0.3), (noise_grid(30, 19), 0.14)]
for y in range(H):
    fy = y / H
    lowf = 0.25 + 0.95 * (fy ** 2.2)      # mist mass sits low
    row = y * W
    for x in range(W):
        fx = x / W
        v = 0.0
        for grid, amp in octaves:
            gh = len(grid) - 1; gw = len(grid[0]) - 1
            gx = fx * gw; gy = fy * gh
            x0 = int(gx); y0 = int(gy)
            tx = smooth(gx - x0); ty = smooth(gy - y0)
            a = grid[y0][x0] * (1 - tx) + grid[y0][x0 + 1] * tx
            b = grid[y0 + 1][x0] * (1 - tx) + grid[y0 + 1][x0 + 1] * tx
            v += (a * (1 - ty) + b * ty) * amp
        m = v * lowf * 0.085
        i = row + x
        R[i] += m * 0.55; G[i] += m * 0.95; B[i] += m * 1.0

# ---- splat: additive gaussian glow ----
def splat(cx, cy, sigma, amp, col):
    rad = int(sigma * 3.2)
    x0 = max(0, int(cx) - rad); x1 = min(W - 1, int(cx) + rad)
    y0 = max(0, int(cy) - rad); y1 = min(H - 1, int(cy) + rad)
    inv = 1.0 / (2 * sigma * sigma)
    cr, cg, cb = col
    for y in range(y0, y1 + 1):
        dy2 = (y - cy) * (y - cy)
        row = y * W
        for x in range(x0, x1 + 1):
            d2 = (x - cx) * (x - cx) + dy2
            e = amp * math.exp(-d2 * inv)
            if e < 0.0008:
                continue
            i = row + x
            R[i] += e * cr; G[i] += e * cg; B[i] += e * cb

GLOW = (0x8e / 255, 0xf0 / 255, 0xd2 / 255)   # spectral green
CORE = (0.92, 1.0, 0.96)                       # near-white green heart
LAV  = (0xb3 / 255, 0xa6 / 255, 0xf0 / 255)   # lavender shimmer

def wisp_trail(head_x, head_y, length, drift, flip=1.0, brightness=1.0):
    """A drifting light with a fading tail behind it."""
    n = 150
    for k in range(n):
        t = k / (n - 1)                 # 0 = tail, 1 = head
        x = head_x - length * (1 - t)
        wig = math.sin((1 - t) * drift * math.pi * 2) * (1 - t)
        y = head_y + flip * wig * 110 + (1 - t) * (1 - t) * 70 * flip
        fade = t ** 2.6
        sig = 2.0 + 9.0 * t + rng.random() * 0.6
        splat(x, y, sig, 0.028 * fade * brightness, GLOW)
        if k % 11 == 5 and t > 0.15:    # lavender shimmer along the wake
            splat(x, y + rng.uniform(-10, 10), sig * 1.7, 0.006 * fade * brightness, LAV)
    # the head: layered halo -> glow -> core
    splat(head_x, head_y, 64, 0.10 * brightness, GLOW)
    splat(head_x, head_y, 26, 0.42 * brightness, GLOW)
    splat(head_x, head_y, 9,  0.95 * brightness, CORE)
    splat(head_x, head_y, 3.2, 1.0 * brightness, (1.0, 1.0, 1.0))

if TWIN:
    wisp_trail(W * 0.60, H * 0.40, W * 0.42, 1.6, flip=1.0, brightness=1.0)
    wisp_trail(W * 0.36, H * 0.62, W * 0.30, 1.2, flip=-1.0, brightness=0.55)
else:
    wisp_trail(W * 0.62, H * 0.44, W * 0.50, 1.8, flip=1.0, brightness=1.0)

# companion motes drifting in the wake
n_motes = 7 if not TWIN else 10
for _ in range(n_motes):
    mx = rng.uniform(W * 0.18, W * 0.85)
    my = rng.uniform(H * 0.25, H * 0.75)
    s = rng.uniform(2.2, 5.5)
    col = GLOW if rng.random() > 0.3 else LAV
    a = rng.uniform(0.10, 0.30)
    splat(mx, my, s * 3.2, a * 0.18, col)
    splat(mx, my, s, a, col)

# faint stars, upper sky only
for _ in range(150):
    sx = rng.uniform(0, W - 1)
    sy = rng.uniform(0, H * 0.55) * rng.random()
    a = rng.uniform(0.04, 0.22) * (1 - sy / (H * 0.6))
    splat(sx, sy, rng.uniform(0.7, 1.4), a, (0.75, 0.85, 1.0))

# ---- vignette + tone map + write ----
out = bytearray(W * H * 3)
cx, cy = W / 2, H / 2
maxd = math.sqrt(cx * cx + cy * cy)
for y in range(H):
    row = y * W
    dy2 = (y - cy) * (y - cy)
    for x in range(W):
        i = row + x
        d = math.sqrt((x - cx) * (x - cx) + dy2) / maxd
        v = 1.0 - 0.34 * d * d
        for buf, off in ((R, 0), (G, 1), (B, 2)):
            c = buf[i] * v
            c = c / (1.0 + 0.18 * c)          # soft knee, keeps glow from clipping hard
            p = int(255 * min(1.0, max(0.0, c)) ** 0.92)
            out[i * 3 + off] = p

with open(OUT, "wb") as f:
    f.write(b"P6\n%d %d\n255\n" % (W, H))
    f.write(out)
print("wrote", OUT)
