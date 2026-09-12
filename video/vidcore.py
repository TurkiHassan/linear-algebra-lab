#!/usr/bin/env python3
"""Shared motion-graphics framework for the linear-algebra course videos.

Proven recipe (from gaussian-elimination-ar.mp4):
- 1280x720 @ 24fps, paper/ink/accent/terracotta tokens, .SF Arabic + Monaco.
- Arabic shaped manually (reshaper+bidi) and drawn with PIL BASIC engine
  (raqm would double-shape). Mixed Arabic+Latin goes through draw_mixed(),
  which sets Arabic runs in SFArabic and the rest in Monaco — SFArabic has
  no ASCII digits, so never draw digits with it.
- Narration: ar-SA-HamedNeural via edge-tts, logical order, plain text,
  selective vowelling (see SPOKEN in each lesson script).

Lesson script contract: SCENES = [dict(id, display, spoken, draw)] where
draw(img, d, t, D) paints frame at time t of a D-second scene.
Call build_video(slug, scenes, lesson_tag, head_ar) from __main__.

Subtitles: synth() captures edge-tts WordBoundary events, so the SRT cues
are word-timed to the narration and split into short readable lines.
"""
import hashlib
import json
import math
import os
import subprocess
import sys

W, H, FPS = 1280, 720, 24
# Bump RENDER whenever draw/assembly changes so cached scenes are rebuilt.
RENDER = 3
PAPER = (246, 241, 231)
INK = (28, 26, 21)
SOFT = (111, 103, 87)
ACCENT = (13, 92, 70)
TERRA = (194, 86, 47)
WHITE = (255, 255, 255)

VOICE = "ar-SA-HamedNeural"

from PIL import Image, ImageDraw, ImageFont, ImageFont as _IF  # noqa: E402
_BASIC = _IF.Layout.BASIC

_SF = "/System/Library/Fonts/SFArabic.ttf"
FDISP = _SF
FDISP_B = _SF
FSANS = _SF
FSANS_M = _SF
FSANS_B = _SF
FMONO = "/System/Library/Fonts/Monaco.ttf"

import arabic_reshaper  # noqa: E402
from bidi.algorithm import get_display  # noqa: E402

_RS = arabic_reshaper.ArabicReshaper(configuration={"delete_harakat": False})


def ar(t):
    return get_display(_RS.reshape(t))


def F(path, size):
    return ImageFont.truetype(path, size, layout_engine=_BASIC)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def pop(t):
    t = max(0.0, min(1.0, t))
    return ease_out(t) * (1 + 0.25 * math.sin(t * math.pi))


# ---------- mixed-script text ----------
def _runs_of(visual):
    runs, cur, cura = [], "", None
    for ch in visual:
        o = ord(ch)
        a = (0x0600 <= o <= 0x06FF) or (0xFB50 <= o <= 0xFDFF) or (0xFE70 <= o <= 0xFEFF)
        if cura is None:
            cura = a
        if a == cura:
            cur += ch
        else:
            runs.append((cur, cura))
            cur, cura = ch, a
    if cur:
        runs.append((cur, cura))
    return runs


def _run_w(d, run, font, stroke=0):
    bb = d.textbbox((0, 0), run, font=font, stroke_width=stroke)
    return bb[2] - bb[0]


def mixed_width(d, logical, far, flat, stroke=0):
    return sum(_run_w(d, run, far if a else flat, stroke if a else 0)
               for run, a in _runs_of(ar(logical)))


def draw_mixed(d, cx, y, logical, far, flat, fill=INK, stroke=0, align="center"):
    items = _runs_of(ar(logical))
    ws = [_run_w(d, run, far if a else flat, stroke if a else 0) for run, a in items]
    x = cx - sum(ws) / 2 if align == "center" else cx - sum(ws)
    for (run, a), w in zip(items, ws):
        f = far if a else flat
        if a and stroke:
            d.text((x, y), run, font=f, fill=fill, anchor="lm",
                   stroke_width=stroke, stroke_fill=fill)
        else:
            d.text((x, y), run, font=f, fill=fill, anchor="lm")
        x += w


def ctext(d, y, t, font, fill=INK, size=None):
    draw_mixed(d, W // 2, y, t, font, F(FMONO, getattr(font, "size", 30)), fill)


def chip(d, cx, y, label):
    f = F(FSANS_B, 26)
    w = mixed_width(d, label, f, F(FMONO, 26), stroke=1) + 56
    d.rounded_rectangle([cx - w // 2, y - 28, cx + w // 2, y + 28], radius=28, fill=INK)
    draw_mixed(d, cx, y - 1, label, f, F(FMONO, 26), WHITE, stroke=1)


def chip_raw(d, cx, y, label):
    f = F(FMONO, 25)
    bb = d.textbbox((0, 0), label, font=f)
    w = bb[2] - bb[0] + 78
    d.rounded_rectangle([cx - w // 2, y - 27, cx + w // 2, y + 27], radius=27, fill=INK)
    d.text((cx, y - 1), label, font=f, fill=WHITE, anchor="mm")


def base(tag="GAUSS 0003", head_ar="مختبر الجبر الخطي"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((60, 30), tag, font=F(FMONO, 22), fill=SOFT, anchor="la")
    draw_mixed(d, W - 60, 30, head_ar, F(FSANS, 24), F(FMONO, 22), SOFT, align="right")
    return img, d


def fade(img, p):
    return Image.blend(Image.new("RGB", img.size, PAPER), img, max(0.0, min(1.0, p)))


# ---------- math drawing ----------
def draw_matrix(d, ox, oy, cw, chh, rows, piv=None, circles=(), pop_t=1.0, aug=False):
    n = len(rows[0])
    m = len(rows)
    gw, gh = cw * n + 26, chh * m
    bw = 14
    d.line([(ox, oy), (ox, oy + gh)], fill=INK, width=4)
    d.line([(ox, oy), (ox + bw, oy)], fill=INK, width=4)
    d.line([(ox, oy + gh), (ox + bw, oy + gh)], fill=INK, width=4)
    x1 = ox + gw + bw
    d.line([(x1, oy), (x1, oy + gh)], fill=INK, width=4)
    d.line([(x1 - bw, oy), (x1, oy)], fill=INK, width=4)
    d.line([(x1 - bw, oy + gh), (x1, oy + gh)], fill=INK, width=4)
    if aug:  # divider before the constants column
        divx = ox + bw + cw * (n - 1) + 8
        d.line([(divx, oy + 6), (divx, oy + gh - 6)], fill=INK, width=3)
    fnt = F(FMONO, 34)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cx = ox + bw + 13 + cw * j + cw // 2
            cy = oy + chh * i + chh // 2
            col = ACCENT if piv == (i, j) else INK
            d.text((cx, cy), str(v), font=fnt, fill=col, anchor="mm")
            if (i, j) in circles:
                s = pop(pop_t)
                d.ellipse([cx - cw // 2 + 4, cy - chh // 2 + 3,
                           cx + cw // 2 - 4, cy + chh // 2 - 3],
                          outline=TERRA, width=3)
    return gw + bw * 2


def latin_lines(d, cx, y0, dy, lines, size=40, fill=INK, stagger=0.0, t=99.0):
    f = F(FMONO, size)
    for k, ln in enumerate(lines):
        if t > stagger + k * 0.9:
            a = ease_out((t - stagger - k * 0.9) / 0.5)
            d.text((cx, y0 + k * dy - int(16 * (1 - a))), ln, font=f, fill=fill, anchor="mm")


def check_mark(d, cx, cy, s, color, width=6):
    d.line([(cx - s, cy), (cx - s * 0.25, cy + s * 0.7)], fill=color, width=width)
    d.line([(cx - s * 0.25, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=color, width=width)


def cross_mark(d, cx, cy, s, color, width=6):
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=color, width=width)
    d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=color, width=width)


def verdict(d, cx, y, w, label_ar, good):
    col = ACCENT if good else TERRA
    d.rounded_rectangle([cx - w // 2, y - 30, cx + w // 2, y + 30], radius=30, outline=col, width=3)
    draw_mixed(d, cx, y + 1, label_ar, F(FSANS_B, 30), F(FMONO, 28), col)


def arrow(d, x0, y0, x1, y1, color, width=4):
    d.line([(x0, y0), (x1, y1)], fill=color, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    L = 16
    for da in (2.6, -2.6):
        d.line([(x1, y1), (x1 + L * math.cos(ang + da), y1 + L * math.sin(ang + da))],
               fill=color, width=width)


def grid_axes(d, box, rng=6, step_px=44):
    """Draw grid+axes in box (x0,y0,x1,y1). Returns to_px mapper."""
    x0, y0, x1, y1 = box
    ox, oy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(box, outline=(222, 212, 194), width=2)
    for i in range(-rng, rng + 1):
        c = (222, 212, 194)
        d.line([(ox + i * step_px, y0), (ox + i * step_px, y1)], fill=c, width=1)
        d.line([(x0, oy + i * step_px), (x1, oy + i * step_px)], fill=c, width=1)
    d.line([(x0, oy), (x1, oy)], fill=INK, width=2)
    d.line([(ox, y0), (ox, y1)], fill=INK, width=2)

    def px(p):
        return ox + p[0] * step_px, oy - p[1] * step_px
    return px


def vec(d, px, p, color, width=4, dot=True):
    x0, y0 = px((0, 0))
    x1, y1 = px(p)
    arrow(d, x0, y0, x1, y1, color, width)
    if dot:
        d.ellipse([x1 - 6, y1 - 6, x1 + 6, y1 + 6], fill=color)


# ---------- TTS + assembly ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAIL:", " ".join(cmd), r.stderr[-500:])
        sys.exit(1)
    return r


def probe(mp3):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", mp3],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _synth_async(text, mp3):
    import asyncio
    import unicodedata
    import edge_tts

    async def go():
        c = edge_tts.Communicate(unicodedata.normalize("NFC", text), voice=VOICE,
                                 rate="+0%", volume="+0%", pitch="+0Hz")
        words = []
        with open(mp3, "wb") as fh:
            async for ch in c.stream():
                if ch["type"] == "audio":
                    fh.write(ch["data"])
                elif ch["type"] == "WordBoundary":
                    # offsets are in 100-nanosecond ticks
                    words.append({"t": ch["offset"] / 1e7,
                                  "d": ch["duration"] / 1e7,
                                  "w": ch["text"]})
        return words

    return asyncio.run(go())


def synth(text, mp3):
    """ar-SA-HamedNeural. Returns (duration, word list).

    Words come from edge-tts WordBoundary events, so subtitles can be
    timed to the exact spoken words instead of guessing.
    """
    if os.path.exists(mp3) and os.path.getsize(mp3) > 1000:
        d = probe(mp3)
        if d > 0.5:
            return d, []
    words = []
    for _ in range(2):
        try:
            words = _synth_async(text, mp3)
            d = probe(mp3)
            if d > 0.5:
                return d, words
        except Exception as e:
            print("tts retry:", e)
    raise RuntimeError("edge-tts produced no audio for: " + text[:40])


def ts(s):
    return "%02d:%02d:%02d,%03d" % (int(s // 3600), int((s % 3600) // 60), int(s % 60), int((s % 1) * 1000))


# ---------- subtitles ----------
_SENT_END = ".؟!:؛"


def _split_sentences(words):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"] and w["w"][-1] in _SENT_END:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def _fallback_words(text, dur):
    """Proportional word timing when edge-tts yields no WordBoundary events."""
    tokens = [t for t in text.split() if t]
    if not tokens:
        return []
    total = sum(len(t) + 1 for t in tokens)
    out, t0 = [], 0.0
    for tok in tokens:
        d = dur * (len(tok) + 1) / total
        out.append({"t": t0, "d": d, "w": tok})
        t0 += d
    return out


def wrap_cue(text, width=46, max_lines=2):
    """Wrap an Arabic cue into at most two balanced lines."""
    text = " ".join(text.split())
    if len(text) <= width:
        return [text]
    words = text.split()
    if len(words) < 2:
        return [text]
    best = None
    for k in range(1, len(words)):
        a = " ".join(words[:k])
        b = " ".join(words[k:])
        if max_lines == 2:
            over = max(0, len(a) - width) + max(0, len(b) - width)
            score = over * 1000 + abs(len(a) - len(b))
            if best is None or score < best[0]:
                best = (score, a, b)
    if best is None:
        return [text]
    return [best[1], best[2]]


def subtitle_cues(words, dur, max_chars=46, max_dur=4.2):
    """Group word-timed narration into short, readable subtitle cues."""
    if not words:
        return []
    cues = []
    for g in _split_sentences(words):
        text = " ".join(w["w"] for w in g)
        start = max(0.0, g[0]["t"] - 0.06)
        end = min(dur, g[-1]["t"] + g[-1]["d"] + 0.30)
        if end - start <= max_dur and len(text) <= max_chars:
            cues.append([start, end, text])
            continue
        chunk, cstart = [], start
        for w in g:
            nxt = (len(" ".join(x["w"] for x in chunk)) + 1 + len(w["w"])) if chunk else len(w["w"])
            if chunk and (nxt > max_chars or w["t"] + w["d"] - cstart > max_dur):
                cues.append([cstart, min(dur, chunk[-1]["t"] + chunk[-1]["d"] + 0.25),
                             " ".join(x["w"] for x in chunk)])
                chunk, cstart = [], max(start, w["t"] - 0.04)
            chunk.append(w)
        if chunk:
            cues.append([cstart, min(dur, chunk[-1]["t"] + chunk[-1]["d"] + 0.30),
                         " ".join(x["w"] for x in chunk)])
    merged = []
    for c in cues:
        if merged and c[0] - merged[-1][1] < 0.05 and len(merged[-1][2]) < 22:
            merged[-1][1] = c[1]
            merged[-1][2] += " " + c[2]
        else:
            merged.append(c)
    return merged


def build_video(slug, scenes, outdir, tmpbase, tag="GAUSS 0003",
                head_ar="مختبر الجبر الخطي"):
    """scenes: [{id, display, spoken, draw(img,d,t,D)}]. Writes mp4+srt+poster.

    Reruns are incremental: a scene whose mp3 and mp4 already exist is reused,
    so a failed later scene does not re-render the earlier ones.
    """
    tmp = os.path.join(tmpbase, slug)
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    segs, srt, clock = [], [], 0.0
    for sc in scenes:
        sid = sc["id"]
        spoken = sc.get("spoken", sc["display"])
        mp3 = os.path.join(tmp, sid + ".mp3")
        seg = os.path.join(tmp, sid + ".mp4")
        meta = os.path.join(tmp, sid + ".json")
        h = hashlib.sha1((spoken + "#" + str(RENDER)).encode("utf-8")).hexdigest()
        cached = {}
        if os.path.exists(meta) and os.path.getsize(meta) > 2:
            try:
                cached = json.load(open(meta))
            except ValueError:
                cached = {}
        if cached.get("hash") != h:  # narration changed: drop stale audio/video
            for p in (mp3, seg, meta):
                if os.path.exists(p):
                    os.remove(p)
            cached = {}
        dur, words = synth(spoken, mp3)
        if not words and cached.get("words"):
            words = cached["words"]
        if words and not cached.get("words"):
            json.dump({"hash": h, "words": words}, open(meta, "w"))
        D = dur + 1.4
        if not (os.path.exists(seg) and os.path.getsize(seg) > 1000):
            n = int(D * FPS)
            fr = os.path.join(tmp, sid)
            os.makedirs(fr, exist_ok=True)
            for f in range(n):
                t = f / FPS
                img, d = base(tag, head_ar)
                img = sc["draw"](img, d, t, D)
                if t < 0.4:
                    img = fade(img, t / 0.4)
                if f > n - 8:
                    img = fade(img, (n - f) / 8)
                img.save(os.path.join(fr, "%04d.png" % f))
            # pad the narration to the full scene length so the SRT clock
            # (audio + tail) stays in sync with the concatenated video
            run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i",
                 os.path.join(fr, "%04d.png"), "-i", mp3, "-af", "apad",
                 "-t", "%.3f" % D,
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", seg])
        segs.append(seg)
        cues = subtitle_cues(words or _fallback_words(spoken, dur + 1.4), D)
        if not cues:
            cues = [[0.0, D, sc.get("display", spoken)]]
        last_end = 0.0
        for a, b, tx in cues:
            a, b = clock + a, clock + b
            if a <= last_end:  # never let cues overlap on screen
                a = last_end + 0.01
            if b <= a:
                b = a + 0.6
            last_end = b
            srt.append((a, b, wrap_cue(tx)))
        clock += D
        print("scene %s: %.1fs" % (sid, D), flush=True)
    open(os.path.join(tmp, "list.txt"), "w").write("".join("file '%s'\n" % s for s in segs))
    final = os.path.join(outdir, slug + "-ar.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", os.path.join(tmp, "list.txt"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", final])
    with open(os.path.join(outdir, slug + "-subs.srt"), "w") as f:
        for i, (a, b, tx) in enumerate(srt, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a), ts(b), "\n".join(tx)))
    img, d = base(tag, head_ar)
    pick = scenes[-2] if len(scenes) > 1 else scenes[-1]
    pick["draw"](img, d, 99, 99)
    img.save(os.path.join(outdir, slug + "-poster.png"))
    print("WROTE", final, "total %.1fs" % clock)
    return final
