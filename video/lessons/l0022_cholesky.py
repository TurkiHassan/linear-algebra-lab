#!/usr/bin/env python3
"""0022 · LU & Cholesky decomposition — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "CHOL 0022"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("تحليل LU وتشوليسكي"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الحذف محفوظا، وجذر للمصفوفة", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0022")
    return img


def sc_two(img, d, t, D):
    ctext(d, 130, "الحذف مكتوبا كضرب", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["E_k ... E_1 A = U", "A = L U"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "U هي النتيجة و L هي الطريق اليها", True)
    return img


def sc_three(img, d, t, D):
    ctext(d, 130, "لماذا يفيد", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["L y = b   then   U x = y", "factor once, solve many times"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "التحليل مرة والاستعمال مرات", True)
    return img


def sc_four(img, d, t, D):
    ctext(d, 130, "تشوليسكي: جذر المصفوفة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["A = L L^T", "l11 = sqrt(a11),  l21 = a21 / l11"], 36, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "للمتماثلة المعرفة الموجبة وحدها", True)
    return img


def sc_five(img, d, t, D):
    ctext(d, 130, "فخ القطر الموجب", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["[[1,3],[3,1]]:  det = -8", "positive diagonal is NOT enough"], 34, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0022 · الشرط لازم لا كاف", False)
    return img


SCENES = [
    {"id": "s1", "display": "تحليل LU وتشوليسكي.",
     "spoken": "تَحْليلُ إل يو وتْشوليسْكي — الحَذْفُ مَحْفوظاً، وجَذْرٌ لِلْمَصْفوفة.",
     "draw": sc_title},
    {"id": "s2", "display": "الحذف الغاوسي مكتوبا كضرب.",
     "spoken": "كُلُّ خُطْوةِ حَذْفٍ هي ضَرْبٌ في مَصْفوفةٍ مُثَلَّثِيّةٍ سُفْلى. فَإنْ جَمَعْتَها كُلَّها خَرَجَ لَكَ أي يُساوي إل في يو.",
     "draw": sc_two},
    {"id": "s3", "display": "التحليل مرة والاستعمال مرات.",
     "spoken": "والفائِدةُ عَمَلِيّة: لِحَلِّ المَنْظومةِ بِعِدّةِ قِيَم، تُحَلِّلُ مَرّةً واحِدة، ثُمَّ تَحُلُّ مَسْألَتَيْنِ مُثَلَّثِيَّتَيْنِ لِكُلِّ قيمة.",
     "draw": sc_three},
    {"id": "s4", "display": "تشوليسكي جذر تربيعي للمصفوفة.",
     "spoken": "وتْشوليسْكي جَذْرٌ تَرْبيعِيٌّ لِلْمَصْفوفة: أي يُساوي إل في إل مَنْقول. وهُوَ وَحيدٌ لِلْمَصْفوفةِ المُتَماثِلةِ المُعَرَّفةِ الموجِبة.",
     "draw": sc_four},
    {"id": "s5", "display": "القطر الموجب شرط لازم لا كاف.",
     "spoken": "واحْذَرِ الفَخّ: القُطْرُ الموجِبُ شَرْطٌ لازِمٌ لا كافٍ. مَصْفوفةٌ قُطْرُها موجِبٌ ومُحَدِّدُها سالِبٌ لا تْشوليسْكي لَها. الدَّرْسُ الثّاني والعِشْرون.",
     "draw": sc_five},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0022-cholesky", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0022")
