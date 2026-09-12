#!/usr/bin/env python3
"""0011 · drills bank + path recap — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "CAP 0011"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("بنك التدريبات: الإحماء"),
           font=F(FDISP, 100), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الورق أولا — واللوحة للتحقق فقط", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0011")
    return img


def sc_drills(img, d, t, D):
    ctext(d, 110, "ثلاث طلقات إحماء", F(FDISP_B, 50))
    rows = [("det [[2,-3],[1,2]] = 7", True),
            ("(1,2).(3,-1) = 1", True),
            ("(1,1),(2,2): dependent", False)]
    f = F(FMONO, 34)
    for k, (eq, good) in enumerate(rows):
        y = 245 + k * 125
        if t > 0.4 + k * 1.1:
            bb = d.textbbox((0, 0), eq, font=f)
            ew = bb[2] - bb[0]
            d.text((W // 2, y), eq, font=f, fill=INK, anchor="mm")
            if good:
                check_mark(d, W // 2 - ew // 2 - 55, y, 20, ACCENT)
            else:
                cross_mark(d, W // 2 - ew // 2 - 55, y, 18, TERRA)
    if t > 4.0:
        draw_mixed(d, W // 2, 640, "حل على ورقك ثم تحقق — لا تغش نفسك",
                   F(FSANS, 30), F(FMONO, 28), SOFT)
    return img


def sc_worked(img, d, t, D):
    ctext(d, 110, "مثال محلول كامل: الأوزان", F(FDISP_B, 50))
    latin_lines(d, W // 2, 245, 85,
                ["w = (5,3) from (2,0),(1,1)", "c2 = 3", "2c1 + 3 = 5  =>  c1 = 1",
                 "check: (5,3) OK"], 36, t=t, stagger=0.5)
    return img


def sc_path(img, d, t, D):
    ctext(d, 130, "المسار اكتمل", F(FDISP_B, 56))
    if t > 0.6:
        draw_mixed(d, W // 2, 260, "من الخطي إلى المحدد: عشر مهارات",
                   F(FSANS_M, 38), F(FMONO, 34), SOFT)
    if t > 1.6:
        latin_lines(d, W // 2, 380, 80,
                    ["linear > matrices > gauss > laws", "vectors > sub > combo > span",
                     "basis > det > drills"], 32, SOFT, t=t, stagger=1.6)
    if t > 4.2:
        verdict(d, W // 2, 600, 560, "مختبر الجبر الخطي · إلى الأمام", True)
    return img


SCENES = [
    {"id": "s1", "display": "بنك التدريبات: الورق أولاً، واللوحة للتحقق فقط.",
     "spoken": "بَنْكُ التَّدْريبات: الإحْماءُ قَبْلَ المُباراة. القاعِدة: الوَرَقُ أوَّلاً، واللَّوْحةُ لِلتَحَقُّقِ فَقَط. مَنْ يَتَحَقَّقْ قَبْلَ أنْ يُحاوِلْ يَسْرِقْ مِنْ نَفْسِهِ التَّدْريب.",
     "draw": sc_title},
    {"id": "s2", "display": "ثلاث طلقات إحماء: محدد، وضرب داخلي، واستقلال.",
     "spoken": "ثَلاثُ طَلَقاتِ إحْماء: مُحَدِّدُ المَصْفوفةِ اثْنانِ وسالِبُ ثَلاثة، وواحِدٌ واثْنان — يُساوي سَبْعة. وضَرْبٌ داخِلِيّ: واحِدٌ واثْنان مَعَ ثَلاثةٍ وسالِبِ واحِد — يُساوي واحِداً. وزَوْجُ واحِدٍ وواحِد مَعَ اثْنَيْنِ واثْنَيْن — مُرْتَبِط.",
     "draw": sc_drills},
    {"id": "s3", "display": "مثال محلول: أوزان (5,3) هي (1,3).",
     "spoken": "ومِثالٌ مَحْلولٌ كامِل: أوْزانُ خَمْسةٍ وثَلاثة مِنِ اثْنَيْنِ وصِفْر، وواحِدٍ وواحِد. المُعامِلُ الثّاني يُساوي ثَلاثة، واثْنان في المُعامِلِ الأوَّلِ زائِدُ ثَلاثةٍ يُساوي خَمْسة، إذَنْ المُعامِلُ الأوَّلُ يُساوي واحِداً. تَحَقَّقْ: خَمْسةٌ وثَلاثة — صَحيح.",
     "draw": sc_worked},
    {"id": "s4", "display": "من الخطي إلى المحدد: المسار اكتمل.",
     "spoken": "وبِهذا اكْتَمَلَ المَسار: مِنْ تَمْييزِ الخَطِّيّ، إلى المَصْفوفاتِ والحَذْفِ والقَوانين، إلى المُتَّجِهاتِ والفَضاءاتِ والتَّراكيب، إلى الأساسِ والمُحَدِّدات. مُخْتَبَرُ الجَبْرِ الخَطِّيّ — إلى الأمام.",
     "draw": sc_path},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0011-drills", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0011")
