#!/usr/bin/env python3
"""0029 · backpropagation and automatic differentiation — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "BACKPROP 0029"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الانتشار الخلفي"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "قاعدة السلسلة بترتيب معاكس", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0029")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "الشبكة تركيب دوال", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["y = (f_K o ... o f_1)(x)", "L(theta) = || y - f_K ||^2"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "كيف نحسب dL/dtheta بكفاءة", False)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "بيان الحساب", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["a = x^2 , b = exp(a) , c = a + b", "d = sqrt(c) , e = cos(c) , f = d + e"], 32, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "ست عمليات اولية لا اكثر", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "المرور الخلفي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["start at df/df = 1", "two paths -> two terms, added"], 34, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "من المخرج الى المدخل", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "لماذا خلفا", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["dL/df_(i-1) = (dL/df_i) J_i", "a row times a matrix, not a matrix stored"], 30, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "المخرج عدد، فالخلفي يفوز دائما", True)
    return img


SCENES = [
    {"id": "s1", "display": "الانتشار الخلفي.",
     "spoken": "الانْتِشارُ الخَلْفِيُّ والاشْتِقاقُ التِّلْقائِيّ — قاعِدةُ السِّلْسِلةِ بِتَرْتيبٍ مُعاكِس.",
     "draw": sc_title},
    {"id": "s2", "display": "الشبكة تركيب دوال.",
     "spoken": "الشَّبَكةُ العَصَبِيّةُ لَيْسَتْ شَيْئاً جَديداً رِياضِيّاً: هي تَرْكيبُ دَوالَّ بَعْضُها فَوْقَ بَعْض. والسُّؤالُ العَمَلِيُّ الوَحيد: كَيْفَ نَحْسُبُ مُشْتَقّةَ الخَسارةِ بِكَفاءةٍ عَلى حاسوب؟",
     "draw": sc_two},
    {"id": "s3", "display": "فكك الدالة الى عمليات اولية.",
     "spoken": "فَكِّكِ الدّالّةَ إلى عَمَلِيّاتٍ أوَّلِيّة، عُقْدةً لِكُلِّ مُتَغَيِّرٍ وَسيط، وحافّةً لِكُلِّ اعْتِماد. هذا هو بَيانُ الحِساب.",
     "draw": sc_three},
    {"id": "s4", "display": "امش خلفا مجمعا حاصلات الضرب.",
     "spoken": "ثُمَّ ابْدَأْ مِنَ المَخْرَجِ وامْشِ خَلْفاً مُجَمِّعاً حاصِلاتِ الضَّرْب. والعُقْدةُ الَّتي تُغَذّي عُقْدَتَيْنِ يُجْمَعُ أثَراها — قاعِدةٌ واحِدةٌ إضافِيّةٌ لا أكْثَر.",
     "draw": sc_four},
    {"id": "s5", "display": "لماذا خلفا لا اماما.",
     "spoken": "والسَّبَبُ في اخْتِيارِ الاتِّجاهِ الخَلْفِيّ: المُرورُ الأمامِيُّ يُعْطيكَ أثَرَ مُدْخَلٍ واحِد، والخَلْفِيُّ يُعْطيكَ أثَرَ كُلِّ المَداخِلِ عَلى مَخْرَجٍ واحِد. والخَسارةُ عَدَدٌ واحِدٌ دائِماً. الدَّرْسُ التّاسِعُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0029-backprop", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0029")
