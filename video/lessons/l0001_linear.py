#!/usr/bin/env python3
"""0001 · which equation is linear — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "LIN 0001"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("أي معادلة خطية؟"),
           font=F(FDISP, 110), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "عشر ثوان تكفي للحكم", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0001")
    return img


def sc_rule(img, d, t, D):
    ctext(d, 120, "القاعدة الذهبية: ثلاثة شروط معا", F(FDISP_B, 52))
    rows = ["الأس 1 لكل متغير", "بلا دوال ملتصقة بالمتغير", "بلا ضرب متغيرين"]
    f = F(FSANS_M, 40)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 100
            d.ellipse([W // 2 - 330, y - 26, W // 2 - 278, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 304, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 36))
    if t > 3.8:
        verdict(d, W // 2, 600, 560, "قوة 1 + بلا دوال + بلا جداء", True)
    return img


def rows_scene(rows, title):
    def draw(img, d, t, D):
        ctext(d, 110, title, F(FDISP_B, 50))
        feq, fwhy = F(FMONO, 36), F(FSANS, 30)
        for k, (eq, why, good) in enumerate(rows):
            y = 245 + k * 135
            if t > 0.4 + k * 1.1:
                a = ease_out((t - 0.4 - k * 1.1) / 0.5)
                yy = y - int(14 * (1 - a))
                bb = d.textbbox((0, 0), eq, font=feq)
                ew = bb[2] - bb[0]
                d.text((W // 2, yy), eq, font=feq, fill=INK, anchor="mm")
                if good:
                    check_mark(d, W // 2 - ew // 2 - 55, yy, 22, ACCENT)
                else:
                    cross_mark(d, W // 2 - ew // 2 - 55, yy, 20, TERRA)
                draw_mixed(d, W // 2, yy + 52, why, fwhy, F(FMONO, 28),
                           ACCENT if good else TERRA)
        return img
    return draw


def sc_end(img, d, t, D):
    ctext(d, 200, "انظر للمتغير وحده", F(FDISP_B, 56))
    if t > 0.6:
        ctext(d, 300, "المعاملات الثابتة مهما بدت غريبة لا تضر", F(FSANS_M, 38), SOFT)
    if t > 1.4:
        verdict(d, W // 2, 440, 620, "الدرس 0001 · تميز الخطي في عشر ثوان", True)
    return img


GOOD_ROWS = [
    ("3x + 2y = 7", "خطية: كل متغير بقوة 1", True),
    ("2y - k = 6", "خطية: k ثابت (مثل جيب π = 0)", True),
    ("(1/2)x + y - 3z = 5", "خطية: الكسور والثوابت لا تضر", True),
]
BAD_ROWS = [
    ("2y - sin x = 6", "ليست خطية: دالة ملتصقة بـ x", False),
    ("x + 2y - xz = 1", "ليست خطية: جداء متغيرين", False),
    ("x + y² = 5", "ليست خطية: الأس 2", False),
]

SCENES = [
    {"id": "s1", "display": "أيُّ مُعادَلةٍ خَطِّيَّة؟ عَشْرُ ثَوانٍ تَكْفي لِلْحُكْم.",
     "spoken": "أيُّ مُعادَلةٍ خَطِّيَّة؟ عَشْرُ ثَوانٍ تَكْفي لِلْحُكْم.",
     "draw": sc_title},
    {"id": "s2", "display": "القاعدة الذهبية: الأس 1، بلا دوال على المتغير، بلا ضرب متغيرين.",
     "spoken": "القاعِدةُ الذَّهَبيَّةُ ثَلاثةُ شُروطٍ مَعاً: الأُسُّ واحِدٌ لِكُلِّ مُتَغَيِّر، وبِلا دَوالَّ مُلْتَصِقةٍ بِالمُتَغَيِّر، وبِلا ضَرْبِ مُتَغَيِّرَيْن.",
     "draw": sc_rule},
    {"id": "s3", "display": "أمثلة خطية: 3x+2y=7، وثابت مثل جَيْب π لا يضر.",
     "spoken": "ثَلاثةُ إكْس زائِدُ اثْنَيْن وايْ يُساوي سَبْعةً: خَطِّيَّة. اثْنان وايْ ناقِصُ ثابِتٍ يُساوي سِتَّةً: خَطِّيَّةٌ أيْضاً، فَالثّابِتُ — مِثْلُ جَيْبِ البايْ — لا يَضُرّ. نِصْفُ إكْس زائِدُ وايْ ناقِصُ ثَلاثةِ زِد يُساوي خَمْسةً: خَطِّيَّة.",
     "draw": rows_scene(GOOD_ROWS, "ثلاث خطيات — احكم قبل أن تكشف")},
    {"id": "s4", "display": "غير خطية: دالة على x، جداء xz، تربيع y.",
     "spoken": "اثْنان وايْ ناقِصُ جَيْبِ إكْس يُساوي سِتَّة: لَيْسَتْ خَطِّيَّة، فَالدّالَّةُ مُلْتَصِقةٌ بِالمُتَغَيِّر. إكْس زائِدُ اثْنَيْن وايْ ناقِصُ إكْس زِد يُساوي واحِداً: لَيْسَتْ خَطِّيَّة، فيها جِداءُ مُتَغَيِّرَيْن. إكْس زائِدُ وايْ مُرَبَّع يُساوي خَمْسة: لَيْسَتْ خَطِّيَّة، فَالأُسُّ اثْنان.",
     "draw": rows_scene(BAD_ROWS, "ثلاث غير خطيات — أين الخلل؟")},
    {"id": "s5", "display": "المعاملات الثابتة لا تضر — انظر للمتغير وحده.",
     "spoken": "تَذَكَّرْ: المُعامِلاتُ الثّابِتة، مَهْما بَدَتْ غَريبةً، لا تَضُرّ — انْظُرْ إلى المُتَغَيِّرِ وَحْدَه. بِهذا تُمَيِّزُ الخَطِّيَّ في عَشْرِ ثَوانٍ.",
     "draw": sc_end},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0001-linear-systems", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0001")
