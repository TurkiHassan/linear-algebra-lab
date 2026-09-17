#!/usr/bin/env python3
"""0027 · partial derivatives and gradients — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "GRAD 0027"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الاشتقاق الجزئي والتدرج"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "جمد كل المحاور الا واحدا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0027")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "المشتقة الجزئية", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["vary one variable", "freeze all the others"], 40, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "عادت المسالة احادية المتغير", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "التدرج متجه صف", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["grad f = [ df/dx1  ...  df/dxn ]", "in R^(1 x n) , a ROW"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "صف لا عمود، والابعاد تتراص", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "اتجاه اشد صعود", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["theta <- theta - eta (grad f)^T", "walk against the gradient"], 36, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "هبوط التدرج كله في سطر", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "السلسلة على مسار", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["df/dt = SUM (df/dxi)(dxi/dt)", "one term per path"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "مجموع ما يصل عبر كل طريق", True)
    return img


SCENES = [
    {"id": "s1", "display": "الاشتقاق الجزئي والتدرج.",
     "spoken": "الاشْتِقاقُ الجُزْئِيُّ والتَّدَرُّج — جَمِّدْ كُلَّ المَحاوِرِ إلّا واحِداً.",
     "draw": sc_title},
    {"id": "s2", "display": "المشتقة الجزئية: مقبض واحد.",
     "spoken": "نَموذَجُ تَعَلُّمِ الآلةِ دالّةٌ في مَلايينِ الأوْزان. فَما مَعْنى المَيْل؟ اسْأَلْ عَنِ المَيْلِ في اتِّجاهِ مِحْوَرٍ واحِد، وجَمِّدِ الباقي — فَتَعودُ المَسْأَلةُ أُحادِيّةَ المُتَغَيِّر.",
     "draw": sc_two},
    {"id": "s3", "display": "التدرج يجمع الميول.",
     "spoken": "ثُمَّ اجْمَعِ المُشْتَقّاتِ الجُزْئِيّةَ كُلَّها في صَفٍّ واحِد: هذا هو التَّدَرُّج. ولاحِظِ الشَّكْل — مُتَّجِهُ صَفٍّ لا عَمود، وهذا ما يَجْعَلُ الأبْعادَ تَتَراصُّ في قاعِدةِ السِّلْسِلة.",
     "draw": sc_three},
    {"id": "s4", "display": "التدرج بوصلة التدريب.",
     "spoken": "والتَّدَرُّجُ يُشيرُ إلى اتِّجاهِ أشَدِّ صُعود، ومِقْدارُهُ سُرْعةُ ذلِكَ الصُّعود. ولِذلِكَ يُدَرَّبُ كُلُّ نَموذَجٍ بِالسَّيْرِ في الاتِّجاهِ المُعاكِس.",
     "draw": sc_four},
    {"id": "s5", "display": "السلسلة حين تكون المتغيرات دوالا.",
     "spoken": "وإنْ كانَتِ المُتَغَيِّراتُ نَفْسُها دَوالَّ في زَمَن، فَأثَرُ الزَّمَنِ مَجْموعُ ما يَصِلُ عَبْرَ كُلِّ طَريق. الدَّرْسُ السّابِعُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0027-partial-gradients", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0027")
