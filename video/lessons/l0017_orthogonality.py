#!/usr/bin/env python3
"""0017 · angles & orthogonal matrices — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "ORTH 0017"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الزاوية من رقم واحد"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "والمصفوفة التي لا تشوه شيئا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0017")
    return img


def sc_cos(img, d, t, D):
    ctext(d, 130, "تشابه الجيب تمام", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["cos w = <x,y> / (|x| |y|)", "cos = 1 aligned, 0 perp, -1 opposite"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "قسمة على الطولين = تحييد الطول ومقارنة الاتجاه", True)
    return img


def sc_perp(img, d, t, D):
    ctext(d, 110, "متى يتعامدان؟", F(FDISP_B, 50))
    rows = [("<x,y> = 0", "متعامدان: الزاوية قائمة", True), ("|x| = |y| = 1 also", "متعامدان متجانسان", True), ("independent only", "الاستقلال لا يعني التعامد", False)]
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


def sc_pyth(img, d, t, D):
    ctext(d, 130, "فيثاغورس يعود", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["|x+y|^2 = |x|^2 + 2<x,y> + |y|^2", "orthogonal -> middle term = 0"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "التعامد هو ما يجعل الأطوال تجمع تربيعيا", True)
    return img


def sc_mat(img, d, t, D):
    ctext(d, 130, "المصفوفة المتعامدة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A^T A = I", "A^-1 = A^T", "det = +1 rotation, -1 reflection"], 36, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "الدرس 0017 · تحفظ الطول والزاوية معا", True)
    return img


SCENES = [
    {"id": "s1", "display": "الزاوية من رقم واحد.",
     "spoken": "الزّاوِيةُ مِنْ رَقَمٍ واحِد، والمَصْفوفةُ الَّتي لا تُشَوِّهُ شَيْئاً.",
     "draw": sc_title},
    {"id": "s2", "display": "جيب تمام الزاوية = الضرب الداخلي على الطولين.",
     "spoken": "بِفَضْلِ كوشي شْفارْتْس تُوجَدُ زاوِيةٌ وَحيدة: جَيْبُ تَمامِها هو الضَّرْبُ الدّاخِلِيُّ مَقْسوماً على حاصِلِ الطّولَيْن. وهذِهِ نَفْسُها تَشابُهُ الجَيْبِ تَمامِ في نَماذِجِ اللُّغة.",
     "draw": sc_cos},
    {"id": "s3", "display": "التعامد: ضرب داخلي صفر. والتجانس: طول واحد.",
     "spoken": "فإذا كانَ الضَّرْبُ الدّاخِلِيُّ صِفْراً فَهُما مُتَعامِدان، وإذا كانَ طولُ كُلٍّ مِنْهُما واحِداً أيْضاً فَهُما مُتَعامِدانِ مُتَجانِسان. والاسْتِقْلالُ الخَطِّيُّ لا يَعْني التَّعامُد.",
     "draw": sc_perp},
    {"id": "s4", "display": "فيثاغورس يتحقق عند التعامد وحده.",
     "spoken": "وافْرِدْ مُرَبَّعَ طولِ المَجْموع، تَرَ أنَّ فيثاغورْسَ يَتَحَقَّقُ إذا اخْتَفى الحَدُّ الأوْسَط، أيْ إذا تَعامَدَ المُتَّجِهان. التَّعامُدُ لَيْسَ زينةً بَلْ شَرْطُ حِساب.",
     "draw": sc_pyth},
    {"id": "s5", "display": "المصفوفة المتعامدة: نظيرها منقولها.",
     "spoken": "والمَصْفوفةُ المُتَعامِدة: أعْمِدَتُها مُتَعامِدةٌ مُتَجانِسة، فَنَظيرُها مَنْقولُها، وهي تَحْفَظُ الأطْوالَ والزَّوايا مَعاً. مُحَدِّدُها واحِدٌ في الدَّوَران، وسالِبُ واحِدٍ في الانْعِكاس. الدَّرْسُ السّابِعَ عَشَر.",
     "draw": sc_mat},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0017-orthogonality", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0017")
