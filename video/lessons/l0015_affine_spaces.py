#!/usr/bin/env python3
"""0015 · affine spaces — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "AFF 0015"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الفضاء الأفيني: فضاء أزيح عن الأصل"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "نقطة إسناد، وفضاء اتجاه", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0015")
    return img


def sc_vs(img, d, t, D):
    ctext(d, 110, "خطي أم أفيني؟", F(FDISP_B, 50))
    rows = [("f(x) = Ax", "خطي: الصفر يذهب إلى الصفر", True), ("f(x) = Ax + b", "أفيني: خطي زائد إزاحة", False), ("f(0) = 0 ?", "هذا هو الاختبار الفاصل كله", True)]
    f = F(FMONO, 32)
    for k, (eq, why, good) in enumerate(rows):
        y = 240 + k * 130
        if t > 0.4 + k * 1.2:
            d.text((W // 2, y), eq, font=f, fill=INK, anchor="mm")
            if good:
                check_mark(d, W // 2 - 340, y, 20, ACCENT)
            else:
                cross_mark(d, W // 2 - 340, y, 18, TERRA)
            draw_mixed(d, W // 2, y + 52, why, F(FSANS, 28), F(FMONO, 26),
                       ACCENT if good else TERRA)
    return img


def sc_form(img, d, t, D):
    ctext(d, 120, "L = x0 + U", F(FDISP_B, 52))
    rows = ["x0: نقطة الإسناد — وليست وحيدة", "U: فضاء الاتجاه — وهو وحيد", "x = x0 + k1 b1 + ... + kk bk"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "البعد يقرره فضاء الاتجاه، لا نقطة الإسناد", F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_sol(img, d, t, D):
    ctext(d, 130, "لماذا حلول Ax = b أفينية؟", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["solution = xp + ker(A)", "b != 0 -> zero is not a solution"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "حل خاص زائد النواة كاملة", True)
    return img


def sc_hyper(img, d, t, D):
    ctext(d, 130, "المستوى الفائق", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["a^T x = c", "dim = n - 1"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0015 · الحد الفاصل في التصنيف", True)
    return img


SCENES = [
    {"id": "s1", "display": "الفضاء الأفيني: فضاء أزيح عن الأصل.",
     "spoken": "الفَضاءُ الأفينِيّ: فَضاءٌ جُزْئِيٌّ أُزيحَ عَنِ الأصْل. نُقْطةُ إسْناد، وفَضاءُ اتِّجاه.",
     "draw": sc_title},
    {"id": "s2", "display": "الفرق إزاحة واحدة: هل f(0) = 0؟",
     "spoken": "الفَرْقُ إزاحةٌ واحِدة: دالّةُ أيْ في إكْس خَطِّيّة، ودالّةُ أيْ في إكْس زائِدَ بي أفينِيّة. واخْتِبارٌ واحِدٌ يَفْصِلُهُما: هَلْ يَذْهَبُ الصِّفْرُ إلى الصِّفْر؟",
     "draw": sc_vs},
    {"id": "s3", "display": "نقطة الإسناد ليست وحيدة. فضاء الاتجاه وحيد.",
     "spoken": "والصّيغةُ العامّة: نُقْطةُ إسْنادٍ زائِدَ فَضاءِ اتِّجاه. نُقْطةُ الإسْنادِ لَيْسَتْ وَحيدة، فأيُّ نُقْطةٍ على الفَضاءِ تَصْلُح. أمّا فَضاءُ الاتِّجاهِ فَوَحيد، وهو الَّذي يُحَدِّدُ البُعْد.",
     "draw": sc_form},
    {"id": "s4", "display": "مجموعة حلول Ax = b أفينية دائما.",
     "spoken": "ولِهذا تَكونُ مَجْموعةُ حُلولِ المَنْظومةِ أفينِيّة: حَلٌّ خاصٌّ واحِدٌ زائِدَ النَّواةِ كامِلة. والصِّفْرُ لَيْسَ حَلّاً، فَلَيْسَتْ فَضاءً جُزْئِيّاً.",
     "draw": sc_sol},
    {"id": "s5", "display": "المستوى الفائق بعده n ناقص واحد.",
     "spoken": "والمُسْتَوى الفائِق: قَيْدٌ واحِدٌ يَخْفِضُ البُعْدَ واحِداً، وهو الحَدُّ الفاصِلُ في خَوارِزْمِيّاتِ التَّصْنيف. الدَّرْسُ الخامِسَ عَشَر.",
     "draw": sc_hyper},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0015-affine-spaces", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0015")
