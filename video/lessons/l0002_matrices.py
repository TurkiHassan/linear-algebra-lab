#!/usr/bin/env python3
"""0002 · matrices, operations & inverse — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "MAT 0002"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("المصفوفة: جدول بعنوان"),
           font=F(FDISP, 100), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الشكل يقرر المسموح والممنوع", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0002")
    return img


def sc_shape(img, d, t, D):
    ctext(d, 115, "الشكل (m × n): صفوف × أعمدة", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 190, 210, 100, 62,
                    [[1, 2, 3], [4, 5, 6]])
    if t > 1.6:
        ctext(d, 470, "صفان وثلاثة أعمدة — الشكل (2×3)", F(FSANS_M, 36))
    if t > 2.6:
        verdict(d, W // 2, 580, 620, "الجمع يحتاج نفس الشكل تماما", True)
    return img


def sc_mul(img, d, t, D):
    ctext(d, 130, "الضرب يحتاج تطابق الوسط", F(FDISP_B, 52))
    if t > 0.6:
        latin_lines(d, W // 2, 280, 100, ["[2x3] . [3x4]  ->  [2x4]"], 44, t=t, stagger=0.6)
    if t > 1.8:
        verdict(d, W // 2, 430, 560, "الأعمدة الأولى = صفوف الثانية", True)
    if t > 3.0:
        latin_lines(d, W // 2, 540, 90, ["[2x3] . [2x3]  =  forbidden"], 40, TERRA, t=t, stagger=3.0)
    return img


def sc_det(img, d, t, D):
    ctext(d, 115, "المحدد يقرر: نظير أم شاذة؟", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 165, 200, 130, 66, [[2, -3], [1, 2]])
    if t > 1.6:
        latin_lines(d, W // 2, 400, 80, ["det = 2(2) - 1(-3) = 7"], 38, t=t, stagger=1.6)
    if t > 2.8:
        verdict(d, W // 2, 520, 420, "غير صفري: النظير موجود", True)
    return img


def sc_inv(img, d, t, D):
    ctext(d, 115, "اقلب القطر واقسم على المحدد", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 165, 190, 130, 62, [[2, -1], [3, 2]])
    if t > 1.8:
        draw_mixed(d, W // 2, 420, "النظير = القطر المقلوب ÷ 7",
                   F(FSANS_M, 36), F(FMONO, 34), ACCENT)
    if t > 3.0:
        draw_matrix(d, W // 2 - 165, 470, 130, 58, [["2/7", "1/7"], ["-3/7", "2/7"]])
    return img


def sc_sing(img, d, t, D):
    ctext(d, 115, "وماذا عن هذه؟", F(FDISP_B, 52))
    if t > 0.6:
        draw_matrix(d, W // 2 - 165, 200, 130, 66, [[2, 1], [4, 2]])
    if t > 1.6:
        latin_lines(d, W // 2, 400, 80, ["det = 2(2) - 4(1) = 0"], 38, t=t, stagger=1.6)
    if t > 2.8:
        verdict(d, W // 2, 520, 460, "شاذة: بلا نظير", False)
    return img


SCENES = [
    {"id": "s1", "display": "المصفوفة: جدول بِعُنْوان. الشكل يُقَرِّر المسموح والممنوع.",
     "spoken": "المَصْفوفةُ جَدْوَلٌ بِعُنْوان. والشَّكْلُ هو الَّذي يُقَرِّرُ المَسْموحَ والمَمْنوع.",
     "draw": sc_title},
    {"id": "s2", "display": "الشكل (2×3): صفان وثلاثة أعمدة. الجمع يحتاج الشكل نفسه.",
     "spoken": "هَذِهِ مَصْفوفةٌ شَكْلُها اثْنان في ثَلاثة: صَفّانِ وثَلاثةُ أعْمِدة. وتَذَكَّرْ: الجَمْعُ يَحْتاجُ الشَّكْلَ نَفْسَهُ تَماماً.",
     "draw": sc_shape},
    {"id": "s3", "display": "الضرب يحتاج تطابق الوسط: أعمدة الأولى = صفوف الثانية.",
     "spoken": "أمّا الضَّرْبُ فَيَحْتاجُ تَطابُقَ الوَسَط: عَدَدُ أعْمِدةِ الأولى يُساوي عَدَدَ صُفوفِ الثّانِية. مَصْفوفةُ اثْنَيْن في ثَلاثة، مَضْروبةً في مَصْفوفةِ ثَلاثةٍ في أرْبَعة، تُعْطي مَصْفوفةَ اثْنَيْنِ في أرْبَعة. ولَوِ اخْتَلَفَ الوَسَط، فَالضَّرْبُ مَمْنوع.",
     "draw": sc_mul},
    {"id": "s4", "display": "المحدد = 7: غير صفري، فالنظير موجود.",
     "spoken": "المُحَدِّد؟ اضْرِبْ القُطْرَ الرَّئيسيَّ واطْرَحْ حاصِلَ القُطْرِ الآخَر: اثْنان في اثْنَيْن، ناقِص، واحِد في سالِبِ ثَلاثة، يُساوي سَبْعة. المُحَدِّدُ غَيْرُ صِفْرِيّ، فَالنَّظيرُ مَوْجود.",
     "draw": sc_det},
    {"id": "s5", "display": "النظير: اقلب القطر، اعكس إشارة الآخر، واقسم على 7.",
     "spoken": "لِلْحُصولِ على النَّظير: اقْلِبْ القُطْرَ الرَّئيسيَّ، واعْكِسْ إشارةَ القُطْرِ الآخَر، ثُمَّ اقْسِمْ كُلَّ خَلِيَّةٍ على المُحَدِّدِ سَبْعة.",
     "draw": sc_inv},
    {"id": "s6", "display": "المحدد صفر: شاذة، بلا نظير.",
     "spoken": "وماذا عَنْ هَذِهِ المَصْفوفة؟ مُحَدِّدُها صِفْر: اثْنان في اثْنَيْن، ناقِصُ أرْبَعة في واحِد. إذَنْ هِيَ شاذَّة، ولا نَظيرَ لَها.",
     "draw": sc_sing},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0002-matrices-inverse", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0002")
