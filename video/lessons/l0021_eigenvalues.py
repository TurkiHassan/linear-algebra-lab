#!/usr/bin/env python3
"""0021 · eigenvalues & eigenvectors — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "EIGEN 0021"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("القيم والمتجهات الذاتية"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "اتجاه لا يدور، ومعامل يمدده", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0021")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "الشرط في سطر واحد", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A x = L x ,  x != 0", "det(A - L I) = 0"], 40, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "اتجاه يخرج على استقامته الاولى", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "الفضاء الذاتي", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["E_L = ker(A - L I)", "A(c x) = c A x = L (c x)"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "المتجهات الذاتية غير وحيدة ابدا", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "هندسة الطيف", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["L = 0  ->  collapse", "complex roots  ->  rotation"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "لكل تحويل بصمة في قيمه الذاتية", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "لماذا يهتم الجميع", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["PageRank = dominant eigenvector", "PCA = eigenvectors of covariance"], 32, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0021 · معادلة واحدة بثلاثة وجوه", True)
    return img


SCENES = [
    {"id": "s1", "display": "القيم والمتجهات الذاتية.",
     "spoken": "القِيَمُ والمُتَّجِهاتُ الذّاتِيّة — اتِّجاهٌ لا يَدور، ومُعامِلٌ يُمَدِّدُه.",
     "draw": sc_title},
    {"id": "s2", "display": "الشرط في سطر واحد.",
     "spoken": "مُعْظَمُ المُتَّجِهاتِ تَدورُ عِنْدَ ضَرْبِها في مَصْفوفة. لكِنَّ بَعْضَ الاتِّجاهاتِ تَصْمُد: يَخْرُجُ المُتَّجِهُ على اسْتِقامَتِهِ الأولى، أطْوَلَ أوْ أقْصَرَ فَحَسْب.",
     "draw": sc_two},
    {"id": "s3", "display": "الفضاء الذاتي نواة.",
     "spoken": "والمُتَّجِهاتُ الذّاتِيّةُ غَيْرُ وَحيدةٍ أبَداً: كُلُّ مُضاعَفٍ غَيْرِ صِفْرِيٍّ ذاتِيٌّ أيْضاً. فَهي تَمْلَأُ فَضاءً جُزْئِيّاً كامِلاً هُوَ نَواةُ أي ناقِص لامْدا آي.",
     "draw": sc_three},
    {"id": "s4", "display": "هندسة الطيف: تمديد وقص ودوران وانهيار.",
     "spoken": "والقِيَمُ الذّاتِيّةُ لَيْسَتْ أرْقاماً مُجَرَّدة: القيمةُ صِفْرٌ تَعْني انْهِياراً، والجُذورُ المُرَكَّبةُ تَعْني دَوَراناً لا يَنْجو مِنْهُ اتِّجاه.",
     "draw": sc_four},
    {"id": "s5", "display": "من ترتيب الصفحات إلى تحليل المكونات.",
     "spoken": "ولِهذا يَهْتَمُّ الجَميع: تَرْتيبُ صَفَحاتِ جوجِل مُتَّجِهٌ ذاتِيّ، وتَحْليلُ المُكَوِّناتِ الرَّئيسةِ يَخْتَصِرُ آلافَ السِّماتِ إلى اتِّجاهاتٍ ذاتِيّة. الدَّرْسُ الحادي والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0021-eigenvalues", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0021")
