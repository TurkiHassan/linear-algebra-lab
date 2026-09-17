#!/usr/bin/env python3
"""0016 · norms & inner products — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "NORM 0016"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("المعايير والضرب الداخلي المجرد"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "بديهيات قليلة تصنع هندسة كاملة", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0016")
    return img


def sc_axioms(img, d, t, D):
    ctext(d, 120, "ثلاثة شروط تصنع الطول", F(FDISP_B, 52))
    rows = ["التجانس المطلق: |kx| = |k| |x|", "متباينة المثلث: |x+y| <= |x| + |y|", "التعريف الموجب: |x| = 0 iff x = 0"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "ثلاث مساطر صادقة لمسافة واحدة", F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "ثلاث مساطر شهيرة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["L1 = sum |xi| = 7", "L2 = sqrt(9+16) = 5", "Linf = max |xi| = 4"], 42, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "x = (3, -4) — والترتيب ثابت دائما", True)
    return img


def sc_pd(img, d, t, D):
    ctext(d, 110, "أي مصفوفة تصلح لضرب داخلي؟", F(FDISP_B, 50))
    rows = [("A1 = [[9,6],[6,5]]", "det = 9 > 0: معرفة موجبة", True), ("A2 = [[9,6],[6,3]]", "det = -9 < 0: لا تصلح", False), ("A = I", "الضرب النقطي: حالة خاصة فقط", True)]
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


def sc_cs(img, d, t, D):
    ctext(d, 130, "كوشي — شفارتز", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["|<x,y>| <= |x| |y|", "cos w in [-1, 1]"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0016 · بها صار للزاوية معنى", True)
    return img


SCENES = [
    {"id": "s1", "display": "المعايير والضرب الداخلي المجرد.",
     "spoken": "المَعاييرُ والضَّرْبُ الدّاخِلِيُّ المُجَرَّد: بَديهِيّاتٌ قَليلةٌ تَصْنَعُ هَنْدَسةً كامِلة.",
     "draw": sc_title},
    {"id": "s2", "display": "ثلاثة شروط تصنع الطول.",
     "spoken": "المِعْيارُ دالّةُ طولٍ تُحَقِّقُ ثَلاثةَ شُروط: التَّجانُسَ المُطْلَق، ومُتَبايِنةَ المُثَلَّث، والتَّعْريفَ المُوجِب. ثَلاثةُ شُروطٍ فَقَط، وتَصيرُ عِنْدَكَ مِسْطَرةٌ صادِقة.",
     "draw": sc_axioms},
    {"id": "s3", "display": "L1 سيارة الأجرة، وL2 الطائر، وLinf أطول ضلع.",
     "spoken": "وأشْهَرُ ثَلاثِ مَساطِر: مِعْيارُ مانْهاتَن وهو مَجْموعُ القِيَمِ المُطْلَقة، والإقْليدِيُّ وهو جَذْرُ مَجْموعِ المُرَبَّعات، ومِعْيارُ اللّانِهاية وهو أكْبَرُ مُرَكِّبة.",
     "draw": sc_three},
    {"id": "s4", "display": "الضرب الداخلي يحتاج مصفوفة معرفة موجبة.",
     "spoken": "أمّا الضَّرْبُ الدّاخِلِيّ فَتَعْميمٌ لِلضَّرْبِ النُّقْطِيّ: إكْسْ مَنْقولٌ في أيْ في واي، بِشَرْطِ أنْ تَكونَ أيْ مُتَماثِلةً مُعَرَّفةً مُوجِبة. والضَّرْبُ النُّقْطِيُّ حالةٌ خاصّةٌ فَقَط.",
     "draw": sc_pd},
    {"id": "s5", "display": "كوشي شفارتز تجعل الزاوية معرفة.",
     "spoken": "ثُمَّ تَأْتي مُتَبايِنةُ كوشي شْفارْتْس: القيمةُ المُطْلَقةُ لِلضَّرْبِ الدّاخِلِيِّ لا تَتَجاوَزُ حاصِلَ الطّولَيْن. وهي الَّتي تَحْصُرُ النِّسْبةَ بَيْنَ سالِبِ واحِدٍ وواحِد، فَيَصيرَ لِلزّاوِيةِ مَعْنى. الدَّرْسُ السّادِسَ عَشَر.",
     "draw": sc_cs},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0016-norms-inner-products", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0016")
