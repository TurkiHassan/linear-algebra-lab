#!/usr/bin/env python3
"""0007 · linear combinations — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "CMB 0007"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("التركيب الخطي: خلطة بأوزان"),
           font=F(FDISP, 96), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الأوزان هي الوصفة — والسؤال عن وجودها", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0007")
    return img


def sc_mix(img, d, t, D):
    ctext(d, 110, "اخلط: ضخم ثم اجمع", F(FDISP_B, 50))
    if t > 0.5:
        px = grid_axes(d, (390, 170, 890, 470), rng=5, step_px=42)
        v1, v2 = (2, 0), (0, 2)
        x0, y0 = px((0, 0))
        for v, c in ((v1, (91, 63, 143)), (v2, TERRA)):
            x1, y1 = px(v)
            d.line([(x0, y0), (x1, y1)], fill=c, width=3)
    if t > 1.6:
        w = (3, 4)
        vec(d, px, w, ACCENT, width=5)
        f = F(FMONO, 26)
        d.text((px(w)[0] + 14, px(w)[1] - 14), "w", font=f, fill=ACCENT, anchor="mm")
    if t > 2.8:
        latin_lines(d, W // 2, 560, 80, ["w = 1.5(2,0) + 2(0,2) = (3,4)"], 34, t=t, stagger=2.8)
    return img


def sc_solve(img, d, t, D):
    ctext(d, 120, "هل الهدف تركيب منهما؟", F(FDISP_B, 52))
    latin_lines(d, W // 2, 250, 90,
                ["w = (5,3)  from  (2,0),(1,1)", "c2 = 3 ,  2c1 + 3 = 5  =>  c1 = 1"], 36,
                t=t, stagger=0.5)
    if t > 3.0:
        verdict(d, W // 2, 540, 420, "نعم: الأوزان (1,3)", True)
    return img


def sc_trap(img, d, t, D):
    ctext(d, 120, "مكونان متوازيان لا يغادران الخط", F(FDISP_B, 50))
    if t > 0.6:
        px = grid_axes(d, (390, 190, 890, 490), rng=5, step_px=42)
        x0, y0 = px((0, 0))
        for v in ((1, 1), (2, 2)):
            x1, y1 = px(v)
            d.line([(x0, y0), (x1, y1)], fill=ACCENT, width=4)
        tx, ty = px((3, 1))
        cross_mark(d, tx, ty, 16, TERRA)
    if t > 2.4:
        verdict(d, W // 2, 590, 480, "(3,1) مستحيلة منهما", False)
    return img


def sc_end(img, d, t, D):
    ctext(d, 200, "كل سؤال تركيب منظومة متنكرة", F(FDISP_B, 54))
    if t > 0.7:
        ctext(d, 310, "اكتب الأوزان أولا — ثم حل وتحقق", F(FSANS_M, 38), SOFT)
    if t > 1.5:
        verdict(d, W // 2, 450, 560, "الدرس 0007 · الأوزان هي السؤال", True)
    return img


SCENES = [
    {"id": "s1", "display": "التركيب الخطي: خلطة بأوزان. الأوزان هي الوصفة.",
     "spoken": "التَّرْكيبُ الخَطِّيّ: خَلْطةٌ بِأوْزان. الأوْزانُ هي الوَصْفة، والمُتَّجِهاتُ هي المُكَوِّنات.",
     "draw": sc_title},
    {"id": "s2", "display": "واحد ونصف في (2,0) زائد 2 في (0,2) يساوي (3,4).",
     "spoken": "اخْلِطْ: تَضْخيمٌ ثُمَّ جَمْع. واحِدٌ ونِصْفٌ في اثْنَيْنِ وصِفْر، زائِدُ اثْنَيْنِ في صِفْرٍ واثْنَيْن، يُساوي ثَلاثةً وأرْبَعة.",
     "draw": sc_mix},
    {"id": "s3", "display": "الهدف (5,3): الأوزان (1,3).",
     "spoken": "والسُّؤالُ العَكْسيّ: هَلْ خَمْسةٌ وثَلاثةٌ تَرْكيبٌ مِنِ اثْنَيْنِ وصِفْر، وواحِدٍ وواحِد؟ مِنَ السَّطْرِ الثّاني: المُعامِلُ الثّاني يُساوي ثَلاثة. نُعَوِّضُ في الأوَّل: اثْنان في المُعامِلِ الأوَّلِ زائِدُ ثَلاثةٍ يُساوي خَمْسة، إذَنْ المُعامِلُ الأوَّلُ يُساوي واحِداً. نَعَمْ، بِالأوْزانِ واحِدٍ وثَلاثة.",
     "draw": sc_solve},
    {"id": "s4", "display": "متوازيان: الأهداف خارج الخط مستحيلة.",
     "spoken": "لَكِنِ احْذَرْ: مُكَوِّنانِ مُتَوازِيانِ لا يُغادِرانِ خَطَّهُما أبَداً. النُّقْطةُ ثَلاثةٌ وواحِدٌ مُسْتَحيلةٌ مِنهُما.",
     "draw": sc_trap},
    {"id": "s5", "display": "كل سؤال تركيب منظومة متنكرة.",
     "spoken": "الخُلاصة: كُلُّ سُؤالِ تَرْكيبٍ هو مَنْظومةٌ خَطِّيَّةٌ مُتَنَكِّرة. اكْتُبِ الأوْزانَ أوَّلاً، ثُمَّ حُلَّ وتَحَقَّقْ.",
     "draw": sc_end},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0007-linear-combinations", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0007")
