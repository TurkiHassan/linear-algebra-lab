#!/usr/bin/env python3
"""0020 · trace & characteristic polynomial — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "TRACE 0020"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الأثر والكثيرة المميزة"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "رقمان لا يمسهما تغيير الأساس", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0020")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "الأثر: مجموع القطر", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["tr(A) = a11 + a22 + ... + ann", "tr(A + B) = tr(A) + tr(B)"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "تعريف ساذج يحمل خاصية عميقة", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "دورة الضرب لا تغير الأثر", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["tr(AB) = tr(BA)", "tr(S^-1 A S) = tr(A S S^-1) = tr(A)"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الأثر صفة التطبيق لا صفة تمثيله", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "الكثيرة المميزة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["p(L) = det(A - L I)", "2x2:  p(L) = L^2 - tr(A) L + det(A)"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "رقمان يبنيان الكثيرة كاملة", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "الجذور تعيد الرقمين", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["sum of roots = tr(A)", "product of roots = det(A)"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0020 · الجسر إلى القيم الذاتية", True)
    return img


SCENES = [
    {"id": "s1", "display": "الأثر والكثيرة المميزة.",
     "spoken": "الأثَرُ والكَثيرةُ المُمَيِّزة — رَقْمانِ لا يَمَسُّهُما تَغْييرُ الأساس.",
     "draw": sc_title},
    {"id": "s2", "display": "الأثر مجموع القطر.",
     "spoken": "الأثَرُ مَجْموعُ القُطْرِ ولا شَيْءَ غَيْرُه. تَعْريفٌ يَبْدو ساذِجاً، لكِنَّهُ يَحْمِلُ خاصِّيّةً تَجْعَلُهُ مِنْ أهَمِّ أرْقامِ المَصْفوفة.",
     "draw": sc_two},
    {"id": "s3", "display": "دورة الضرب لا تغير الأثر.",
     "spoken": "الأثَرُ يَحْتَرِمُ دَوْرةَ الضَّرْب: أثَرُ أي بي يُساوي أثَرَ بي أي دائِماً. ومِنْ هذِهِ القاعِدةِ وَحْدَها يَتْبَعُ أنَّ الأثَرَ لا يَتَغَيَّرُ بِتَغْييرِ الأساس.",
     "draw": sc_three},
    {"id": "s4", "display": "الكثيرة المميزة جذورها القيم الذاتية.",
     "spoken": "والكَثيرةُ المُمَيِّزةُ هي مُحَدِّدُ أي ناقِص لامْدا في مَصْفوفةِ الوَحْدة. ولِلْمَصْفوفةِ اثْنَيْنِ في اثْنَيْنِ تَخْتَصِرُ إلى سَطْرٍ واحِدٍ يَسْتَحِقُّ الحِفْظ.",
     "draw": sc_four},
    {"id": "s5", "display": "مجموع الجذور أثر وحاصل ضربها محدد.",
     "spoken": "وجُذورُها تُعيدُ الرَّقْمَيْن: مَجْموعُ الجُذورِ هُوَ الأثَر، وحاصِلُ ضَرْبِها هُوَ المُحَدِّد. الدَّرْسُ العِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0020-trace-characteristic", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0020")
