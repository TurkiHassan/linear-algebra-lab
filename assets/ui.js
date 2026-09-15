/* ===================================================================
   طبقة السلوك المشتركة — مختبر الجبر الخطي
   Loaded on every page, AFTER assets/site.js.

   يضيف: لوحة الأوامر (Ctrl/⌘+K)، اختصارات لوحة المفاتيح، فهرس الدرس
   الجانبي، شريط تقدّم القراءة، تصحيح الاختبار وحفظ الدرجة، «تابع من
   حيث توقفت»، سلسلة الأيام، والتنبيهات.

   لا يعتمد على أي مكتبة خارجية، ويعمل دون اتصال.
   =================================================================== */
(function () {
  "use strict";

  /* ---------- constants ------------------------------------------- */
  var K = {
    done:   "linalg:done",
    quiz:   "linalg:quiz",
    resume: "linalg:resume",
    streak: "linalg:streak",
    seen:   "linalg:seen"
  };

  var LESSONS = [
    { id: "0001", file: "0001-linear-systems.html",       t: "منظومات المعادلات الخطية",    m: 1 },
    { id: "0002", file: "0002-matrices-inverse.html",     t: "المصفوفات والنظير الضربي",     m: 1 },
    { id: "0003", file: "0003-gaussian-elimination.html", t: "الحذف الغاوسي خطوة بخطوة",     m: 1 },
    { id: "0004", file: "0004-matrix-properties.html",    t: "خصائص المصفوفات والصفرية",     m: 1 },
    { id: "0005", file: "0005-euclidean-spaces.html",     t: "فضاء المتجهات الإقليدي",       m: 2 },
    { id: "0006", file: "0006-subspaces.html",            t: "الفضاء الجزئي",                m: 2 },
    { id: "0007", file: "0007-linear-combinations.html",  t: "التركيب الخطي",                m: 2 },
    { id: "0008", file: "0008-span-independence.html",    t: "المولد والاستقلال الخطي",      m: 2 },
    { id: "0009", file: "0009-basis-dimension.html",      t: "الأساس والأبعاد",              m: 3 },
    { id: "0010", file: "0010-determinants.html",         t: "المحددات من 2×2 إلى 3×3",      m: 3 },
    { id: "0011", file: "0011-drills.html",               t: "بنك التدريبات مع الحلول",      m: 3 }
  ];

  /* ---------- storage helpers -------------------------------------- */
  function read(key, fb) {
    try { var v = JSON.parse(localStorage.getItem(key)); return v === null ? fb : v; }
    catch (e) { return fb; }
  }
  function write(key, v) {
    try { localStorage.setItem(key, JSON.stringify(v)); return true; } catch (e) { return false; }
  }
  function todayKey() {
    var d = new Date();
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  }
  function daysBetween(a, b) {
    return Math.round((Date.parse(b + "T00:00:00") - Date.parse(a + "T00:00:00")) / 86400000);
  }

  /* ---------- paths ------------------------------------------------ */
  var thisSrc = (document.currentScript && document.currentScript.src) || "";
  var ROOT = thisSrc.replace(/assets\/ui\.js.*$/, "");
  if (!ROOT) ROOT = /\/lessons\//.test(location.pathname) ? "../" : "./";
  function url(p) { return ROOT + p; }

  /* ---------- page identity ---------------------------------------- */
  var body = document.body;
  var lessonId = body ? body.getAttribute("data-lesson-id") : null;
  if (!lessonId) {
    var m = location.pathname.match(/(\d{4})-[a-z-]+\.html$/);
    if (m) lessonId = m[1];
  }
  var lessonIdx = -1;
  for (var li = 0; li < LESSONS.length; li++) if (LESSONS[li].id === lessonId) lessonIdx = li;
  var isLesson = lessonIdx >= 0;

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function reduceMotion() {
    return !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  /* =================================================================
     1) التنبيهات — toasts
     ================================================================= */
  var toastHost = null;
  function toast(msg, ms) {
    if (!toastHost) {
      toastHost = el("div", "ui-toasts");
      toastHost.setAttribute("role", "status");
      toastHost.setAttribute("aria-live", "polite");
      document.body.appendChild(toastHost);
    }
    var t = el("div", "ui-toast", esc(msg));
    toastHost.appendChild(t);
    setTimeout(function () {
      t.className = "ui-toast leaving";
      setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 260);
    }, ms || 2600);
  }
  window.linalgToast = toast;

  /* =================================================================
     2) الأرشيف العربي للبحث — Arabic-tolerant normaliser
     ================================================================= */
  var DIAC = /[ً-ْٰـ]/g;
  function norm(s) {
    return (s || "").replace(DIAC, "")
      .replace(/[أإآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ؤ/g, "و").replace(/ئ/g, "ي")
      .replace(/ة/g, "ه").toLowerCase().trim();
  }

  /* =================================================================
     3) لوحة الأوامر — command palette (Ctrl/⌘+K, /)
     ================================================================= */
  var pal = null, palInput, palList, palEmpty, palItems = [], palSel = 0, palLastFocus = null;
  var corpus = null, corpusLoading = false;

  var ACTIONS = [
    { t: "الصفحة الرئيسية",        s: "فهرس المقرر والدروس الأحد عشر",       href: "index.html",      kind: "تنقل" },
    { t: "الخارطة الذهنية الشاملة", s: "كل مفاهيم المقرر وروابطها في لوحة واحدة", href: "map.html",    kind: "تنقل" },
    { t: "الملخص الشامل",          s: "مرجع دراسي كامل مع أمثلة محلولة",      href: "summary.html",    kind: "تنقل" },
    { t: "المراجعة المتباعدة",      s: "بطاقات مجدولة بخوارزمية SM-2",         href: "review.html",     kind: "تنقل" },
    { t: "البحث الموحّد",           s: "بحث في المصطلحات ومحتوى الدروس",       href: "search.html",     kind: "تنقل" },
    { t: "مشغّل بايثون",            s: "شغّل التمارين داخل المتصفح",            href: "playground.html", kind: "تنقل" },
    { t: "بنك التدريبات",           s: "الدرس 0011 — تدريبات واختبار ختامي",    href: "lessons/0011-drills.html", kind: "تنقل" }
  ];

  function ensureCorpus(cb) {
    if (window.LINALG_DATA) { corpus = flatten(window.LINALG_DATA); return cb(); }
    if (corpusLoading) return;
    corpusLoading = true;
    var s = document.createElement("script");
    s.src = url("assets/search-data.js");
    s.onload = function () { corpus = flatten(window.LINALG_DATA || []); corpusLoading = false; cb(); };
    s.onerror = function () { corpus = []; corpusLoading = false; cb(); };
    document.head.appendChild(s);
  }
  function flatten(data) {
    var out = [];
    (data || []).forEach(function (les) {
      (les.entries || []).forEach(function (e) {
        out.push({
          kind: e.type === "term" ? "مصطلح" : (e.type === "lesson" ? "درس" : "قسم"),
          t: e.title || les.title,
          s: (e.type === "term" ? (e.en || "") + " — " : "") + (e.text || les.title),
          href: les.url + (e.anchor || ""),
          hay: norm((e.title || "") + " " + (e.en || "") + " " + (e.text || "") + " " + les.title)
        });
      });
    });
    return out;
  }

  function buildPalette() {
    pal = el("div", "ui-palette");
    pal.setAttribute("role", "dialog");
    pal.setAttribute("aria-modal", "true");
    pal.setAttribute("aria-label", "لوحة الأوامر والبحث السريع");
    pal.innerHTML =
      '<div class="ui-pal-box">' +
        '<div class="ui-pal-inputrow">' +
          '<span class="ui-pal-icon" aria-hidden="true">🔍</span>' +
          '<input class="ui-pal-input" type="text" autocomplete="off" spellcheck="false" ' +
                 'placeholder="ابحث عن درس أو مصطلح أو انتقل إلى صفحة…" aria-label="بحث وأوامر">' +
          '<span class="ui-pal-esc">Esc</span>' +
        '</div>' +
        '<ul class="ui-pal-list" role="listbox" aria-label="النتائج"></ul>' +
        '<p class="ui-pal-empty ui-hidden">لا نتائج — جرّب كلمة أقصر أو بلا تشكيل.</p>' +
        '<div class="ui-pal-foot">' +
          '<span><span class="ui-key">↑</span> <span class="ui-key">↓</span> تنقّل</span>' +
          '<span><span class="ui-key">Enter</span> فتح</span>' +
          '<span><span class="ui-key">?</span> كل الاختصارات</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(pal);
    palInput = pal.querySelector(".ui-pal-input");
    palList  = pal.querySelector(".ui-pal-list");
    palEmpty = pal.querySelector(".ui-pal-empty");

    palInput.addEventListener("input", renderPalette);
    palInput.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); movePal(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); movePal(-1); }
      else if (e.key === "Enter") { e.preventDefault(); openPalItem(palSel); }
      else if (e.key === "Escape") { e.preventDefault(); closePalette(); }
    });
    pal.addEventListener("mousedown", function (e) { if (e.target === pal) closePalette(); });
    palList.addEventListener("click", function (e) {
      var li = e.target.closest ? e.target.closest(".ui-pal-item") : null;
      if (li) { e.preventDefault(); openPalItem(+li.getAttribute("data-i")); }
    });
  }

  function palResults(q) {
    var nq = norm(q);
    var acts = ACTIONS.map(function (a) {
      return { kind: a.kind, t: a.t, s: a.s, href: url(a.href), hay: norm(a.t + " " + a.s) };
    });
    var lessons = LESSONS.map(function (l) {
      return {
        kind: "درس " + l.id, t: l.id + " · " + l.t, s: "افتح الدرس التفاعلي",
        href: url("lessons/" + l.file), hay: norm(l.id + " " + l.t)
      };
    });
    var pool = acts.concat(lessons).concat(corpus || []);
    if (!nq) return acts.concat(lessons).slice(0, 14);
    var hits = [];
    for (var i = 0; i < pool.length && hits.length < 220; i++) {
      var idx = pool[i].hay.indexOf(nq);
      if (idx >= 0) { pool[i]._r = idx; hits.push(pool[i]); }
    }
    hits.sort(function (a, b) { return a._r - b._r; });
    return hits.slice(0, 40);
  }

  function hl(text, nq) {
    if (!nq) return esc(text);
    var nt = norm(text), i = nt.indexOf(nq);
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + "<mark>" + esc(text.slice(i, i + nq.length)) + "</mark>" + esc(text.slice(i + nq.length));
  }

  function renderPalette() {
    var q = palInput.value, nq = norm(q);
    palItems = palResults(q);
    palSel = 0;
    palList.innerHTML = palItems.map(function (r, i) {
      return '<li class="ui-pal-item" role="option" data-i="' + i + '" aria-selected="' + (i === 0) + '">' +
        '<span class="ui-pal-kind">' + esc(r.kind) + '</span>' +
        '<span class="ui-pal-body"><span class="ui-pal-t">' + hl(r.t, nq) + '</span>' +
        '<span class="ui-pal-s">' + hl((r.s || "").slice(0, 150), nq) + '</span></span></li>';
    }).join("");
    palEmpty.classList.toggle("ui-hidden", palItems.length > 0);
  }

  function movePal(d) {
    if (!palItems.length) return;
    var nodes = palList.querySelectorAll(".ui-pal-item");
    nodes[palSel].setAttribute("aria-selected", "false");
    palSel = (palSel + d + palItems.length) % palItems.length;
    nodes[palSel].setAttribute("aria-selected", "true");
    nodes[palSel].scrollIntoView({ block: "nearest" });
  }
  function openPalItem(i) {
    var r = palItems[i];
    if (!r) return;
    closePalette();
    location.href = r.href;
  }
  function openPalette(seed) {
    if (!pal) buildPalette();
    palLastFocus = document.activeElement;
    pal.classList.add("open");
    document.documentElement.style.overflow = "hidden";
    palInput.value = seed || "";
    ensureCorpus(function () { if (pal.classList.contains("open")) renderPalette(); });
    renderPalette();
    palInput.focus();
    palInput.select();
  }
  function closePalette() {
    if (!pal) return;
    pal.classList.remove("open");
    document.documentElement.style.overflow = "";
    if (palLastFocus && palLastFocus.focus) palLastFocus.focus();
  }
  window.linalgPalette = openPalette;

  /* =================================================================
     4) ورقة الاختصارات — keyboard help
     ================================================================= */
  var helpBox = null;
  var SHORTCUTS = [
    ["Ctrl / ⌘ + K", "افتح لوحة الأوامر والبحث"],
    ["/", "ابحث فوراً"],
    ["←  →", "الدرس السابق / التالي"],
    ["J  K", "القسم التالي / السابق داخل الدرس"],
    ["G ثم H", "الرئيسية"],
    ["G ثم M", "الخارطة الذهنية"],
    ["G ثم R", "المراجعة المتباعدة"],
    ["G ثم S", "الملخص الشامل"],
    ["G ثم P", "مشغّل بايثون"],
    ["D", "تبديل الوضع الداكن"],
    ["?", "عرض هذه القائمة"]
  ];
  function toggleHelp(force) {
    if (!helpBox) {
      helpBox = el("div", "ui-help");
      helpBox.setAttribute("role", "dialog");
      helpBox.setAttribute("aria-modal", "true");
      helpBox.setAttribute("aria-label", "اختصارات لوحة المفاتيح");
      helpBox.innerHTML = '<div class="ui-help-box"><h2>اختصارات لوحة المفاتيح</h2>' +
        '<p>كل الاختصارات تعمل في أي صفحة من المقرر.</p>' +
        SHORTCUTS.map(function (s) {
          return '<div class="ui-help-row"><span>' + esc(s[1]) + '</span><span class="ui-key">' + esc(s[0]) + '</span></div>';
        }).join("") +
        '<div class="ui-help-row" style="justify-content:flex-end;border-top:0;padding-top:16px">' +
        '<button class="ui-btn" type="button" data-close style="font:inherit;font-size:12.5px;border:1.5px solid currentColor;' +
        'background:transparent;color:inherit;border-radius:999px;padding:8px 20px;cursor:pointer">إغلاق</button></div></div>';
      document.body.appendChild(helpBox);
      helpBox.addEventListener("click", function (e) {
        if (e.target === helpBox || (e.target.closest && e.target.closest("[data-close]"))) toggleHelp(false);
      });
    }
    var on = force == null ? !helpBox.classList.contains("open") : force;
    helpBox.classList.toggle("open", on);
  }

  /* =================================================================
     5) اختصارات لوحة المفاتيح — global keyboard shortcuts
     ================================================================= */
  function isTyping(t) {
    if (!t) return false;
    var tag = (t.tagName || "").toLowerCase();
    return tag === "input" || tag === "textarea" || tag === "select" || t.isContentEditable;
  }
  var gPending = 0;
  document.addEventListener("keydown", function (e) {
    var mod = e.metaKey || e.ctrlKey;
    if (mod && (e.key === "k" || e.key === "K")) { e.preventDefault(); openPalette(); return; }
    if (isTyping(e.target) || e.altKey || e.ctrlKey || e.metaKey) return;

    if (e.key === "Escape") { closePalette(); toggleHelp(false); return; }

    if (gPending && Date.now() - gPending < 1400) {
      gPending = 0;
      var go = { h: "index.html", m: "map.html", r: "review.html", s: "summary.html", p: "playground.html", f: "search.html" };
      var dest = go[e.key.toLowerCase()];
      if (dest) { e.preventDefault(); location.href = url(dest); return; }
    }
    switch (e.key) {
      case "/":  e.preventDefault(); openPalette(); break;
      case "?":  e.preventDefault(); toggleHelp(); break;
      case "g": case "G": gPending = Date.now(); break;
      case "d": case "D": {
        var tb = document.querySelector(".theme-btn");
        if (tb) { e.preventDefault(); tb.click(); }
        break;
      }
      case "ArrowLeft": case "ArrowRight": {
        if (!isLesson) break;
        /* RTL: السهم الأيسر يتقدّم، الأيمن يرجع */
        var fwd = e.key === "ArrowLeft";
        var n = lessonIdx + (fwd ? 1 : -1);
        if (n >= 0 && n < LESSONS.length) { e.preventDefault(); location.href = url("lessons/" + LESSONS[n].file); }
        break;
      }
      case "j": case "J": e.preventDefault(); jumpSection(1); break;
      case "k": case "K": e.preventDefault(); jumpSection(-1); break;
    }
  });

  function jumpSection(d) {
    var hs = [].slice.call(document.querySelectorAll("main h2, .wrap h2, section > h2, article > h2"));
    if (!hs.length) return;
    var y = window.scrollY + 90, target = null;
    if (d > 0) { for (var i = 0; i < hs.length; i++) if (hs[i].getBoundingClientRect().top + window.scrollY > y + 12) { target = hs[i]; break; } }
    else { for (var j = hs.length - 1; j >= 0; j--) if (hs[j].getBoundingClientRect().top + window.scrollY < y - 12) { target = hs[j]; break; } }
    if (target) target.scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "start" });
  }

  /* =================================================================
     6) الشريط العائم — back to top + palette launcher
     ================================================================= */
  function mountRail() {
    var rail = el("div", "ui-rail");
    rail.innerHTML =
      '<button type="button" data-act="search" aria-label="ابحث (اضغط / أو Ctrl+K)" title="ابحث — Ctrl/⌘+K">🔍</button>' +
      '<button type="button" data-act="top" aria-label="العودة إلى الأعلى" title="العودة إلى الأعلى">↑</button>';
    document.body.appendChild(rail);
    var btns = rail.querySelectorAll("button");
    rail.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button") : null;
      if (!b) return;
      if (b.getAttribute("data-act") === "top") window.scrollTo({ top: 0, behavior: reduceMotion() ? "auto" : "smooth" });
      else openPalette();
    });
    function sync() {
      var on = window.scrollY > 420;
      for (var i = 0; i < btns.length; i++) btns[i].classList.toggle("show", on);
    }
    addEventListener("scroll", sync, { passive: true });
    sync();
  }

  /* =================================================================
     7) فهرس الدرس الجانبي + شريط تقدّم القراءة
     ================================================================= */
  function mountLessonToc() {
    var heads = [].slice.call(document.querySelectorAll(".wrap > section > h2"));
    if (heads.length < 3) return;

    var box = el("div", "ui-toc ui-toc-rail");
    box.setAttribute("data-open", "true");
    var list = el("ul", "ui-toc-list");
    var items = [];

    heads.forEach(function (h, i) {
      var sec = h.parentElement;
      if (!sec.id) sec.id = "ui-sec-" + i;
      var clone = h.cloneNode(true);
      var sub = clone.querySelector(".en-sub"); if (sub) sub.remove();
      var numEl = clone.querySelector(".num");
      var numTxt = numEl ? numEl.textContent.trim() : String(i + 1);
      if (numEl) numEl.remove();
      var label = clone.textContent.replace(/\s+/g, " ").trim();

      var liNode = el("li");
      liNode.innerHTML = '<a href="#' + sec.id + '"><span class="ui-toc-n">' + esc(numTxt) + '</span>' +
                         '<span>' + esc(label) + '</span></a>';
      list.appendChild(liNode);
      items.push({ sec: sec, a: liNode.querySelector("a") });
    });

    var head = el("button", "ui-toc-head");
    head.type = "button";
    head.innerHTML = '<span>محتويات الدرس</span><span class="ui-toc-caret" aria-hidden="true">▾</span>';
    head.setAttribute("aria-expanded", "true");
    head.addEventListener("click", function () {
      var open = box.getAttribute("data-open") === "true";
      box.setAttribute("data-open", open ? "false" : "true");
      head.setAttribute("aria-expanded", open ? "false" : "true");
    });
    box.appendChild(head);
    box.appendChild(list);

    /* Desktop: floating rail. Mobile: inline right after the hero. */
    var hero = document.querySelector(".wrap > .hero") || document.querySelector(".wrap > header");
    if (hero && hero.parentNode) hero.parentNode.insertBefore(box, hero.nextSibling);
    else document.querySelector(".wrap").appendChild(box);

    function spy() {
      var y = window.scrollY + 120, cur = items[0];
      for (var i = 0; i < items.length; i++) {
        if (items[i].sec.getBoundingClientRect().top + window.scrollY <= y) cur = items[i];
      }
      items.forEach(function (it) {
        if (it === cur) it.a.setAttribute("aria-current", "true");
        else it.a.removeAttribute("aria-current");
      });
    }
    addEventListener("scroll", spy, { passive: true });
    spy();

    /* On narrow screens collapse by default to save space. */
    if (window.innerWidth < 1180) {
      box.classList.remove("ui-toc-rail");
      box.setAttribute("data-open", "false");
      head.setAttribute("aria-expanded", "false");
    }
    addEventListener("resize", function () {
      box.classList.toggle("ui-toc-rail", window.innerWidth >= 1180);
    });
  }

  function mountReadBar() {
    if (document.querySelector(".reading-progress-fill")) return; /* summary.html has its own */
    var bar = el("div", "ui-readbar");
    bar.innerHTML = "<i></i>";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
    var fill = bar.querySelector("i");
    function sync() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      fill.style.width = (h > 0 ? Math.min(100, Math.max(0, window.scrollY / h * 100)) : 0) + "%";
    }
    addEventListener("scroll", sync, { passive: true });
    addEventListener("resize", sync);
    sync();
  }

  /* =================================================================
     8) مسار التنقّل — breadcrumb inside lessons
     ================================================================= */
  var MODULES = { 1: "المحور 1 · المنظومات والمصفوفات", 2: "المحور 2 · الفضاءات والمتجهات", 3: "المحور 3 · الأساس والمحددات" };
  function mountCrumb() {
    var hero = document.querySelector(".wrap > .hero");
    if (!hero) return;
    var L = LESSONS[lessonIdx];
    var c = el("nav", "ui-crumb");
    c.setAttribute("aria-label", "مسار التنقّل");
    c.innerHTML =
      '<a href="' + url("index.html") + '">الرئيسية</a><span class="sep">›</span>' +
      '<a href="' + url("map.html") + '#n-l' + L.id + '">' + esc(MODULES[L.m]) + '</a><span class="sep">›</span>' +
      '<b>الدرس ' + L.id + '</b><span class="sep">·</span>' +
      '<span>' + (lessonIdx + 1) + ' من ' + LESSONS.length + '</span>';
    hero.parentNode.insertBefore(c, hero);
  }

  /* =================================================================
     9) تصحيح الاختبار وحفظ الدرجة — quiz scoring
     ================================================================= */
  function quizStore() { return read(K.quiz, {}) || {}; }

  function mountQuiz() {
    var quiz = document.getElementById("quiz");
    if (!quiz) return;
    var boxes = [].slice.call(quiz.querySelectorAll(".q"));
    if (!boxes.length) return;

    var answered = {}, correct = {};
    var card = el("div", "ui-score");
    card.setAttribute("data-state", "idle");
    card.setAttribute("aria-live", "polite");
    quiz.appendChild(card);

    var prev = quizStore()[lessonId];
    render();

    function render() {
      var n = boxes.length, a = Object.keys(answered).length, c = 0;
      for (var q in correct) if (correct[q]) c++;
      var pct = a ? Math.round(c / a * 100) : 0;
      var missing = boxes.filter(function (b) { return answered[b.id] && !correct[b.id]; })
                         .map(function (b, i) {
                            var p = b.querySelector(".prompt");
                            return p ? p.textContent.replace(/\s+/g, " ").trim().slice(0, 70) : b.id;
                         });

      var head, note;
      if (a === 0) {
        head = prev ? "آخر محاولة: " + prev.correct + " من " + prev.total : "لم تبدأ الاختبار بعد";
        note = prev
          ? "أجب مرة أخرى لتحديث درجتك — الاسترجاع النشط أقوى من إعادة القراءة."
          : "خمس أسئلة قصيرة. أجب أولاً من ذاكرتك، ثم اكشف — هذا هو الاسترجاع النشط.";
      } else if (a < n) {
        head = "أجبت " + a + " من " + n;
        note = "أكمل بقية الأسئلة لتُحتسب درجتك وتُحفظ في لوحة تقدّمك.";
      } else {
        head = "نتيجتك: " + c + " من " + n;
        note = c === n ? "إتقان كامل — انتقل إلى الدرس التالي بثقة."
             : c >= Math.ceil(n * 0.7) ? "جيد. راجع النقاط التي أخطأت فيها ثم أتمّ الدرس."
             : "أعد قراءة قسمي «القاعدة الذهبية» و«ماذا كسبت؟» ثم أعد الاختبار.";
      }

      card.style.setProperty("--pct", a ? pct : 0);
      card.setAttribute("data-state", a === n ? "done" : "idle");
      card.innerHTML =
        '<div class="ui-score-top">' +
          '<div class="ui-score-ring" aria-hidden="true"><span>' + (a ? pct + "%" : "—") + '</span></div>' +
          '<div class="ui-score-txt"><b>' + esc(head) + '</b><small>' + esc(note) + '</small></div>' +
        '</div>' +
        (missing.length ? '<div class="ui-score-miss"><b>يحتاج مراجعة:</b> ' + esc(missing.join(" · ")) + '</div>' : "") +
        '<div class="ui-score-acts">' +
          (a === n ? '<button class="ui-btn solid" type="button" data-act="retry">أعد الاختبار</button>' : "") +
          '<a class="ui-btn" href="' + url("review.html") + '#l' + lessonId + '">بطاقات المراجعة</a>' +
          '<a class="ui-btn" href="' + url("summary.html") + '#c' + lessonId + '">اقرأ الملخص</a>' +
          '<a class="ui-btn" href="' + url("map.html") + '#n-l' + lessonId + '">موضعه في الخارطة</a>' +
        '</div>';
    }

    card.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-act=retry]") : null;
      if (!b) return;
      location.hash = "#quiz";
      location.reload();
    });

    quiz.addEventListener("click", function (e) {
      var opt = e.target.closest ? e.target.closest(".opt") : null;
      if (!opt) return;
      var box = opt.closest(".q");
      if (!box || answered[box.id]) return;
      /* let the lesson's own handler paint ok/no first */
      setTimeout(function () {
        answered[box.id] = true;
        correct[box.id] = !opt.classList.contains("no");
        render();
        var n = boxes.length, a = Object.keys(answered).length;
        if (a === n) {
          var c = 0; for (var q in correct) if (correct[q]) c++;
          var store = quizStore();
          store[lessonId] = { correct: c, total: n, at: Date.now(), day: todayKey() };
          write(K.quiz, store);
          toast(c === n ? "درجة كاملة في الدرس " + lessonId + " ✓" : "حُفظت درجتك: " + c + " من " + n);
          if (typeof window.applyLinalgProgress === "function") window.applyLinalgProgress();
        }
      }, 0);
    });
  }

  /* =================================================================
     10) تابع من حيث توقفت + سلسلة الأيام
     ================================================================= */
  function trackResume() {
    if (!isLesson) return;
    var L = LESSONS[lessonIdx];
    var save = function () {
      write(K.resume, {
        id: L.id, title: L.t, href: "lessons/" + L.file,
        y: Math.round(window.scrollY), at: Date.now()
      });
    };
    var t = null;
    addEventListener("scroll", function () { clearTimeout(t); t = setTimeout(save, 700); }, { passive: true });
    addEventListener("beforeunload", save);
    save();

    /* mark as visited so the map can show "بدأته" */
    var seen = read(K.seen, {}) || {};
    if (!seen[L.id]) { seen[L.id] = Date.now(); write(K.seen, seen); }
  }

  function bumpStreak() {
    var s = read(K.streak, null) || { last: null, count: 0, best: 0, days: [] };
    var t = todayKey();
    if (s.last !== t) {
      var gap = s.last ? daysBetween(s.last, t) : 999;
      s.count = gap === 1 ? (s.count || 0) + 1 : 1;
      s.last = t;
      s.best = Math.max(s.best || 0, s.count);
      s.days = (s.days || []).concat(t).slice(-120);
      write(K.streak, s);
    }
    return s;
  }
  window.linalgStreak = function () { return read(K.streak, { count: 0, best: 0, days: [] }); };
  window.linalgQuiz = quizStore;
  window.linalgLessons = LESSONS;
  window.linalgRoot = ROOT;

  function mountResumeBanner() {
    var host = document.getElementById("resumeSlot");
    if (!host) return;
    var r = read(K.resume, null);
    var done = read(K.done, {}) || {};
    var next = null;
    for (var i = 0; i < LESSONS.length; i++) if (!done[LESSONS[i].id]) { next = LESSONS[i]; break; }

    if (!r && !next) return;
    if (r && done[r.id] && next) r = null; /* finished it — point forward instead */

    var target = r ? r : { id: next.id, title: next.t, href: "lessons/" + next.file };
    var label  = r ? "تابع من حيث توقفت" : "ابدأ من هنا";
    var sub    = r ? "الدرس " + r.id + " — " + r.title : "الدرس " + next.id + " — " + next.t;

    var banner = el("div", "ui-resume");
    banner.innerHTML =
      '<div class="t"><b>' + esc(label) + '</b><small>' + esc(sub) + '</small></div>' +
      '<a href="' + url(target.href) + '">' + (r ? "أكمل الدرس ←" : "افتح الدرس ←") + '</a>' +
      '<button class="dismiss" type="button" aria-label="إخفاء">✕</button>';
    host.appendChild(banner);
    banner.querySelector(".dismiss").addEventListener("click", function () { banner.remove(); });
  }

  /* =================================================================
     11) boot
     ================================================================= */
  function boot() {
    bumpStreak();
    mountRail();
    mountReadBar();
    mountResumeBanner();
    if (isLesson) {
      mountCrumb();
      mountLessonToc();
      mountQuiz();
      trackResume();
    }
    if (location.hash === "#quiz") {
      var q = document.getElementById("quiz");
      if (q) setTimeout(function () { q.scrollIntoView({ behavior: "auto", block: "start" }); }, 60);
    }
    document.dispatchEvent(new CustomEvent("linalg:ui-ready"));
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
