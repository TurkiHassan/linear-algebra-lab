#!/usr/bin/env python3
"""0025 · low-rank approximation — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "RANK 0025"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("التقريب منخفض الرتبة"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "احتفظ بالاكبر، والخطا محسوب سلفا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0025")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "المصفوفة طبقات", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A = sum sigma_i u_i v_i^T", "rank(u v^T) = 1"], 38, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "كومة طبقات مرتبة بالاهمية", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "القطع عند k", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A(k) = sum_{i=1..k} sigma_i u_i v_i^T", "storage: k(m + n + 1)  not  m n"], 30, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "احفظ الطبقات لا الناتج", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "مبرهنة ايكارت ويونغ", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["||A - A(k)||_2 = sigma_(k+1)", "and nothing of rank k does better"], 32, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "ليس تقريبا جيدا بل الافضل", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "اين تظهر", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["image compression", "recommender systems", "low-rank weights in deep nets"], 34, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "الدرس 0025 · الضغط مبرهنة لا حيلة", True)
    return img


SCENES = [
    {"id": "s1", "display": "التقريب منخفض الرتبة.",
     "spoken": "التَّقْريبُ مُنْخَفِضُ الرُّتْبة — احْتَفِظْ بِالأكْبَر، والخَطَأُ مَحْسوبٌ سَلَفاً.",
     "draw": sc_title},
    {"id": "s2", "display": "المصفوفة كومة طبقات.",
     "spoken": "أعِدْ قِراءةَ التَّحْليلِ بِطَريقةٍ أُخْرى: بَدَلَ ضَرْبِ ثَلاثِ مَصْفوفات، اجْمَعْ طَبَقات. وكُلُّ طَبَقةٍ رُتْبَتُها واحِدٌ بِالضَّبْط.",
     "draw": sc_two},
    {"id": "s3", "display": "القطع عند k والتخزين.",
     "spoken": "فَإنِ اكْتَفَيْتَ بِأوَّلِ كاف طَبَقة، صارَ التَّخْزينُ كافاً في مَجْموعِ الأبْعادِ زائِدَ واحِد، بَدَلَ حاصِلِ ضَرْبِهِما. والتَّوْفيرُ في حِفْظِ الطَّبَقاتِ لا النّاتِج.",
     "draw": sc_three},
    {"id": "s4", "display": "ايكارت ويونغ تعطي الخطا بالضبط.",
     "spoken": "ومُبْرَهَنةُ إيكارْت ويونْغ لا تَقولُ إنَّ الخَطَأَ صَغيرٌ فَحَسْب، بَلْ تُعْطيهِ بِالضَّبْط: هُوَ القيمةُ المُفْرَدةُ التّالِيةُ مُباشَرةً بَعْدَ القَطْع.",
     "draw": sc_four},
    {"id": "s5", "display": "من ضغط الصور إلى الشبكات العميقة.",
     "spoken": "ومِنْ هُنا جاءَ ضَغْطُ الصُّوَر، وأنْظِمةُ التَّوْصِية، وتَحْليلُ المَعْنى الكامِن. بَلْ إنَّ أوْزانَ الشَّبَكاتِ العَميقةِ تُظْهِرُ رُتْبةً فَعّالةً مُنْخَفِضة. الدَّرْسُ الخامِسُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0025-low-rank", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0025")
