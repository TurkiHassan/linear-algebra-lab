#!/usr/bin/env python3
"""0024 · singular value decomposition — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "SVD 0024"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("تحليل القيم المفردة"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "دوران ثم تمديد ثم دوران", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0024")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "لماذا لا تكفي القطرنة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["EVD needs a square matrix", "and enough eigenvectors"], 38, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "ومصفوفة البيانات ليست مربعة", False)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "التفكيك الذي يعمل دائما", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A = U S V^T", "for EVERY matrix, any shape"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "لا استثناء ولا شرط", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "الخطوات الثلاث", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["V^T : rotate", "S   : stretch", "U   : rotate"], 40, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "تشكيل الطين: وجه، اضغط، وجه", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "من اين تاتي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A^T A = V D V^T", "sigma = sqrt(L),  u = A v / sigma"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0024 · سكين الجيش السويسري", True)
    return img


SCENES = [
    {"id": "s1", "display": "تحليل القيم المفردة.",
     "spoken": "تَحْليلُ القِيَمِ المُفْرَدة — دَوَرانٌ ثُمَّ تَمْديدٌ ثُمَّ دَوَران.",
     "draw": sc_title},
    {"id": "s2", "display": "لماذا لا تكفي القطرنة.",
     "spoken": "القَطْرَنةُ اشْتَرَطَتْ شَرْطَيْن: مَصْفوفةً مُرَبَّعة، ومُتَّجِهاتٍ ذاتِيّةً تَكْفي أساساً. ومَصْفوفةُ البَياناتِ الحَقيقِيّةِ لا تُحَقِّقُ الأوَّلَ أصْلاً.",
     "draw": sc_two},
    {"id": "s3", "display": "التفكيك الذي يعمل لكل مصفوفة.",
     "spoken": "وتَحْليلُ القِيَمِ المُفْرَدةِ يَعْمَلُ لِكُلِّ مَصْفوفةٍ مَهْما كانَ شَكْلُها، بِلا اسْتِثْناءٍ ولا شَرْط. ولِهذا سُمِّيَ سِكّينَ الجَيْشِ السّويسْرِيّ.",
     "draw": sc_three},
    {"id": "s4", "display": "دوران ثم تمديد ثم دوران.",
     "spoken": "والصّورةُ الهَنْدَسِيّةُ بَسيطة: أدِرِ المُدْخَلَ لِتَضْبِطَ مَحاوِرَه، ثُمَّ امْدُدْ كُلَّ مِحْوَرٍ بِقيمَتِهِ المُفْرَدة، ثُمَّ أدِرِ النّاتِجَ إلى مَوْضِعِه.",
     "draw": sc_four},
    {"id": "s5", "display": "من مصفوفة غرام تاتي المصفوفات الثلاث.",
     "spoken": "وأمّا مِنْ أيْنَ تَأْتي المَصْفوفاتُ الثَّلاث؟ مِنْ أي مَنْقول في أي، وهي مُتَماثِلةٌ دائِماً فَتَنْطَبِقُ عَلَيْها النَّظَرِيّةُ الطَّيْفِيّة. الدَّرْسُ الرّابِعُ والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0024-svd", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0024")
