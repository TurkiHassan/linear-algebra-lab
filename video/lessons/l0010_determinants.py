#!/usr/bin/env python3
"""0010 · determinants 2x2 to 3x3 — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "DET 0010"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("المحدد: رقم يكشف ثلاثة أسرار"),
           font=F(FDISP, 92), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "نظير؟ استقلال؟ مساحة؟ — الصفر يجيب سلبا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0010")
    return img


def sc_2x2(img, d, t, D):
    ctext(d, 115, "محدد 2×2: اضرب القطر واطرح", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 165, 190, 130, 62, [[2, -3], [1, 2]])
    if t > 1.6:
        latin_lines(d, W // 2, 390, 75, ["|A| = 2(2) - 1(-3) = 7"], 38, t=t, stagger=1.6)
    if t > 2.8:
        verdict(d, W // 2, 520, 480, "غير صفري: نظير واستقلال", True)
    return img


def sc_area(img, d, t, D):
    ctext(d, 110, "والمساحة؟ متوازي أضلاع العمودين", F(FDISP_B, 50))
    if t > 0.5:
        px = grid_axes(d, (390, 170, 890, 470), rng=5, step_px=42)
        u, v = (2, 1), (-1, 3)
        pts = [px((0, 0)), px(u), (px(u)[0] + px(v)[0] - px((0, 0))[0],
                                px(u)[1] + px(v)[1] - px((0, 0))[1]), px(v)]
        d.polygon(pts, fill=(169, 183, 149))
        for p in (u, v):
            vec(d, px, p, INK, width=4, dot=False)
    if t > 2.4:
        draw_mixed(d, W // 2, 570, "المساحة = القيمة المطلقة للمحدد = 7",
                   F(FSANS_M, 36), F(FMONO, 34), ACCENT)
    return img


def sc_sarrus(img, d, t, D):
    ctext(d, 110, "ساروس لـ 3×3: نوازل ناقص صواعد", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 200, 180, 96, 56,
                    [[2, 4, 6], [3, 8, 5], [-1, 1, 2]])
    if t > 2.2:
        latin_lines(d, W // 2, 440, 75, ["down = 30 ,  up = -14"], 36, t=t, stagger=2.2)
    if t > 3.4:
        latin_lines(d, W // 2, 530, 75, ["det = 30 - (-14) = 44"], 40, ACCENT, t=t, stagger=3.4)
    return img


def sc_sing(img, d, t, D):
    ctext(d, 140, "ومحدد الصفر؟", F(FDISP_B, 54))
    if t > 0.7:
        latin_lines(d, W // 2, 280, 95, ["det = 0"], 54, TERRA, t=t, stagger=0.7)
    if t > 1.8:
        draw_mixed(d, W // 2, 420, "بلا نظير + أعمدة مرتبطة + مساحة مسطحة",
                   F(FSANS_M, 36), F(FMONO, 32), TERRA)
    if t > 2.8:
        verdict(d, W // 2, 550, 420, "الدرس 0010 · الصفر حاسم", True)
    return img


SCENES = [
    {"id": "s1", "display": "المحدد: رقم يكشف ثلاثة أسرار.",
     "spoken": "المُحَدِّد: رَقَمٌ واحِدٌ يَكْشِفُ ثَلاثةَ أسْرار: هَلْ يُوجَدُ نَظير؟ وهَلِ الأعْمِدةُ مُسْتَقِلَّة؟ وهَلِ المِساحةُ غَيْرُ مُسَطَّحة؟",
     "draw": sc_title},
    {"id": "s2", "display": "محدد 2×2: سبعة — غير صفري.",
     "spoken": "مُحَدِّدُ اثْنَيْنِ في اثْنَيْن: اضْرِبْ القُطْرَ الرَّئيسيَّ واطْرَحْ حاصِلَ القُطْرِ الآخَر. اثْنان في اثْنَيْن، ناقِص، واحِد في سالِبِ ثَلاثة، يُساوي سَبْعة. غَيْرُ صِفْرِيّ، فَالنَّظيرُ مَوْجودٌ والأعْمِدةُ مُسْتَقِلَّة.",
     "draw": sc_2x2},
    {"id": "s3", "display": "المساحة = القيمة المطلقة للمحدد.",
     "spoken": "وهَنْدَسِيّاً: عَمودا المَصْفوفةِ ضِلْعا مُتَوازي أضْلاع، ومِساحَتُهُ تُساوي القيمَةَ المُطْلَقةَ لِلمُحَدِّد. هُنا سَبْعة.",
     "draw": sc_area},
    {"id": "s4", "display": "ساروس: حواصل النوازل ناقص الصواعد = 44.",
     "spoken": "ولِلرُّتْبَةِ ثَلاثة: قاعِدةُ ساروس. انْسَخْ عَمودَيْن، واجْمَعْ حَواصِلَ الأقْطارِ النّازِلة، ثُمَّ اطْرَحْ حَواصِلَ الأقْطارِ الصّاعِدة. ثَلاثون، ناقِصُ سالِبِ أرْبَعةَ عَشَر، يُساوي أرْبَعةً وأرْبَعين.",
     "draw": sc_sarrus},
    {"id": "s5", "display": "محدد الصفر: لا نظير ولا استقلال ولا مساحة.",
     "spoken": "ومُحَدِّدُ الصِّفْر؟ ثَلاثةُ أحْكامٍ سَلْبِيَّةٍ دَفْعةً واحِدة: بِلا نَظير، وأعْمِدةٌ مُرْتَبِطة، ومِساحةٌ مُسَطَّحة. الدَّرْسُ العاشِر: الصِّفْرُ حاسِم.",
     "draw": sc_sing},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0010-determinants", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0010")
