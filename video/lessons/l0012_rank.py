#!/usr/bin/env python3
"""0012 · rank & solvability — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "RANK 0012"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الرتبة: كم عمودا مختلفا حقا؟"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "رقم واحد يعد الاستقلال، ويحسم وجود الحل", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0012")
    return img


def sc_def(img, d, t, D):
    ctext(d, 120, "ثلاث طرق للعد، ورقم واحد", F(FDISP_B, 52))
    rows = ["عدد الأعمدة المستقلة خطيا", "عدد الصفوف المستقلة — العدد نفسه", "عدد القادة في الصورة الدرجية"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "احذف غاوسيا ثم عد القادة: هذه هي rk(A)", F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_cases(img, d, t, D):
    ctext(d, 110, "محكمة الحلول الثلاث", F(FDISP_B, 50))
    rows = [("rk(A) = rk(A|b) = n", "حل وحيد: لا متغير حر", True), ("rk(A) = rk(A|b) < n", "حلول لانهائية: يوجد متغير حر", True), ("rk(A) < rk(A|b)", "لا حل: ظهر صف 0 = b", False)]
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


def sc_null(img, d, t, D):
    ctext(d, 130, "وبعد فضاء الحل؟", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["dim ker(A) = n - rk(A)", "rk = 2, n = 3 -> free = 1"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الرتبة تقيد، والباقي حر", True)
    return img


def sc_full(img, d, t, D):
    ctext(d, 130, "الرتبة التامة والمصفوفة المربعة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["rk(A) = n", "det(A) != 0", "A inverse exists"], 42, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "الدرس 0012 · ثلاثة أوجه لحقيقة واحدة", True)
    return img


SCENES = [
    {"id": "s1", "display": "الرتبة: كم عمودا مختلفا حقا؟",
     "spoken": "الرُّتْبة: كَمْ عَموداً مُخْتَلِفاً حَقّاً؟ رَقَمٌ واحِدٌ يَعُدُّ الاسْتِقْلال، ويَحْسِمُ وُجودَ الحَلّ.",
     "draw": sc_title},
    {"id": "s2", "display": "الرتبة = عدد القادة = عدد الأعمدة المستقلة.",
     "spoken": "ثَلاثُ طُرُقٍ لِلْعَدِّ ورَقَمٌ واحِدٌ يَخْرُجُ مِنْها: عَدَدُ الأعْمِدةِ المُسْتَقِلّة، وعَدَدُ الصُّفوفِ المُسْتَقِلّة، وعَدَدُ القادةِ في الصّورةِ الدَّرَجِيّة. احْذِفْ غاوسِيّاً ثُمَّ عُدَّ القادة.",
     "draw": sc_def},
    {"id": "s3", "display": "قارن rk(A) مع rk(A|b) ومع n.",
     "spoken": "ثُمَّ قارِنْ رُتْبَتَيْن: إذا تَساوَتا وبَلَغَتا عَدَدَ المَجاهيلِ فالحَلُّ وَحيد، وإذا تَساوَتا ونَقَصَتا فالحُلولُ لانِهائِيّة، وإذا اخْتَلَفَتا فلا حَلَّ أصْلاً.",
     "draw": sc_cases},
    {"id": "s4", "display": "بعد فضاء الحل = n ناقص الرتبة.",
     "spoken": "وبُعْدُ فَضاءِ الحَلّ؟ هو عَدَدُ الأعْمِدةِ ناقِصَ الرُّتْبة. كُلُّ قائِدٍ يُقَيِّدُ مُتَغَيِّراً، وما بَقِيَ بِلا قائِدٍ يَبْقى حُرّاً.",
     "draw": sc_null},
    {"id": "s5", "display": "الرتبة التامة تعني نظيرا ومحددا غير صفري.",
     "spoken": "وفي المُصْفوفةِ المُرَبَّعة: الرُّتْبةُ التّامّة، والمُحَدِّدُ غَيْرُ الصِّفْرِيّ، ووُجودُ النَّظير — ثَلاثةُ أوْجُهٍ لِحَقيقةٍ واحِدة. الدَّرْسُ الثّاني عَشَر.",
     "draw": sc_full},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0012-rank", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0012")
