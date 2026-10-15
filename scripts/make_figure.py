# -*- coding: utf-8 -*-
"""黑白霍尔效应原理图（用文本测量精确定位，不再猜坐标）。"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1400, 1150
img = Image.new("RGB", (W * SS, H * SS), "white")
d = ImageDraw.Draw(img)
BLACK, GRAY = (0, 0, 0), (110, 110, 110)
F_FRONT, F_TOP, F_RIGHT = (250, 250, 250), (236, 236, 236), (214, 214, 214)


def font(sz):
    for nm in ("simhei.ttf", "msyh.ttc", "simsun.ttc", "arial.ttf"):
        p = os.path.join(r"C:\Windows\Fonts", nm)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, int(sz * SS))
            except Exception:
                pass
    return ImageFont.load_default()


FBIG, FSMALL = font(30), font(24)


def line(p1, p2, w=3, color=BLACK):
    d.line([p1[0] * SS, p1[1] * SS, p2[0] * SS, p2[1] * SS], fill=color, width=int(w * SS))


def arrow(p1, p2, w=6, color=BLACK, head=22):
    line(p1, p2, w, color)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for da in (2.7, -2.7):
        line(p2, (p2[0] + head * math.cos(ang + da), p2[1] + head * math.sin(ang + da)), w, color)


def dashed(p1, p2, dash=15, gap=11):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]) or 1
    for i in range(int(L // (dash + gap)) + 1):
        t0 = i * (dash + gap) / L
        t1 = min((i * (dash + gap) + dash) / L, 1.0)
        if t0 >= 1:
            break
        line((p1[0] + (p2[0] - p1[0]) * t0, p1[1] + (p2[1] - p1[1]) * t0),
             (p1[0] + (p2[0] - p1[0]) * t1, p1[1] + (p2[1] - p1[1]) * t1), 3, GRAY)


def text_center(cx, cy, s, f, color=BLACK):
    """把字符串精确居中到 (cx, cy)。"""
    bb = d.textbbox((0, 0), s, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx * SS - w / 2 - bb[0], cy * SS - h / 2 - bb[1]), s, font=f, fill=color)


# ---------------- geometry ----------------
XL, XR = 430, 830
ZB, ZT = 790, 320
DX, DY = 150, -105

# front / top / right faces
d.polygon([(XL * SS, ZB * SS), (XR * SS, ZB * SS), (XR * SS, ZT * SS), (XL * SS, ZT * SS)],
          fill=F_FRONT, outline=BLACK, width=3 * SS)
d.polygon([(XL * SS, ZT * SS), (XR * SS, ZT * SS), ((XR + DX) * SS, (ZT + DY) * SS),
           ((XL + DX) * SS, (ZT + DY) * SS)], fill=F_TOP, outline=BLACK, width=3 * SS)
d.polygon([(XR * SS, ZB * SS), ((XR + DX) * SS, (ZB + DY) * SS),
           ((XR + DX) * SS, (ZT + DY) * SS), (XR * SS, ZT * SS)],
          fill=F_RIGHT, outline=BLACK, width=3 * SS)
dashed((XL, ZB), (XL + DX, ZB + DY))
dashed((XL + DX, ZB + DY), (XR + DX, ZB + DY))
dashed((XL + DX, ZB + DY), (XL + DX, ZT + DY))

# ---------------- I_S : 竖直，中心线 ----------------
XC = (XL + XR) / 2
arrow((XC, ZB + 150), (XC, ZB + 25))
arrow((XC, ZT - 25), (XC, ZT - 150))
text_center(XC - 20, ZB + 95, "I", FBIG)
text_center(XC + 15, ZB + 103, "S", FSMALL)
text_center(XC - 20, ZT - 190, "I", FBIG)
text_center(XC + 15, ZT - 182, "S", FSMALL)

# ---------------- B : 顶面 ⊗ + 箭头（画在薄片右侧，远离文字） ----------------
for i in range(4):
    for j in range(2):
        cx = XL + 95 + i * 90 + j * 45
        cz = ZT + DY + 30 + j * 42
        r = 13
        d.ellipse([(cx - r) * SS, (cz - r) * SS, (cx + r) * SS, (cz + r) * SS],
                  outline=BLACK, width=3 * SS)
        k = r * 0.6
        line((cx - k, cz - k), (cx + k, cz + k), 3)
        line((cx - k, cz + k), (cx + k, cz - k), 3)

# B 箭头：从顶面外侧指向薄片内部（沿 y 方向）
bx0, bz0 = XR + DX + 120, ZT + DY / 2 - 40
arrow((bx0, bz0), (bx0 - DX * 0.55, bz0 - DY * 0.55), 6)
text_center(bx0 + 44, bz0 - 46, "B", FBIG)

# ---------------- U_H : 跨顶边，P/S 在两端 ----------------
Y_TOP = ZT - 230
LXL, RXL = XL + 45, XR - 45
line((LXL, Y_TOP), (LXL, ZT - 12), 5)
line((RXL, Y_TOP), (RXL, ZT - 12), 5)
line((LXL, Y_TOP), (RXL, Y_TOP), 5)
arrow((LXL, Y_TOP), (LXL + 30, Y_TOP), 5)
arrow((RXL, Y_TOP), (RXL - 30, Y_TOP), 5)
text_center(LXL - 34, Y_TOP - 4, "P", FBIG)
text_center(RXL + 34, Y_TOP - 4, "S", FBIG)
text_center((XL + XR) / 2, Y_TOP - 52, "U", FBIG)
text_center((XL + XR) / 2 + 32, Y_TOP - 44, "H", FSMALL)

# ---------------- 尺寸标注 ----------------
text_center((XL + XR) / 2, ZB + 42, "b", FSMALL, GRAY)
text_center(XR + DX + 40, (ZB + ZT) / 2 + DY / 2, "d", FSMALL, GRAY)

img = img.resize((W, H), Image.LANCZOS)
base = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(base, "hall.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes", img.size)
