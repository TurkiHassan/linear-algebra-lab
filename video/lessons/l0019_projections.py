#!/usr/bin/env python3
"""0019 · orthogonal projections & rotations — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "PROJ 0019"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الإسقاط: أقرب نقطة ممكنة"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "ظل المتجه على الفضاء الجزئي", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0019")
    return img


def sc_line(img, d, t, D):
    ctext(d, 130, "الإسقاط على خط", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["<x - pi(x), b> = 0", "lambda = b^T x / |b|^2", "P = b b^T / |b|^2"], 38, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "شرط واحد: أن يكون الفرق عموديا", True)
    return img


def sc_sub(img, d, t, D):
    ctext(d, 130, "الإسقاط على فضاء جزئي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["lambda = (B^T B)^-1 B^T x", "P = B (B^T B)^-1 B^T"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "والنظير الزائف يظهر هنا لأول مرة", True)
    return img


def sc_props(img, d, t, D):
    ctext(d, 110, "خصائص مصفوفة الإسقاط", F(FDISP_B, 50))
    rows = [("P^2 = P", "متحايدة: تكرار الإسقاط لا يغير", True), ("P^T = P", "متماثلة: إسقاط متعامد", True), ("P^-1", "غير موجود: الإسقاط يهدم بعدا", False)]
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


def sc_ls(img, d, t, D):
    ctext(d, 130, "المربعات الصغرى والدوران", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A^T A x = A^T b", "R(t) = [[cos,-sin],[sin,cos]], det = +1"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0019 · ضرب داخلي ثم معيار ثم زاوية ثم إسقاط", True)
    return img


SCENES = [
    {"id": "s1", "display": "الإسقاط: أقرب نقطة ممكنة.",
     "spoken": "الإسْقاط: أقْرَبُ نُقْطةٍ مُمْكِنة — ظِلُّ المُتَّجِهِ على الفَضاءِ الجُزْئِيّ.",
     "draw": sc_title},
    {"id": "s2", "display": "شرط واحد: الفرق عمودي.",
     "spoken": "الإسْقاطُ المُتَعامِدُ على خَطٍّ لَهُ شَرْطٌ واحِدٌ فَقَط: أنْ يَكونَ الفَرْقُ عَمودِيّاً على الخَطّ. ومِنْ هذا الشَّرْطِ وَحْدَهُ تَخْرُجُ كُلُّ الصِّيَغ.",
     "draw": sc_line},
    {"id": "s3", "display": "التعميم على فضاء جزئي بمصفوفة الأساس.",
     "spoken": "وعِنْدَ التَّعْميمِ على فَضاءٍ جُزْئِيٍّ تَصيرُ الصّيغةُ بي في نَظيرِ بي مَنْقولٍ في بي، في بي مَنْقول. والجُزْءُ الأوْسَطُ يُسَمّى النَّظيرَ الزّائِف.",
     "draw": sc_sub},
    {"id": "s4", "display": "مصفوفة الإسقاط متحايدة ومتماثلة، لا معكوسة.",
     "spoken": "ومَصْفوفةُ الإسْقاطِ مُتَحايِدةٌ ومُتَماثِلة: تَكْرارُ الإسْقاطِ لا يُغَيِّرُ شَيْئاً. لكِنَّها لَيْسَتْ قابِلةً لِلْعَكْس، لِأنَّها تَهْدِمُ البُعْدَ المُتَعامِدَ ولا يُمْكِنُ اسْتِرْجاعُه.",
     "draw": sc_props},
    {"id": "s5", "display": "المربعات الصغرى إسقاط، والدوران يحفظ كل شيء.",
     "spoken": "وحينَ لا يوجَدُ حَلٌّ نَطْلُبُ الأقْرَب، فَتَخْرُجُ المُعادَلةُ السَّوِيّة: أساسُ الانْحِدارِ الخَطّيّ. أمّا الدَّوَرانُ فَمَصْفوفةٌ مُتَعامِدةٌ مُحَدِّدُها واحِد، تَحْفَظُ الهَنْدَسةَ كامِلة. الدَّرْسُ التّاسِعَ عَشَر.",
     "draw": sc_ls},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0019-projections-rotations", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0019")
