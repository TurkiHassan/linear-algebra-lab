#!/usr/bin/env python3
"""0018 · orthonormal basis & Gram-Schmidt — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "GS 0018"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("اطرح الإسقاط، يبق العمودي"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "صناعة الأساس المثالي بدل انتظاره", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0018")
    return img


def sc_why(img, d, t, D):
    ctext(d, 120, "لماذا الأساس المتعامد المتجانس أفضل؟", F(FDISP_B, 52))
    rows = ["الإحداثيات بضرب داخلي واحد", "بلا حل منظومة ولا حذف غاوسي", "مصفوفته متعامدة، ونظيرها منقولها"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "قوم الخريطة مرة، واقرأها إلى الأبد", F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_gs(img, d, t, D):
    ctext(d, 130, "غرام — شميت في سطرين", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["u1 = b1", "uk = bk - sum proj(bk on ui)", "ei = ui / |ui|"], 38, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 620, "اطرح الإسقاط، يبق العمودي بالضرورة", True)
    return img


def sc_ex(img, d, t, D):
    ctext(d, 130, "مثال المحاضرة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["b1 = (1,1,0), b2 = (1,0,1)", "u2 = b2 - (1/2) u1 = (0.5,-0.5,1)"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "تحقق: <u1, u2> = 0", True)
    return img


def sc_comp(img, d, t, D):
    ctext(d, 130, "متمم التعامد", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["dim U_perp = D - M", "ker(A) = row(A)_perp"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0018 · وكل متجه ينحل انحلالا وحيدا", True)
    return img


SCENES = [
    {"id": "s1", "display": "اطرح الإسقاط، يبق العمودي.",
     "spoken": "اطْرَحِ الإسْقاط، يَبْقَ العَمودِيّ: صِناعةُ الأساسِ المِثالِيِّ بَدَلَ انْتِظارِه.",
     "draw": sc_title},
    {"id": "s2", "display": "في الأساس المتعامد المتجانس، الإحداثيات ضرب داخلي.",
     "spoken": "لِماذا الأساسُ المُتَعامِدُ المُتَجانِسُ أفْضَل؟ لِأنَّ إحْداثِيّاتِ أيِّ مُتَّجِهٍ تُقْرَأُ بِضَرْبٍ داخِلِيٍّ واحِد، بِلا حَلِّ مَنْظومةٍ ولا حَذْفٍ غاوسِيّ.",
     "draw": sc_why},
    {"id": "s3", "display": "الخوارزمية: فكرة واحدة مكررة.",
     "spoken": "وغْرامْ شْميتْ فِكْرةٌ واحِدةٌ مُكَرَّرة: خُذِ الأوَّلَ كَما هو، ثُمَّ اطْرَحْ مِنْ كُلِّ تالٍ إسْقاطَهُ على ما سَبَق، فَما يَتَبَقّى عَمودِيٌّ بِالضَّرورة. ثُمَّ اقْسِمْ كُلّاً على طولِه.",
     "draw": sc_gs},
    {"id": "s4", "display": "مثال: (1,1,0) و(1,0,1).",
     "spoken": "مِثالُ المُحاضَرة: المُتَّجِهُ الأوَّلُ كَما هو، والثّاني نَطْرَحُ مِنْهُ نِصْفَ الأوَّل، فَنَحْصُلُ على نِصْفٍ وسالِبِ نِصْفٍ وواحِد. وضَرْبُهُما الدّاخِلِيُّ صِفْر: تَعامُدٌ مُؤَكَّد.",
     "draw": sc_ex},
    {"id": "s5", "display": "متمم التعامد والنواة.",
     "spoken": "ومُتَمِّمُ التَّعامُد: كُلُّ ما يَتَعامَدُ مَعَ الفَضاءِ كامِلاً، وبُعْدُهُ الفَرْق. وأجْمَلُ نَتيجة: النَّواةُ هي بِالضَّبْطِ ما يَتَعامَدُ مَعَ كُلِّ صُفوفِ المُصْفوفة. الدَّرْسُ الثّامِنَ عَشَر.",
     "draw": sc_comp},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0018-gram-schmidt", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0018")
