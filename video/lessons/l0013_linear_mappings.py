#!/usr/bin/env python3
"""0013 · linear mappings, kernel & image — motion explainer with Hamed narration."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "MAP 0013"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("التطبيق الخطي: دالة تحترم القواعد"),
           font=F(FDISP, 84), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "ما يهدم إلى الصفر، وما يمكن الوصول إليه", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0013")
    return img


def sc_axioms(img, d, t, D):
    ctext(d, 120, "شرطان يصنعان التطبيق الخطي", F(FDISP_B, 52))
    rows = ["الجمع: Phi(x+y) = Phi(x) + Phi(y)", "القياس: Phi(kx) = k Phi(x)", "ويلزم عنهما حتما: Phi(0) = 0"]
    f = F(FSANS_M, 38)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 105
            d.ellipse([W // 2 - 340, y - 26, W // 2 - 288, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 314, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 34))
    if t > 4.0:
        draw_mixed(d, W // 2, 590, "الصفر لا يذهب للصفر؟ ليس خطيا — وانتهى الفحص", F(FSANS_M, 36), F(FMONO, 32), TERRA)
    return img


def sc_test(img, d, t, D):
    ctext(d, 110, "فاحص الخطية", F(FDISP_B, 50))
    rows = [("Phi(x,y) = (2x+y, x-y)", "خطي: الشرطان يتحققان", True), ("Phi(x,y) = (2x+y+1, x-y)", "أفيني: الصفر لا يذهب للصفر", False), ("Phi(x,y) = (x^2, y)", "التربيع يكسر الضرب القياسي", False)]
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


def sc_kerim(img, d, t, D):
    ctext(d, 130, "النواة والصورة: فضاءان لا مجموعتان", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["ker(A) = {v : Av = 0}", "Im(A) = span of columns"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "النواة تحوي الصفر دائما — ليست فارغة أبدا", True)
    return img


def sc_rn(img, d, t, D):
    ctext(d, 130, "نظرية الرتبة والنواة", F(FDISP_B, 52))
    latin_lines(d, W // 2, 270, 95, ["dim ker + dim Im = dim V", "nullity(A) + rk(A) = n"], 42, t=t, stagger=0.6)
    if t > 2.8:
        verdict(d, W // 2, 590, 620, "الدرس 0013 · لا شيء يضيع في الحساب", True)
    return img


SCENES = [
    {"id": "s1", "display": "التطبيق الخطي: دالة تحترم القواعد.",
     "spoken": "التَّطْبيقُ الخَطّيّ: دالّةٌ تَحْتَرِمُ القَواعِد. ما يُهْدَمُ إلى الصِّفْر، وما يُمْكِنُ الوُصولُ إلَيْه.",
     "draw": sc_title},
    {"id": "s2", "display": "شرطان: الجمع والضرب القياسي. ويلزم Phi(0) = 0.",
     "spoken": "شَرْطانِ يَصْنَعانِ التَّطْبيقَ الخَطّيّ: أنْ يَحْتَرِمَ الجَمْع، وأنْ يَحْتَرِمَ الضَّرْبَ القِياسِيّ. ويَلْزَمُ عَنْهُما حَتْماً أنْ يَذْهَبَ الصِّفْرُ إلى الصِّفْر.",
     "draw": sc_axioms},
    {"id": "s3", "display": "الإزاحة الثابتة والتربيع يكسران الخطية.",
     "spoken": "فَحْصٌ سَريع: التَّطْبيقُ المَصْفوفِيُّ الخالِصُ خَطّيّ، أمّا الَّذي فيهِ إزاحةٌ ثابِتةٌ فأفينِيٌّ لا خَطّيّ، والتَّرْبيعُ يَكْسِرُ الضَّرْبَ القِياسِيَّ فَوْراً.",
     "draw": sc_test},
    {"id": "s4", "display": "النواة: ما ينهار. الصورة: ما يمكن بلوغه.",
     "spoken": "ثُمَّ فَضاءان: النَّواةُ هي كُلُّ ما يُرْسَلُ إلى الصِّفْر، والصّورةُ هي كُلُّ ما يُمْكِنُ الوُصولُ إلَيْه، وهي مُوَلِّدُ أعْمِدةِ المُصْفوفة. والنَّواةُ تَحْوي الصِّفْرَ دائِماً.",
     "draw": sc_kerim},
    {"id": "s5", "display": "ما يهدم وما يبنى مجموعهما ثابت.",
     "spoken": "ونَظَرِيّةُ الرُّتْبةِ والنَّواة: بُعْدُ النَّواةِ زائِدُ بُعْدِ الصّورةِ يُساوي بُعْدَ الفَضاءِ الأصْلِيّ. ما يُهْدَمُ وما يُبْنى مَجْموعُهُما ثابِت. الدَّرْسُ الثّالِثَ عَشَر.",
     "draw": sc_rn},
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "outputs")
    tmp = os.environ.get("COURSEVID_TMP") or os.path.join(tempfile.gettempdir(), "coursevid")
    build_video("0013-linear-mappings", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0013")
