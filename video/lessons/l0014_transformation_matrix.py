#!/usr/bin/env python3
"""0014 · transformation matrix & basis change — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "BASIS 0014"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("ثبت الأساس، يصر التطبيق مصفوفة"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "التطبيق أصل ثابت، والمصفوفة وصف نسبي", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0014")
    return img


def sc_coords(img, d, t, D):
    ctext(d, 120, "الإحداثيات: المتجه في لغة أساس", F(FDISP_B, 52))
    rows = ["ثبت أساسا مرتبا B = (b1, ..., bn)", "كل متجه يكتب بطريقة وحيدة", "عمود المعاملات هو [x]_B"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "المتجه واحد، والعناوين بعدد الأسس", F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_build(img, d, t, D):
    ctext(d, 130, "أعمدتها صور متجهات الأساس", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["Phi(e1) = (2,1) -> column 1", "Phi(e2) = (1,-1) -> column 2", "A = [[2,1],[1,-1]]"], 38, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "طبق على الأساس، واكتب الناتج عمودا", True)
    return img


def sc_change(img, d, t, D):
    ctext(d, 130, "وماذا لو بدلت الأساس؟", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A' = T^-1 A S", "one basis: A' = S^-1 A S"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "لا معنى لمصفوفة التطبيق بلا ذكر الأساسين", False)
    return img


def sc_inv(img, d, t, D):
    ctext(d, 130, "ما لا يتغير بتغير الوصف", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["det, trace, rank, dim ker", "invariant under basis change"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0014 · التطبيق واحد والوصف اثنان", True)
    return img


SCENES = [
    {"id": "s1", "display": "ثبت الأساس، يصر التطبيق مصفوفة.",
     "spoken": "ثَبِّتِ الأساس، يَصِرِ التَّطْبيقُ مَصْفوفة. التَّطْبيقُ أصْلٌ ثابِت، والمَصْفوفةُ وَصْفٌ نِسْبِيّ.",
     "draw": sc_title},
    {"id": "s2", "display": "الإحداثيات تتبع الأساس الذي اخترته.",
     "spoken": "ثَبِّتْ أساساً مُرَتَّباً، فَيَصيرَ لِكُلِّ مُتَّجِهٍ تَمْثيلٌ وَحيدٌ بِهِ، وعَمودُ المُعامِلاتِ هو إحْداثِيّاتُه. المُتَّجِهُ واحِد، والعَناوينُ بِعَدَدِ الأُسُس.",
     "draw": sc_coords},
    {"id": "s3", "display": "الأعمدة هي صور متجهات الأساس.",
     "spoken": "وبِناءُ المَصْفوفةِ وَصْفةٌ مِنْ سَطْرٍ واحِد: طَبِّقِ التَّطْبيقَ على كُلِّ مُتَّجِهِ أساس، واكْتُبِ النّاتِجَ عَموداً. هذِهِ هي مَصْفوفةُ التَّحْويل.",
     "draw": sc_build},
    {"id": "s4", "display": "تغيير الأساس: A' = T^-1 A S.",
     "spoken": "فإنْ بَدَّلْتَ الأساسَيْن تَغَيَّرَتِ المَصْفوفةُ بِالصّيغة: نَظيرُ تي في أيْ في إس. ولا مَعْنى لِعِبارةِ مَصْفوفةِ التَّطْبيقِ بِلا ذِكْرِ الأساسَيْن.",
     "draw": sc_change},
    {"id": "s5", "display": "المحدد والرتبة والأثر لا تتغير.",
     "spoken": "لكِنَّ المُحَدِّدَ والرُّتْبةَ والأثَرَ وبُعْدَ النَّواةِ لا تَتَغَيَّر، لِأنَّها صِفاتُ التَّطْبيقِ لا صِفاتُ الجَدْوَل. الدَّرْسُ الرّابِعَ عَشَر.",
     "draw": sc_inv},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0014-transformation-matrix", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0014")
