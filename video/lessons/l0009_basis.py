#!/usr/bin/env python3
"""0009 · basis & dimension — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "BAS 0009"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("الأساس: أصغر فريق يغطي الملعب"),
           font=F(FDISP, 92), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "تغطية كاملة، بلا تداخل، بأقل عدد", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0009")
    return img


def sc_cond(img, d, t, D):
    ctext(d, 120, "شرطان معا — لا أحدهما", F(FDISP_B, 52))
    rows = ["مستقل: لا هدر ولا زائد", "مولد: يغطي الفضاء كله"]
    f = F(FSANS_M, 40)
    for k, r in enumerate(rows):
        if t > 0.5 + k * 1.1:
            y = 280 + k * 110
            d.ellipse([W // 2 - 330, y - 26, W // 2 - 278, y + 26], outline=ACCENT, width=4)
            d.text((W // 2 - 304, y - 1), str(k + 1), font=F(FMONO, 30), fill=ACCENT, anchor="mm")
            draw_mixed(d, W // 2 + 60, y, r, f, F(FMONO, 36))
    if t > 3.0:
        draw_mixed(d, W // 2, 560, "أساس = استقلال + توليد، والبعد = عدد الأعضاء",
                   F(FSANS_M, 36), F(FMONO, 32), ACCENT)
    return img


def sc_court(img, d, t, D):
    ctext(d, 110, "ثلاثة مرشحين لأساس R²", F(FDISP_B, 50))
    rows = [("(1,0),(0,1)", "المعياري: أساس", True),
            ("(1,1),(1,-1)", "المائل: أساس (det=-2)", True),
            ("(1,1),(2,2)", "المتوازي: ليس أساسا (det=0)", False)]
    f = F(FMONO, 34)
    for k, (eq, why, good) in enumerate(rows):
        y = 240 + k * 130
        if t > 0.4 + k * 1.2:
            d.text((W // 2, y), eq, font=f, fill=INK, anchor="mm")
            if good:
                check_mark(d, W // 2 - 300, y, 20, ACCENT)
            else:
                cross_mark(d, W // 2 - 300, y, 18, TERRA)
            draw_mixed(d, W // 2, y + 52, why, F(FSANS, 29), F(FMONO, 27),
                       ACCENT if good else TERRA)
    return img


def sc_coords(img, d, t, D):
    ctext(d, 120, "الإحداثيات تتبع الأساس", F(FDISP_B, 52))
    latin_lines(d, W // 2, 260, 95,
                ["(4,2) = 3(1,1) + 1(1,-1)", "coords = (3,1)"], 40, t=t, stagger=0.5)
    if t > 2.8:
        draw_mixed(d, W // 2, 500, "نفس النقطة (4,2) إحداثياتها (4,2) في المعياري",
                   F(FSANS_M, 34), F(FMONO, 32), SOFT)
    if t > 3.8:
        verdict(d, W // 2, 600, 480, "لا تخلط دفتر العناوين", True)
    return img


def sc_dim(img, d, t, D):
    ctext(d, 140, "والبعد؟ عد الأعضاء", F(FDISP_B, 54))
    latin_lines(d, W // 2, 280, 95,
                ["dim R2 = 2", "dim line = 1", "dim point = 0"], 42, t=t, stagger=0.6)
    if t > 3.4:
        verdict(d, W // 2, 590, 560, "الدرس 0009 · البعد ثابت للفضاء", True)
    return img


SCENES = [
    {"id": "s1", "display": "الأساس: أصغر فريق يغطي الملعب.",
     "spoken": "الأساس: أصْغَرُ فَريقٍ يُغَطّي المَلْعَب. تَغْطِيةٌ كامِلة، بِلا تَداخُل، وبِأقَلِّ عَدَد.",
     "draw": sc_title},
    {"id": "s2", "display": "أساس = استقلال + توليد. والبعد = عدد الأعضاء.",
     "spoken": "شَرْطانِ مَعاً، لا أحَدُهُما: مُسْتَقِلٌّ بِلا هَدَر، ومُوَلِّدٌ يُغَطّي الفَضاءَ كُلَّه. والبُعْدُ هو عَدَدُ أعْضاءِ أيِّ أساس.",
     "draw": sc_cond},
    {"id": "s3", "display": "المعياري والمائل أساسان. والمتوازي لا.",
     "spoken": "ثَلاثةُ مُرَشَّحينَ لِأساسِ المُسْتَوى: المِعْياريُّ أساس، والمائِلُ أساسٌ لِأنَّ مُحَدِّدَهُ يُساوي سالِبَ اثْنَيْن، والمُتَوازي لَيْسَ أساساً لِأنَّ مُحَدِّدَهُ صِفْر.",
     "draw": sc_court},
    {"id": "s4", "display": "إحداثيات (4,2) في المائل هي (3,1).",
     "spoken": "والإحْداثِيّاتُ تَتْبَعُ الأساس: أرْبَعةٌ واثْنان تُساوي ثَلاثةً في واحِدٍ وواحِد، زائِدُ واحِدٍ في واحِدٍ وسالِبِ واحِد. إذَنِ الإحْداثِيّاتُ ثَلاثةٌ وواحِد — لا تَخْلِطْ دَفْتَرَ العَناوين.",
     "draw": sc_coords},
    {"id": "s5", "display": "البعد: المستوى 2، والخط 1، والنقطة 0.",
     "spoken": "والبُعْد؟ عُدَّ الأعْضاءَ فَقَط: بُعْدُ المُسْتَوى اثْنان، وبُعْدُ الخَطِّ واحِد، وبُعْدُ النُّقْطةِ صِفْر. الدَّرْسُ التّاسِع: البُعْدُ ثابِتٌ لِلْفَضاء.",
     "draw": sc_dim},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0009-basis-dimension", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0009")
