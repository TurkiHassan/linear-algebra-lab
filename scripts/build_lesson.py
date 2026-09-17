#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""قالب صفحة الدرس — الهيكل الذي تشترك فيه كل الدروس.

يُستورد من ملف مواصفة يصف الدروس، ثم يكتبها إلى lessons/:

    from build_lesson import write_all
    write_all([L26, L27])

كل مواصفة قاموس فيه: id, slug, ar, enshort, enline, desc, module, prereq,
ref, prev, next, mins, body, script، و canvas=True إن كان في الدرس لوحة رسم
(فيُحمَّل assets/figure.js قبل سكربت الدرس وتُربط أسماؤه).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://turkihassan.github.io/linear-algebra-lab"

BASE_CSS = """  :root{--paper:#f6f1e7;--ink:#1c1a15;--soft:#6f6757;--line:#ded4c2;--accent:#0d5c46;--terra:#c2562f;--vio:#5b3f8f}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif-text);line-height:1.9}
  h1,h2,h3{font-family:var(--serif-display)}
  .masthead,.kicker,.meta,.hint,.card-tag,.btn,.opt,.coord,.readout,.footer{font-family:var(--th-sans)}
  .wrap{max-width:860px;margin:0 auto;padding:0 22px 90px}
  .masthead{display:flex;justify-content:space-between;gap:12px;padding:20px 0;border-bottom:3px solid var(--ink);font-size:12px}
  .hero{padding:38px 0 10px}
  .kicker{color:var(--accent);font-weight:700;font-size:12px}
  h1{font-size:clamp(34px,6vw,54px);line-height:1.25;margin:6px 0}
  .en-line{display:block;direction:ltr;text-align:left;color:var(--soft);font-size:14px}
  .rule{height:3px;background:var(--ink);margin:18px 0}
  .meta{color:var(--soft);font-size:13px}
  h2{font-size:26px;margin:54px 0 8px}
  .num{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--ink);color:#fff;font-size:17px;margin-left:10px}
  .en-sub{display:block;direction:ltr;text-align:left;color:var(--soft);font-size:13px}
  .analogy{border:1px solid var(--line);border-inline-start:6px solid var(--accent);border-radius:14px;padding:16px 18px;background:#fff;margin:20px 0}
  .card{border-radius:14px;padding:16px 18px;margin:20px 0;background:#fff;border:1px solid var(--line)}
  .card.idea{border-inline-start:6px solid var(--accent)}
  .card.warn{border-inline-start:6px solid var(--terra)}
  .card-tag{display:inline-block;font-size:11px;background:var(--ink);color:#fff;border-radius:999px;padding:3px 12px;margin-bottom:8px}
  .warn-tag{background:var(--terra)}
  .term{font-weight:800}
  .en{color:var(--soft)}
  .coord{direction:ltr;unicode-bidi:isolate;font-family:ui-monospace,Menlo,Consolas,monospace;background:#00000008;padding:0 6px;border-radius:6px}
  .demo{border:2px dashed var(--ink);border-radius:18px;padding:20px;margin:24px 0;background:#fff}
  .demo h3{margin:0 0 4px}
  .hint{color:var(--soft);font-size:13px;margin:0 0 12px}
  .controls{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0;align-items:center}
  .controls label{font-size:13px}
  .controls input[type=number]{width:64px;font:inherit;border:1.5px solid var(--line);border-radius:8px;padding:4px 8px;direction:ltr}
  .controls select{font:inherit;border:1.5px solid var(--line);border-radius:8px;padding:6px 10px;background:#fff}
  html{scroll-behavior:smooth}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  .btn{font:inherit;border:1.5px solid var(--ink);background:var(--ink);color:#fff;border-radius:999px;padding:9px 20px;cursor:pointer;transition:transform .15s ease,background .2s ease}
  .btn:hover{background:#000}
  .btn.ghost:hover{background:var(--ink);color:#fff}
  .btn:active{transform:scale(.97)}
  .opt:hover{border-color:var(--ink)}
  .controls.stick{position:sticky;bottom:12px;z-index:6;width:max-content;max-width:100%;background:color-mix(in srgb,#fff 90%,transparent);backdrop-filter:blur(10px);border:1px solid var(--line);border-radius:999px;padding:8px 12px;box-shadow:0 12px 32px rgba(0,0,0,.14)}
  .btn.ghost{background:transparent;color:var(--ink)}
  .opt{display:block;width:100%;text-align:start;font:inherit;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 14px;margin:8px 0;cursor:pointer}
  .opt:disabled{opacity:.75;cursor:default}
  .opt.ok{border-color:var(--accent);background:#0d5c4612}
  .opt.no{border-color:var(--terra);background:#c2562f12}
  .feedback{font-size:13px;min-height:1.6em;color:var(--soft)}
  .readout{font-family:ui-monospace,Menlo,Consolas,monospace;direction:ltr;text-align:left;background:var(--ink);color:#f6f1e7;border-radius:12px;padding:12px 16px;margin-top:12px;overflow-x:auto}
  .footer{margin-top:60px;border-top:1px solid var(--line);padding-top:16px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--soft)}
  table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
  th,td{border:1px solid var(--line);padding:9px 12px;text-align:start}
  th{background:#00000008}
  .kmath{direction:ltr;text-align:center;overflow-x:auto;padding:8px;background:#fff;border:1px solid var(--line);border-radius:12px;margin:12px 0}
  a{color:var(--accent)}"""

# عقد اللوحة نفسه في assets/lesson.css — لا يُكرَّر هنا. يبقى وصف الشكل فقط.
CANVAS_CSS = """
  .figcap{font-family:var(--th-sans);font-size:12.5px;color:var(--soft);text-align:center;margin:2px 0 0}"""

QUIZ_JS = """  document.querySelectorAll('.q').forEach(function(box){
    var id=box.id,fb=box.querySelector('.feedback'),opts=box.querySelectorAll('.opt'),done=false;
    opts.forEach(function(b){b.addEventListener('click',function(){
      if(done)return;done=true;var a=b.getAttribute('data-a'),info=ANS[id][a];
      opts.forEach(function(o){o.disabled=true;if(ANS[id][o.getAttribute('data-a')][1])o.classList.add('ok');});
      if(!info[1])b.classList.add('no');fb.textContent=info[0];
    });});
  });"""

FIG_BIND = """  var FIG = LinalgFig.FIG, onTheme = LinalgFig.onTheme, plane = LinalgFig.plane;
"""

REFS = """  <div class="refs">
    <span class="card-tag">مراجع خارجية</span>
    <ul>
      <li><a href="https://mml-book.github.io/" target="_blank" rel="noopener" lang="en">Mathematics for Machine Learning — Deisenroth, Faisal, Ong</a><span>{ref}</span></li>
      <li><a href="https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" target="_blank" rel="noopener" lang="en">3Blue1Brown — Essence of Linear Algebra</a></li>
    </ul>
  </div>"""


def page(L):
    slug = L["slug"]
    css = BASE_CSS + (CANVAS_CSS if L.get("canvas") else "") + L.get("css", "")
    prev_a = '<a href="%s.html">→ السابق</a> · ' % L["prev"][0]
    next_a = ' · <a href="%s.html">التالي ←</a>' % L["next"][0] if L.get("next") else ""
    pager_next = ('<a class="next" href="%s.html" rel="next"><small>الدرس التالي</small>%s</a>'
                  % (L["next"][0], L["next"][1])) if L.get("next") else \
        '<a class="next home" href="../index.html"><small>اكتمل المسار</small>إلى الفهرس</a>'
    return """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{id} · {ar} — {enshort}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/lessons/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{id} · {ar} — مختبر الجبر الخطي">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="ar_SA">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<link rel="stylesheet" href="../assets/lesson-fonts.css">
<style>
{css}
</style>
<link rel="stylesheet" href="../assets/lesson.css">
<link rel="stylesheet" href="../assets/ui.css">
<link rel="manifest" href="../manifest.webmanifest">
<meta name="theme-color" content="#faf7f2">
<link rel="icon" type="image/png" href="../assets/icons/icon-192.png">
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "LearningResource",
 "inLanguage": "ar",
 "name": "{id} · {ar}",
 "alternateName": "{enshort}",
 "description": "{desc}",
 "url": "{site}/lessons/{slug}.html",
 "learningResourceType": [
  "درس تفاعلي",
  "تمرين برمجي"
 ],
 "educationalLevel": "جامعي — مقدمة",
 "isPartOf": {{
  "@type": "Course",
  "name": "مختبر الجبر الخطي",
  "url": "{site}/"
 }},
 "position": {pos}
}}
</script>
</head>
<body data-lesson-id="{id}">
<div class="wrap">
  <div class="masthead"><div>مختبر الجبر الخطي <b>· من الصفر</b></div><div>{prev_a}<a href="../index.html">الرئيسية</a> · <a href="../map.html#l{id}">الخارطة</a>{next_a}</div></div>
  <header class="hero">
    <div class="kicker">الدرس {id} · {module}</div>
    <h1>{ar}</h1>
    <span class="en-line" lang="en">{enline}</span>
    <div class="rule"></div>
    <p class="meta">~{mins} دقيقة · المتطلب: الدرس {prereq}</p>
  </header>

{body}

  <div class="lesson-tools" role="group" aria-label="أدوات الدرس">
    <button class="tool-btn theme-btn" type="button">الوضع الداكن</button>
    <button class="tool-btn" type="button" onclick="window.print()">طباعة / PDF</button>
    <a class="tool-btn" href="../playground.html?ex={slug}">شغّل التمرين في المتصفح</a>
    <a class="tool-btn" href="../map.html#l{id}">موضع الدرس في الخارطة</a>
    <a class="tool-btn" href="../review.html#l{id}">بطاقات المراجعة</a>
    <button class="tool-btn done-toggle" type="button" data-lesson="{id}" aria-pressed="false">أتممت الدرس</button>
  </div>
{refs}
  <nav class="pager" aria-label="التنقل بين الدروس">
    <a class="prev" href="{prev_slug}.html" rel="prev"><small>الدرس السابق</small>{prev_title}</a>
    {pager_next}
  </nav>
  <footer class="footer"><span>الدرس {id} · {ar}</span><span>التمرين: <code lang="en">python3 practice/{slug}.py</code> · <a href="../playground.html?ex={slug}">في المتصفح</a></span></footer>
</div>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
{figsrc}<script>
(function(){{
  "use strict";
  function tex(el,s){{try{{if(window.katex)katex.render(s,el,{{throwOnError:false}});else el.textContent=s;}}catch(e){{el.textContent=s;}}}}
{script}
{quizjs}
}})();
</script>
<script src="../assets/site.js"></script>
<script src="../assets/ui.js"></script>
</body>
</html>
""".format(id=L["id"], ar=L["ar"], enshort=L["enshort"], desc=L["desc"], site=SITE, slug=slug,
           css=css, pos=int(L["id"]), prev_a=prev_a, next_a=next_a, module=L["module"],
           enline=L["enline"], mins=L["mins"], prereq=L["prereq"], body=L["body"],
           refs=REFS.format(ref=L["ref"]), prev_slug=L["prev"][0], prev_title=L["prev"][1],
           pager_next=pager_next,
           figsrc=('<script src="../assets/figure.js"></script>\n' if L.get("canvas") else ""),
           script=((FIG_BIND + L["script"]) if L.get("canvas") else L["script"]), quizjs=QUIZ_JS)


def write_all(lessons):
    for L in lessons:
        p = os.path.join(ROOT, "lessons", L["slug"] + ".html")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(page(L))
        print("wrote", p)
