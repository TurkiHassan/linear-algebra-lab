#!/usr/bin/env python3
"""0004 · matrix properties + zero matrix — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "PRP 0004"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("قوانين المصفوفات الستة"),
           font=F(FDISP, 100), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "كل قوانين الأعداد تنتقل — إلا واحدا", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0004")
    return img


def sc_add(img, d, t, D):
    ctext(d, 120, "قوانين الجمع: حرة تماما", F(FDISP_B, 52))
    latin_lines(d, W // 2, 250, 95, ["A + B  =  B + A", "A + (B+C)  =  (A+B) + C"], 42, t=t, stagger=0.5)
    if t > 2.6:
        verdict(d, W // 2, 520, 420, "الإبدال والدمج للجمع", True)
    return img


def sc_scale(img, d, t, D):
    ctext(d, 120, "الضرب القياسي يتوزع ويدمج", F(FDISP_B, 52))
    latin_lines(d, W // 2, 250, 95, ["(cd)A  =  c(dA)", "c(A+B)  =  cA + cB"], 42, t=t, stagger=0.5)
    if t > 2.6:
        verdict(d, W // 2, 520, 460, "التوزيع يعمل كالأعداد", True)
    return img


def sc_ident(img, d, t, D):
    ctext(d, 115, "الوحدة I: الدوار الذي يعيدك", F(FDISP_B, 50))
    if t > 0.6:
        draw_matrix(d, W // 2 - 140, 200, 110, 62, [[1, 0], [0, 1]], piv=None)
    if t > 1.6:
        latin_lines(d, W // 2, 400, 80, ["I A  =  A"], 44, t=t, stagger=1.6)
    if t > 2.6:
        ctext(d, 520, "واحدات على القطر الرئيسي فقط", F(FSANS_M, 34), ACCENT)
    return img


def sc_zero(img, d, t, D):
    ctext(d, 115, "الصفرية O: المحايد الجمعي", F(FDISP_B, 50))
    latin_lines(d, W // 2, 240, 90, ["A + O  =  A", "A + (-A)  =  O"], 42, t=t, stagger=0.5)
    if t > 2.6:
        draw_mixed(d, W // 2, 480, "وإذا cA = O فإما c = 0 أو A صفرية",
                   F(FSANS_M, 36), F(FMONO, 34), TERRA)
    if t > 3.6:
        verdict(d, W // 2, 590, 520, "الصفرية كاشف الشذوذ", True)
    return img


def sc_trap(img, d, t, D):
    ctext(d, 140, "الفخ: إبدال الضرب", F(FDISP_B, 54))
    if t > 0.7:
        latin_lines(d, W // 2, 300, 100, ["A B  !=  B A"], 54, TERRA, t=t, stagger=0.7)
    if t > 2.0:
        verdict(d, W // 2, 500, 560, "الضرب له ترتيب — توقف واسأل", False)
    return img


SCENES = [
    {"id": "s1", "display": "قوانين المصفوفات الستة. كل قوانين الأعداد تنتقل — إلا واحداً.",
     "spoken": "قَوانينُ المَصْفوفاتِ السِّتَّة. كُلُّ قَوانينِ الأعْدادِ تَنْتَقِلُ إلَيْها — إلّا واحِداً.",
     "draw": sc_title},
    {"id": "s2", "display": "الجمع حر: إبدال ودمج بلا قيود.",
     "spoken": "قَوانينُ الجَمْعِ حُرَّةٌ تَماماً: أ زائِدُ ب يُساوي ب زائِدَ أ، والدَّمْجُ يَعْمَلُ كَما في الأعْداد.",
     "draw": sc_add},
    {"id": "s3", "display": "الضرب القياسي: دمج وتوزيع.",
     "spoken": "والضَّرْبُ القِياسيُّ يَنْدَمِجُ ويَتَوَزَّع: سِي دالْ في أ، يُساوي سِي في دالْ أ. وسِي في قَوْسِ أ زائِدِ ب، يُساوي سِي أ زائِدَ سِي ب.",
     "draw": sc_scale},
    {"id": "s4", "display": "الوحدة I: واحدات القطر، و I A = A.",
     "spoken": "مَصْفوفةُ الوَحْدة: واحِداتٌ على القُطْرِ الرَّئيسيِّ فَقَط. آيْ في أ تُساوي أ — إنَّها الدَّوّارُ الَّذي يُعيدُكَ إلى نَفْسِ الشّارِع.",
     "draw": sc_ident},
    {"id": "s5", "display": "الصفرية: محايد الجمع. و cA=O تكشف.",
     "spoken": "والمَصْفوفةُ الصِّفْرِيَّةُ مُحايِدُ الجَمْع. وتَذَكَّرِ القاعِدةَ الذَّهَبيَّة: إذا كانَ سِي أ يُساوي المَصْفوفةَ الصِّفْرِيَّة، فَإمّا أنْ يَكونَ سِي صِفْراً، أو تَكونَ أ صِفْرِيَّة.",
     "draw": sc_zero},
    {"id": "s6", "display": "الفخ: A B لا تساوي B A غالباً.",
     "spoken": "والفَخُّ الأشْهَر: أ في ب لا تُساوي ب في أ غالِباً. الضَّرْبُ لَهُ تَرْتيب — تَوَقَّفْ واسْأَلْ قَبْلَ أنْ تُبادِل.",
     "draw": sc_trap},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0004-matrix-properties", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0004")
