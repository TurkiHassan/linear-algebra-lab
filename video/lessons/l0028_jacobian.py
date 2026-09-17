#!/usr/bin/env python3
"""0028 · Jacobians and vector-valued gradients — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "JACOB 0028"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("مصفوفة جاكوبي"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "صف لكل مخرج وعمود لكل مدخل", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0028")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "حين يصير المخرج متجها", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["f : R^n -> R^m", "one column per input variable"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "التدرج وحده لا يكفي", False)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "شكل الجاكوبي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["J in R^(m x n)", "J_ij = d f_i / d x_j"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "صف لكل مخرج، عمود لكل مدخل", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "الطبقة الخطية", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["f(x) = A x", "J = A , at every x"], 44, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "التطبيق الخطي هو تخطيطه", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "خسارة المربعات الصغرى", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["dL/de = 2 e^T   (1 x N)", "de/dtheta = - Phi   (N x D)"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الابعاد تتراص فتصح الصيغة", True)
    return img


SCENES = [
    {"id": "s1", "display": "مصفوفة جاكوبي.",
     "spoken": "مَصْفوفةُ جاكوبي — صَفٌّ لِكُلِّ مَخْرَجٍ وعَمودٌ لِكُلِّ مُدْخَل.",
     "draw": sc_title},
    {"id": "s2", "display": "المخرج صار متجها.",
     "spoken": "في الدَّرْسِ السّابِقِ كانَ المَخْرَجُ عَدَداً واحِداً، فَكانَ التَّدَرُّجُ صَفّاً. والآنَ لِيَكُنِ المَخْرَجُ مُتَّجِهاً: كُلُّ مُرَكَّبةٍ تَتَأثَّر، فَالمُشْتَقّةُ بِالنِّسْبةِ لِمُتَغَيِّرٍ واحِدٍ صارَتْ عَموداً.",
     "draw": sc_two},
    {"id": "s3", "display": "اصفف الاعمدة تحصل على جاكوبي.",
     "spoken": "اصْفُفْ هذِهِ الأعْمِدةَ جَنْباً إلى جَنْب، عَموداً لِكُلِّ مُتَغَيِّرٍ مُدْخَل، تَحْصُلْ عَلى الجاكوبي. والعُنْصُرُ فيهِ يُجيبُ سُؤالاً واحِداً: كَمْ يَتَغَيَّرُ هذا المَخْرَجُ إنْ تَحَرَّكَ ذاكَ المُدْخَل؟",
     "draw": sc_three},
    {"id": "s4", "display": "جاكوبي الطبقة الخطية.",
     "spoken": "وجاكوبي التَّطْبيقِ الخَطِّيِّ هو المَصْفوفةُ نَفْسُها، ولا يَعْتَمِدُ عَلى النُّقْطةِ إطْلاقاً — لِأنَّ التَّطْبيقَ الخَطِّيَّ لا يَنْحَني فَتُقَرِّبَه.",
     "draw": sc_four},
    {"id": "s5", "display": "تدرج المربعات الصغرى.",
     "spoken": "وفي خَسارةِ المُرَبَّعاتِ الصُّغْرى: مُشْتَقّةُ الخَسارةِ بِالنِّسْبةِ لِلْبَواقي صَفٌّ، ومُشْتَقّةُ البَواقي بِالنِّسْبةِ لِلْمُعامِلاتِ مَصْفوفة. اضْرِبْهُما يَتَراصَّ البُعْدُ الدّاخِلِيّ. الدَّرْسُ الثّامِنُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0028-jacobian", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0028")
