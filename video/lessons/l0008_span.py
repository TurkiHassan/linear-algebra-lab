#!/usr/bin/env python3
"""0008 · span & independence — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "SPN 0008"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("المولد والاستقلال الخطي"),
           font=F(FDISP, 96), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الوصول سؤال — والهدر سؤال آخر", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0008")
    return img


def sc_span(img, d, t, D):
    ctext(d, 115, "المولد: كل ما تصل إليه الخلطة", F(FDISP_B, 50))
    if t > 0.6:
        px = grid_axes(d, (390, 180, 890, 480), rng=5, step_px=42)
        x0, y0 = px((0, 0))
        for gx in range(-5, 6):
            for gy in range(-3, 4):
                x, y = px((gx, gy))
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(160, 190, 175))
    if t > 2.2:
        draw_mixed(d, W // 2, 570, "مولد (1,0) و (0,1) هو R² كله",
                   F(FSANS_M, 36), F(FMONO, 34), ACCENT)
    return img


def sc_det(img, d, t, D):
    ctext(d, 115, "المحدد يحسم الاستقلال لزوج", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 165, 200, 130, 62, [[1, 2], [1, 2]])
    if t > 1.6:
        latin_lines(d, W // 2, 400, 80, ["det = 1(2) - 1(2) = 0"], 38, t=t, stagger=1.6)
    if t > 2.8:
        verdict(d, W // 2, 520, 480, "مرتبطان: متوازيان", False)
    return img


def sc_zero(img, d, t, D):
    ctext(d, 115, "معادلة الصفر هي المحك", F(FDISP_B, 52))
    if t > 0.6:
        latin_lines(d, W // 2, 250, 95,
                    ["2(1,1) - 1(2,2) = (0,0)", "nonzero weights -> dependent"], 38,
                    t=t, stagger=0.6)
    if t > 2.8:
        draw_mixed(d, W // 2, 500, "أوزان غير صفرية تصنع الصفر = ارتباط",
                   F(FSANS_M, 36), F(FMONO, 32), TERRA)
    if t > 3.8:
        verdict(d, W // 2, 600, 420, "هدر: أحدهما زائد", False)
    return img


def sc_poison(img, d, t, D):
    ctext(d, 170, "الصفري يسمم الاستقلال", F(FDISP_B, 54))
    if t > 0.7:
        latin_lines(d, W // 2, 320, 95, ["1·0 + 0·v = 0"], 44, t=t, stagger=0.7)
    if t > 2.0:
        draw_mixed(d, W // 2, 470, "أي مجموعة تحوي الصفري مرتبطة حتما",
                   F(FSANS_M, 36), F(FMONO, 32), TERRA)
    if t > 3.0:
        verdict(d, W // 2, 580, 560, "الدرس 0008 · لا هدر", True)
    return img


SCENES = [
    {"id": "s1", "display": "المولد والاستقلال: الوصول سؤال، والهدر سؤال آخر.",
     "spoken": "المُوَلِّدُ والاسْتِقْلالُ الخَطِّيّ. المُوَلِّدُ سُؤالُ وُصول: إلى أيْنَ تَصِل؟ والاسْتِقْلالُ سُؤالُ هَدَر: هَلْ مِنْ مُتَّجِهٍ زائِد؟",
     "draw": sc_title},
    {"id": "s2", "display": "مولد (1,0) و (0,1) هو R² كله.",
     "spoken": "المُوَلِّدُ هو كُلُّ التَّراكيبِ المُمْكِنة. مُوَلِّدُ واحِدٍ وصِفْر مَعَ صِفْرٍ وواحِدٍ هو المُسْتَوى كُلُّه: أيُّ نُقْطةٍ تَصِلُ إلَيْها بِأوْزانٍ مُناسِبة.",
     "draw": sc_span},
    {"id": "s3", "display": "المحدد صفر: متوازيان، مرتبطان.",
     "spoken": "ولِلزَّوْجِ في المُسْتَوى اخْتِبارٌ فَوْريّ: المُحَدِّد. واحِدٌ وواحِدٌ مَعَ اثْنَيْنِ واثْنَيْن: المُحَدِّدُ يُساوي واحِداً في اثْنَيْن، ناقِصَ واحِدٍ في اثْنَيْن، يُساوي صِفْراً. إذَنِ المُتَّجِهانِ مُتَوازِيان، وهُما مُرْتَبِطان.",
     "draw": sc_det},
    {"id": "s4", "display": "أوزان غير صفرية تصنع الصفر: ارتباط مثبت.",
     "spoken": "والتَّعْريفُ الدَّقيقُ بِمُعادَلةِ الصِّفْر: اثْنان في واحِدٍ وواحِد، ناقِصُ واحِدٍ في اثْنَيْنِ واثْنَيْن، يُساوي الصِّفْر — بِأوْزانٍ غَيْرِ صِفْرِيَّة. إذَنِ الارْتِباطُ مُثْبَت.",
     "draw": sc_zero},
    {"id": "s5", "display": "الصفري يسمم الاستقلال دائماً.",
     "spoken": "وقاعِدةٌ أخيرة: أيُّ مَجْموعةٍ تَحْوي المُتَّجِهَ الصِّفْرِيَّ مُرْتَبِطةٌ حَتْماً — فَوَزْنُهُ واحِد، وبَقِيَّةُ الأوْزانِ أصْفار، فَتَصْنَعُ الصِّفْر. الدَّرْسُ الثّامِن: لا هَدَر.",
     "draw": sc_poison},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0008-span-independence", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0008")
