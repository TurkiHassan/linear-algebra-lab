#!/usr/bin/env python3
"""0005 · euclidean vector spaces — motion explainer with Hamed narration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from vidcore import *  # noqa: E402,F403

TAG = "VEC 0005"


def sc_title(img, d, t, D):
    a = ease_out(t / 0.6)
    d.text((W // 2, 300 - int(30 * (1 - a))), ar("المتجه: عنوان في الفضاء"),
           font=F(FDISP, 100), fill=INK, anchor="mm")
    if t > 0.5:
        ctext(d, 425, "الترتيب هو المعنى: (3,8) ليست (8,3)", F(FSANS_M, 40), SOFT)
    if t > 1.0:
        chip(d, W // 2, 525, "الدرس 0005")
    return img


def sc_ops(img, d, t, D):
    ctext(d, 115, "الجمع والتمديد: عنصرا بعنصر", F(FDISP_B, 50))
    if t > 0.5:
        px = grid_axes(d, (400, 180, 880, 500), rng=5, step_px=40)
    if t > 1.0:
        vec(d, px, (3, 2), ACCENT)
    if t > 1.8:
        vec(d, px, (-1, 4), TERRA)
    if t > 2.8:
        draw_mixed(d, W // 2, 580, "u+v تجمع المتناظر، و ku تضخم الجميع",
                   F(FSANS_M, 34), F(FMONO, 32), SOFT)
    return img


def sc_dot(img, d, t, D):
    ctext(d, 115, "الضرب الداخلي: رقم التشابه", F(FDISP_B, 50))
    latin_lines(d, W // 2, 250, 100,
                ["<u,v> = u1v1 + u2v2 + ...", "(1,2).(3,-1) = 3 - 2 = 1"], 40, t=t, stagger=0.5)
    if t > 3.0:
        verdict(d, W // 2, 540, 560, "اضرب المتناظر ثم اجمع", True)
    return img


def sc_len(img, d, t, D):
    ctext(d, 115, "الطول والمسافة: امتداد فيثاغورس", F(FDISP_B, 48))
    latin_lines(d, W // 2, 250, 100,
                ["||u|| = sqrt(u1^2 + u2^2)", "||(3,4)|| = 5", "d(u,v) = ||u - v||"], 40, t=t, stagger=0.5)
    if t > 3.4:
        verdict(d, W // 2, 580, 420, "المسافة = طول الفرق", True)
    return img


def sc_orth(img, d, t, D):
    ctext(d, 130, "الصفر يكشف الزاوية القائمة", F(FDISP_B, 52))
    if t > 0.7:
        latin_lines(d, W // 2, 270, 95, ["(3,1).(-1,3) = -3 + 3 = 0"], 42, t=t, stagger=0.7)
    if t > 2.2:
        verdict(d, W // 2, 470, 460, "متعامدان", True)
    if t > 3.0:
        draw_mixed(d, W // 2, 580, "الصفري طوله صفر — لا يصلح اتجاهاً",
                   F(FSANS, 30), F(FMONO, 28), SOFT)
    return img


SCENES = [
    {"id": "s1", "display": "المتجه: عنوان في الفضاء. الترتيب هو المعنى.",
     "spoken": "المُتَّجِهُ عُنْوانٌ في الفَضاء، والتَّرْتيبُ هو المَعْنى: ثَلاثة وثَمانِية، لَيْسَتْ ثَمانِيةً وثَلاثة.",
     "draw": sc_title},
    {"id": "s2", "display": "الجمع والتمديد عنصراً بعنصر.",
     "spoken": "الجَمْعُ والتَّمْديدُ عُنْصُراً بِعُنْصُر: المُتَناظِرُ مَعَ المُتَناظِر، والتَّرْتيبُ مَحْفوظٌ دائماً.",
     "draw": sc_ops},
    {"id": "s3", "display": "الضرب الداخلي: اضرب المتناظر ثم اجمع.",
     "spoken": "والضَّرْبُ الدّاخِليُّ رَقَمُ التَّشابُه: اضْرِبِ المُتَناظِرَ ثُمَّ اجْمَع. واحِدٌ واثْنان مَعَ ثَلاثةٍ وسالِبِ واحِد: ثَلاثةٌ ناقِصُ اثْنَيْن يُساوي واحِداً.",
     "draw": sc_dot},
    {"id": "s4", "display": "الطول جذر مجموع المربعات. والمسافة طول الفرق.",
     "spoken": "والطّولُ امْتِدادُ فيثاغورْس: جَذْرُ مَجْموعِ المُربَّعات. طولُ ثَلاثةٍ وأرْبَعة يُساوي خَمْسة. والمَسافةُ بَيْنَ نُقْطَتَيْنِ هي طولُ الفَرْقِ بَيْنَهُما.",
     "draw": sc_len},
    {"id": "s5", "display": "الضرب الداخلي صفر يعني تعامداً.",
     "spoken": "وأجْمَلُ ثِمارِ الضَّرْبِ الدّاخِليّ: إذا كانَ النّاتِجُ صِفْراً فَالمُتَّجِهانِ مُتَعامِدان. ثَلاثةٌ وواحِد مَعَ سالِبِ واحِدٍ وثَلاثة: سالِبُ ثَلاثةٍ زائِدُ ثَلاثةٍ يُساوي صِفْراً — زاوِيةٌ قائِمة.",
     "draw": sc_orth},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    tmp = "/var/folders/w5/k0crbh412l30rjl8s8s8nwjr0000gn/T/opencode/coursevid"
    build_video("0005-euclidean-spaces", SCENES, out, tmp, TAG,
                "مختبر الجبر الخطي · الدرس 0005")
