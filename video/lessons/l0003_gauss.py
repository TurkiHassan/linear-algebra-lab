#!/usr/bin/env python3
"""0003 · Gaussian elimination — motion explainer with Hamed narration.

The original standalone build (make_video.py) is folded into the shared
vidcore framework so all eleven videos share one pipeline, one voice and
word-timed subtitles.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "GAU 0003"

FULL = [[2, 4, 6, 22], [3, 8, 5, 27], [-1, 1, 2, 2]]
S1 = [[1, 2, 3, 11], [3, 8, 5, 27], [-1, 1, 2, 2]]
S2 = [[1, 2, 3, 11], [0, 2, -4, -6], [0, 3, 5, 13]]
S3 = [[1, 2, 3, 11], [0, 1, -2, -3], [0, 3, 5, 13]]
S4 = [[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 11, 22]]
S5 = [[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 1, 2]]
CH1 = [(0, 0), (0, 1), (0, 2), (0, 3)]
CH2 = [(1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)]
CH3 = [(1, 1), (1, 2), (1, 3)]
CH4 = [(2, 1), (2, 2), (2, 3)]
CH5 = [(2, 2), (2, 3)]

EQ_LINES = ["2x + 4y + 6z = 22", "3x + 8y + 5z = 27", "-x + y + 2z = 2"]


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    y0 = 300 - int(30 * (1 - a))
    d.text((W // 2, y0), ar("الحذف الغاوسي"), font=F(FDISP, 120), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 420, "من المنظومة إلى الحل، في خمس خطوات", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 520, "الدرس 0003")
    return img


def sc_system(img, d, t, D):
    ctext(d, 130, "منظومتنا: ثلاث معادلات خطية", F(FDISP_B, 54))
    f = F(FMONO, 44)
    ys = [270, 370, 470]
    for k, (ln, y) in enumerate(zip(EQ_LINES, ys)):
        if t > 0.4 + k * 0.9:
            a = ease_out((t - 0.4 - k * 0.9) / 0.5)
            d.text((W // 2, y - int(16 * (1 - a))), ln, font=f, fill=INK, anchor="mm")
    if t > 3.2:
        d.rounded_rectangle([W // 2 - 330, 540, W // 2 + 330, 600], radius=30, outline=ACCENT, width=3)
        ctext(d, 571, "كلها خطية: الأس واحد، بلا دوال، بلا ضرب متغيرات", F(FSANS, 28), ACCENT)
    return img


def _mx_scene(img, d, t, rows, piv, circles, title, chip_t, beats, raw_chips=()):
    ctext(d, 125, title, F(FDISP_B, 50))
    if t > beats[0]:
        if raw_chips:
            xs = {2: [-215, 215], 3: [-360, 0, 360]}[len(raw_chips)]
            for lbl, dx in zip(raw_chips, xs):
                if lbl == "و":
                    d.text((W // 2 + dx, 200), ar("و"), font=F(FSANS_B, 30), fill=INK, anchor="mm")
                else:
                    chip_raw(d, W // 2 + dx, 200, lbl)
        else:
            chip(d, W // 2, 200, chip_t)
    if t > beats[1]:
        draw_matrix(d, W // 2 - 250, 260, 108, 64, rows, piv,
                    circles if t > beats[2] else (), pop((t - beats[2]) / 0.4), aug=True)
    return img


def sc_aug(img, d, t, D):
    return _mx_scene(img, d, t, S1, (0, 0), set(CH1),
                     "المصفوفة الموسعة — ثم نقسم الصف الأول على 2", "R₁ ÷ 2", (0.3, 0.9, 2.2))


def sc_elim1(img, d, t, D):
    return _mx_scene(img, d, t, S2, (1, 0), set(CH2),
                     "نصفّر تحت القائد", None, (0.3, 0.9, 2.2),
                     raw_chips=("−3R₁+R₂", "و", "R₁+R₃"))


def sc_mid(img, d, t, D):
    ctext(d, 120, "قائد جديد، ثم تصفير جديد", F(FDISP_B, 50))
    if t > 0.3:
        chip_raw(d, W // 2 - 215, 195, "R₂ ÷ 2")
        d.text((W // 2, 195), ar("ثم"), font=F(FSANS_B, 30), fill=INK, anchor="mm")
        chip_raw(d, W // 2 + 215, 195, "−3R₂+R₃")
    if t > 0.9:
        draw_matrix(d, 150, 250, 96, 58, S3, (1, 1), set(CH3) if t > 2.0 else (),
                    pop((t - 2.0) / 0.4), aug=True)
    if t > 3.4:
        draw_matrix(d, 700, 250, 96, 58, S4, (2, 1), set(CH4) if t > 4.4 else (),
                    pop((t - 4.4) / 0.4), aug=True)
    if t > 3.4:
        ax, ay = 660, 380
        d.line([(ax + 34, ay), (ax - 30, ay)], fill=SOFT, width=5)
        d.line([(ax - 30, ay), (ax - 8, ay - 12)], fill=SOFT, width=5)
        d.line([(ax - 30, ay), (ax - 8, ay + 12)], fill=SOFT, width=5)
    return img


def sc_tri(img, d, t, D):
    ctext(d, 125, "القسمة الأخيرة — واكتمل المثلث", F(FDISP_B, 50))
    if t > 0.3:
        chip(d, W // 2, 200, "R₃ ÷ 11")
    if t > 0.9:
        draw_matrix(d, W // 2 - 250, 250, 108, 64, S5, (2, 2), set(CH5) if t > 2.0 else (), pop((t - 2.0) / 0.4))
    if t > 3.0:
        d.rounded_rectangle([W // 2 - 200, 520, W // 2 + 200, 590], radius=30, fill=ACCENT)
        d.text((W // 2, 556), "z = 2", font=F(FMONO, 44), fill=WHITE, anchor="mm")
    return img


def sc_back(img, d, t, D):
    ctext(d, 115, "التعويض الخلفي: نصعد السلم", F(FDISP_B, 50))
    f = F(FMONO, 38)
    lines = ["z = 2", "y - 2(2) = -3  =>  y = 1", "x + 2(1) + 3(2) = 11  =>  x = 3"]
    ys = [230, 320, 410]
    for k, (ln, y) in enumerate(zip(lines, ys)):
        if t > 0.4 + k * 1.0:
            d.text((W // 2, y), ln, font=f, fill=INK, anchor="mm")
    if t > 3.6:
        d.rounded_rectangle([W // 2 - 350, 452, W // 2 + 350, 528], radius=30, fill=INK)
        d.text((W // 2, 491), "( x , y , z ) = ( 3 , 1 , 2 )", font=F(FMONO, 38), fill=WHITE, anchor="mm")
    if t > 4.6:
        d.rounded_rectangle([W // 2 - 350, 545, W // 2 + 350, 645], radius=30, outline=ACCENT, width=3)
        ctext(d, 572, "تحقق بنفسك: عوّض الحل في المعادلة الأولى", F(FSANS, 30), ACCENT)
        d.text((W // 2, 612), "2(3) + 4(1) + 6(2) = 22", font=F(FMONO, 30), fill=ACCENT, anchor="mm")
    return img


SCENES = [
    {"id": "s1",
     "display": "الحَذْفُ الغاوْسيّ. مِنَ المَنْظومةِ إلى الحَلّ، في خَمْسِ خُطُوات.",
     "spoken": "الحَذْفُ الغاوْسيّ. مِنَ المَنْظومةِ إلى الحَلّ، في خَمْسِ خُطُوات.",
     "draw": sc_title},
    {"id": "s2",
     "display": "منظومة من ثلاث معادلات خطية: 2x+4y+6z=22 ، 3x+8y+5z=27 ، −x+y+2z=2.",
     "spoken": "مَنْظومَتُنا ثَلاثُ مُعادَلاتٍ خَطِّيَّة. اثْنان إكْس زائِدُ أرْبَعة وايْ زائِدُ سِتَّة زِد يُساوي اثْنَيْنِ وعِشْرين. ثَلاثةُ إكْس زائِدُ ثَمانِية وايْ زائِدُ خَمْسةِ زِد يُساوي سَبْعةً وعِشْرين. وسالِبُ إكْس زائِدُ وايْ زائِدُ اثْنَيْن زِد يُساوي اثْنَيْن.",
     "draw": sc_system},
    {"id": "s3",
     "display": "نكتب المصفوفة الموسّعة ثم نقسم الصف الأول على 2.",
     "spoken": "نَكْتُبُ المَصْفوفةَ المُوَسَّعة: المُعامِلاتُ يَسارَ الخَطّ، والثَّوابِتُ يَمينَه. الخُطْوةُ الأولى: نَقْسِمُ الصَّفَّ الأوَّلَ على اثْنَيْن، فَيُصْبِحُ القائِدُ واحِداً.",
     "draw": sc_aug},
    {"id": "s4",
     "display": "نُصَفِّرُ تحت القائد: −3R₁+R₂ و R₁+R₃.",
     "spoken": "الآنَ نُصَفِّرُ تَحْتَ القائِد: نَطْرَحُ ثَلاثةَ أمْثالِ الصَّفِّ الأوَّلِ مِنَ الصَّفِّ الثّاني، ونَجْمَعُ الصَّفَّ الأوَّلَ مَعَ الثّالِث. العَمودُ الأوَّلُ صارَ واحِداً في الأعْلى، وصِفْرَيْنِ تَحْتَه.",
     "draw": sc_elim1},
    {"id": "s5",
     "display": "R₂÷2 ثم −3R₂+R₃: يكتمل المثلث تقريباً.",
     "spoken": "نَقْسِمُ الصَّفَّ الثّانيَ على اثْنَيْن، فَيُصْبِحُ قائِدُهُ واحِداً. ثُمَّ نَطْرَحُ ثَلاثةَ أمْثالِ الثّاني مِنَ الثّالِث، فَيَكْتَمِلُ المُثَلَّثُ تَقْريباً.",
     "draw": sc_mid},
    {"id": "s6",
     "display": "R₃÷11: اكتمل المثلث، ونقرأ z = 2.",
     "spoken": "وأخيراً نَقْسِمُ الصَّفَّ الثّالِثَ على أحَدَ عَشَر. اكْتَمَلَ المُثَلَّث، ونَقْرَأُ زِد يُساوي اثْنَيْنِ مُباشَرة.",
     "draw": sc_tri},
    {"id": "s7",
     "display": "التعويض الخلفي: z = 2 ثم y = 1 ثم x = 3.",
     "spoken": "بِالتَّعْويضِ الخَلْفيّ: وايْ ناقِصُ أرْبَعة يُساوي سالِبَ ثَلاثة، إذَنْ وايْ يُساوي واحِداً. وإكْس زائِدُ اثْنَيْن زائِدُ سِتَّة يُساوي أحَدَ عَشَر، إذَنْ إكْس يُساوي ثَلاثة. الحَلّ: ثَلاثةٌ وواحِدٌ واثْنان. عَوِّضْ في الأصْلِ لِتَتَحَقَّقَ بِنَفْسِك.",
     "draw": sc_back},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0003-gaussian-elimination", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0003")
