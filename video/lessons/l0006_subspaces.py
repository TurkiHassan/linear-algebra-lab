#!/usr/bin/env python3
"""0006 · subspaces — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "SUB 0006"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الفضاء الجزئي: ناد مغلق"),
           font=F(FDISP, 100), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "ثلاثة شروط — يسقط واحد يسقط النادي", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0006")
    return img


def sc_rules(img, d, t, D):
    ctext(d, 120, "اختبار من ثلاثة أسطر", F(FDISP_B, 52))
    rows = ["الصفر موجود", "الجمع مغلق: u+v يبقى", "الضرب مغلق: ku يبقى"]
    f = F(FSANS_M, 40)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.0:
            y = 260 + k * 100
            d.ellipse([W // 2 - 330, y - 26, W // 2 - 278, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 304, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 36))
    if t > 3.8:
        verdict(d, W // 2, 600, 420, "نعم ثلاث مرات = فضاء جزئي", True)
    return img


def sc_line0(img, d, t, D):
    ctext(d, 110, "خط عبر الأصل y = x", F(FDISP_B, 50))
    if t > 0.5:
        px = grid_axes(d, (390, 180, 890, 500), rng=5, step_px=42)
        x0, y0 = 390, 500
        d.line([(400, 490), (880, 190)], fill=ACCENT, width=5)
        d.ellipse([px((0, 0))[0] - 7, px((0, 0))[1] - 7,
                   px((0, 0))[0] + 7, px((0, 0))[1] + 7], fill=TERRA)
    if t > 2.2:
        verdict(d, W // 2, 585, 380, "فضاء جزئي", True)
    return img


def sc_line1(img, d, t, D):
    ctext(d, 110, "خط مزاح y = x + 1", F(FDISP_B, 50))
    if t > 0.5:
        px = grid_axes(d, (390, 180, 890, 500), rng=5, step_px=42)
        d.line([(400, 448), (880, 148)], fill=ACCENT, width=5)
        x0, y0 = px((0, 0))
        cross_mark(d, x0, y0, 16, TERRA)
    if t > 2.2:
        draw_mixed(d, W // 2, 560, "الصفر (0,0) لا يحقق 0 = 1: مرفوض في ثانية",
                   F(FSANS_M, 34), F(FMONO, 32), TERRA)
    if t > 3.4:
        verdict(d, W // 2 - 0, 640, 420, "ليس فضاء جزئيا", False)
    return img


def sc_quad(img, d, t, D):
    ctext(d, 110, "الربع الأول يحوي الصفر — فهل ينجو؟", F(FDISP_B, 48))
    if t > 0.6:
        latin_lines(d, W // 2, 280, 100, ["(-1) . (1,1)  =  (-1,-1)"], 42, t=t, stagger=0.6)
    if t > 2.0:
        draw_mixed(d, W // 2, 420, "الضرب بسالب يخرج من الربع",
                   F(FSANS_M, 36), F(FMONO, 34), TERRA)
    if t > 3.0:
        verdict(d, W // 2, 540, 480, "يسقط في الشرط الثالث", False)
    return img


SCENES = [
    {"id": "s1", "display": "الفضاء الجزئي: نادٍ مغلق بثلاثة شروط.",
     "spoken": "الفَضاءُ الجُزْئيّ: نادٍ مُغْلَقٌ بِثَلاثةِ شُروط. يَسْقُطُ شَرْطٌ واحِد، يَسْقُطُ النّادي كُلُّه.",
     "draw": sc_title},
    {"id": "s2", "display": "الصفر موجود، والجمع مغلق، والضرب مغلق.",
     "spoken": "الاخْتِبارُ مِنْ ثَلاثةِ أسْطُر: هَلِ الصِّفْرُ مَوْجود؟ وهَلْ مَجْموعُ أيِّ عُنْصُرَيْنِ يَبْقى داخِلَ المَجْموعة؟ وهَلْ أيُّ مُضاعَفٍ يَبْقى؟ نَعَمْ ثَلاثَ مَرّات، إذَنْ هو فَضاءٌ جُزْئيّ.",
     "draw": sc_rules},
    {"id": "s3", "display": "خط عبر الأصل: يحوي الصفر ومغلق — فضاء جزئي.",
     "spoken": "خَطٌّ يَمُرُّ بِالأصْل، مِثْلُ وايْ يُساوي إكْس: يَحْوي الصِّفْر، ومُغْلَقٌ تَحْتَ الجَمْعِ والضَّرْب. حُكْمُهُ: فَضاءٌ جُزْئيّ.",
     "draw": sc_line0},
    {"id": "s4", "display": "خط مزاح: الصفر مفقود — مرفوض في ثانية.",
     "spoken": "وخَطٌّ مُزاحٌ مِثْلُ وايْ يُساوي إكْس زائِدَ واحِد: الصِّفْرُ لَيْسَ فيه. مَرْفوضٌ في ثانِيةٍ واحِدة، قَبْلَ أنْ نَخْتَبِرَ شَيْئاً.",
     "draw": sc_line1},
    {"id": "s5", "display": "الربع الأول: يسقط في الضرب السالب.",
     "spoken": "والرُّبْعُ الأوَّلُ يَحْوي الصِّفْر، لَكِنَّ الضَّرْبَ في سالِبِ واحِدٍ يُخْرِجُ مِنه: سالِبُ واحِدٍ في واحِدٍ وواحِد، يُساوي سالِبَ واحِدٍ وسالِبَ واحِد — خارِجَ الرُّبْع. فَيَسْقُطُ في الشَّرْطِ الثّالِث.",
     "draw": sc_quad},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0006-subspaces", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0006")
