#!/usr/bin/env python3
"""0023 · diagonalization & the spectral theorem — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "DIAG 0023"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("القطرنة والنظرية الطيفية"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "اساس ذاتي يجعل التحويل تمديدا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0023")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "لماذا نريد القطر", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A = P D P^-1", "A^k = P D^k P^-1"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "ضربتان بدل خمسين ضربة", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "متى تفشل القطرنة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["z <= a  always", "diagonalizable  <=>  sum z = n"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "نقص المتجهات لا تكرار الجذر", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "النظرية الطيفية", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A = A^T   <=>   A = P D P^T", "real values, perpendicular vectors"], 32, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "التماثل يضمن كل شيء", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "اين تظهر", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["covariance is always symmetric", "so PCA axes are always orthogonal"], 32, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0023 · من الطيف إلى المكونات الرئيسة", True)
    return img


SCENES = [
    {"id": "s1", "display": "القطرنة والنظرية الطيفية.",
     "spoken": "القَطْرَنةُ والنَّظَرِيّةُ الطَّيْفِيّة — أساسٌ ذاتِيٌّ يَجْعَلُ التَّحْويلَ تَمْديداً على مَحاوِر.",
     "draw": sc_title},
    {"id": "s2", "display": "القوى تصير قوى اعداد.",
     "spoken": "المَصْفوفةُ القُطْرِيّةُ سَهْلةٌ إلى حَدِّ السَّذاجة: رَفْعُها لِقُوّةٍ هُوَ رَفْعُ كُلِّ عُنْصُرٍ قُطْرِيّ. فَلَوِ اسْتَطَعْنا كِتابةَ أيِّ مَصْفوفةٍ بِهذِهِ الصّورةِ لَوَرِثْنا السُّهولةَ كُلَّها.",
     "draw": sc_two},
    {"id": "s3", "display": "متى تفشل القطرنة.",
     "spoken": "لكِنَّ القَطْرَنةَ تَفْشَل. والسَّبَبُ لَيْسَ تَكْرارَ الجَذْرِ بَلْ نَقْصَ المُتَّجِهاتِ المُسْتَقِلّة: التَّعَدُّدُ الهَنْدَسِيُّ لا يَبْلُغُ الجَبْرِيّ.",
     "draw": sc_three},
    {"id": "s4", "display": "التماثل يضمن اساسا متعامدا.",
     "spoken": "والنَّظَرِيّةُ الطَّيْفِيّةُ تَحْسِمُ الأمْر: المَصْفوفةُ تُقَطْرَنُ قَطْرَنةً مُتَعامِدةً إذا وفَقَطْ إذا كانَتْ مُتَماثِلة. وحينَها تَكونُ قِيَمُها حَقيقِيّةً ومُتَّجِهاتُها مُتَعامِدة.",
     "draw": sc_four},
    {"id": "s5", "display": "مصفوفة التغاير متماثلة دائما.",
     "spoken": "ومَصْفوفةُ التَّغايُرِ في البَياناتِ مُتَماثِلةٌ دائِماً. ولِهذا تُوجَدُ لِتَحْليلِ المُكَوِّناتِ الرَّئيسةِ اتِّجاهاتٌ مُتَعامِدةٌ مُرَتَّبةٌ دائِماً. الدَّرْسُ الثّالِثُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0023-diagonalization", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0023")
