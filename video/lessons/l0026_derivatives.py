#!/usr/bin/env python3
"""0026 · derivatives and Taylor series — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "DERIV 0026"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الاشتقاق ومتسلسلة تايلور"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الميل المتوسط يصير لحظيا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0026")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "حاصل الفرق", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["( f(x+h) - f(x) ) / h", "average slope on an interval"], 38, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "متوسط لا لحظة", False)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "المشتقة هي الحد", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["df/dx = lim h->0", "slope of the tangent line"], 40, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "ميل المماس، واتجاه اشد صعود", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "متسلسلة تايلور", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["T_n(x) = SUM f^(k)(x0)/k! (x-x0)^k", "error ~ the first dropped term"], 34, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "الدالة من مشتقاتها عند نقطة", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "القواعد الاربع", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["(f g)' = f' g + f g'", "(g(f(x)))' = g'(f(x)) f'(x)"], 38, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "السلسلة اهمها بفارق كبير", True)
    return img


SCENES = [
    {"id": "s1", "display": "الاشتقاق ومتسلسلة تايلور.",
     "spoken": "الاشْتِقاقُ ومُتَسَلْسِلةُ تايْلور — المَيْلُ المُتَوَسِّطُ يَصيرُ لَحْظِيّاً.",
     "draw": sc_title},
    {"id": "s2", "display": "حاصل الفرق: متوسط الميل.",
     "spoken": "خُذْ نُقْطَتَيْنِ عَلى المُنْحَنى. مَيْلُ الوَتَرِ بَيْنَهُما هو حاصِلُ الفَرْق: مُتَوَسِّطُ التَّغَيُّرِ عَلى الفَتْرةِ كُلِّها، لا عِنْدَ نُقْطةٍ بِعَيْنِها.",
     "draw": sc_two},
    {"id": "s3", "display": "المشتقة حد حاصل الفرق.",
     "spoken": "قَرِّبِ النُّقْطَتَيْنِ حَتّى تَكادا تَلْتَقِيان. الوَتَرُ يَسْتَديرُ حَتّى يَنْطَبِقَ عَلى المُماسّ، وهذا الحَدُّ هو المُشْتَقّة — وهي تُشيرُ إلى اتِّجاهِ أشَدِّ صُعود.",
     "draw": sc_three},
    {"id": "s4", "display": "تايلور: الدالة من مشتقاتها.",
     "spoken": "وإنْ عَرَفْتَ قيمةَ الدّالةِ ومُشْتَقّاتِها عِنْدَ نُقْطةٍ واحِدة، أمْكَنَكَ بِناؤُها حَوْلَها: هذِهِ مُتَسَلْسِلةُ تايْلور. والعامِلِيُّ في المَقامِ هو ما يُطابِقُ المُشْتَقّات.",
     "draw": sc_four},
    {"id": "s5", "display": "اربع قواعد لا اكثر.",
     "spoken": "ولا تَحْفَظْ مُشْتَقّات، بَلِ احْفَظْ أرْبَعَ قَواعِد: الجَمْعَ والضَّرْبَ والقِسْمةَ والسِّلْسِلة. وأهَمُّها السِّلْسِلة، فَعَلَيْها يَقومُ تَدْريبُ كُلِّ شَبَكةٍ عَصَبِيّة. الدَّرْسُ السّادِسُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0026-derivatives-taylor", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0026")
