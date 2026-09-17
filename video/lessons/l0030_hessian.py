#!/usr/bin/env python3
"""0030 · Hessian, linearization and the multivariate Taylor series — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "HESSIAN 0030"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("هسي والانحناء"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الميل رتبة اولى والانحناء ثانية", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0030")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "المشتقة الثانية", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["grad tells the slope", "it says nothing about the bend"], 38, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الميل وحده لا يرى المنعطف", False)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "مصفوفة هسي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["H in R^(n x n)", "H is ALWAYS symmetric"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "والتماثل يستدعي النظرية الطيفية", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "تصنيف الانحناء", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["all eigenvalues > 0  -> minimum", "mixed signs      -> saddle"], 32, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "الاشارات تصنف النقطة", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "التخطيط وخطوة نيوتن", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["f = f(x0) + grad f . delta + 0.5 delta^T H delta", "delta* = - H^-1 (grad f)^T"], 26, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "وثمنها عكس مصفوفة بحجم المعاملات", True)
    return img


SCENES = [
    {"id": "s1", "display": "هسي والتخطيط وتايلور.",
     "spoken": "هِسّي والتَّخْطيطُ ومُتَسَلْسِلةُ تايْلورَ مُتَعَدِّدةِ المُتَغَيِّرات — المَيْلُ رُتْبةٌ أولى والانْحِناءُ ثانِية.",
     "draw": sc_title},
    {"id": "s2", "display": "التدرج لا يرى الانحناء.",
     "spoken": "التَّدَرُّجُ يُخْبِرُكَ بِالمَيْل، ولا يُخْبِرُكَ بِالانْحِناء. والسّائِقُ الَّذي يَعْرِفُ سُرْعَتَهُ ولا يَرى المُنْعَطَفَ لَنْ يُبْطِئَ في وَقْتِه.",
     "draw": sc_two},
    {"id": "s3", "display": "اشتق مرة ثانية.",
     "spoken": "فَاشْتَقَّ مَرّةً ثانِية: لِكُلِّ زَوْجٍ مِنَ المَحاوِرِ مُشْتَقّةٌ ثانِية، وجَمْعُها كُلِّها في مَصْفوفةٍ يُعْطي هِسّي. وهي مُتَماثِلةٌ دائِماً، فَتَنْطَبِقُ عَلَيْها النَّظَرِيّةُ الطَّيْفِيّة.",
     "draw": sc_three},
    {"id": "s4", "display": "الاشارات تصنف النقطة.",
     "spoken": "وإشاراتُ قِيَمِ هِسّي الذّاتِيّةِ تُصَنِّفُ النُّقْطة: كُلُّها موجِبةٌ فَهيَ صُغْرى، وكُلُّها سالِبةٌ فَهيَ عُظْمى، ومُخْتَلِطةٌ فَهيَ نُقْطةُ سَرْج.",
     "draw": sc_four},
    {"id": "s5", "display": "التخطيط والنموذج التربيعي.",
     "spoken": "وأوَّلُ حَدَّيْنِ مِنْ تايْلورَ يُعْطيانِ المُسْتَوى المُماسّ، وإضافةُ الحَدِّ التَّرْبيعِيِّ تُعْطي نَموذَجاً يَرى الانْحِناء — ومِنْهُ تُولَدُ خُطْوةُ نيوتُن. الدَّرْسُ الثَّلاثون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0030-hessian-taylor", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0030")
