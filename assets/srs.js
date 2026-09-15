/* ===================================================================
   محرّك المراجعة المتباعدة — Spaced Repetition (SM-2)
   مختبر الجبر الخطي

   خوارزمية SuperMemo-2 بأربع درجات على طريقة Anki:
     0 أعدها  · 1 صعبة · 2 جيدة · 3 سهلة
   كل بطاقة تحمل: معامل السهولة EF، عدد التكرارات، الفاصل بالأيام،
   وتاريخ الاستحقاق. كل شيء محلي في localStorage — بلا خادم.
   =================================================================== */
(function (root) {
  "use strict";

  var KEY = "linalg:srs";
  var LOG = "linalg:srs-log";
  var DAY = 86400000;

  function read(k, fb) {
    try { var v = JSON.parse(localStorage.getItem(k)); return v === null ? fb : v; }
    catch (e) { return fb; }
  }
  function write(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }

  function startOfDay(ts) { var d = new Date(ts); d.setHours(0, 0, 0, 0); return d.getTime(); }
  function todayKey(ts) {
    var d = new Date(ts == null ? Date.now() : ts);
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  }

  function all() { return read(KEY, {}) || {}; }
  function save(s) { return write(KEY, s); }

  function card(id) {
    var s = all();
    return s[id] || { ef: 2.5, reps: 0, interval: 0, due: 0, lapses: 0, last: 0 };
  }

  /* حالة البطاقة: جديدة / مستحقّة / مجدولة */
  function state(id, now) {
    now = now || Date.now();
    var c = all()[id];
    if (!c || !c.reps && !c.last) return "new";
    if (c.due <= now) return "due";
    return "later";
  }

  /* الدرجات الأربع → جودة SM-2 */
  var Q = [2, 3, 4, 5];

  function grade(id, g, now) {
    now = now || Date.now();
    var s = all();
    var c = s[id] || { ef: 2.5, reps: 0, interval: 0, due: 0, lapses: 0, last: 0 };
    var q = Q[Math.max(0, Math.min(3, g))];

    if (q < 3) {
      /* نسيتها: تعود إلى البداية وتُعاد في نفس الجلسة */
      c.lapses = (c.lapses || 0) + 1;
      c.reps = 0;
      c.interval = 0;
      c.due = now;                       /* مستحقّة فوراً — تُعاد في هذه الجلسة */
    } else {
      /* البطاقة الجديدة: نفرّق بين الدرجات من أول مرة بدل أن تعطي كلها «غداً» */
      if (c.reps === 0) c.interval = (q === 3 ? 1 : (q === 4 ? 2 : 4));
      else if (c.reps === 1) c.interval = (q === 3 ? 3 : (q === 4 ? 6 : 9));
      else {
        var mult = q === 3 ? 1.2 : (q === 4 ? c.ef : c.ef * 1.3);
        c.interval = Math.max(1, Math.round(c.interval * mult));
      }
      c.reps += 1;
      /* تُستحق عند بداية اليوم رقم interval من اليوم — بلا إزاحة يوم إضافي */
      c.due = startOfDay(now) + c.interval * DAY;
    }

    /* تحديث معامل السهولة (SM-2) */
    c.ef = Math.max(1.3, Math.min(3.0, c.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))));
    c.last = now;
    s[id] = c;
    save(s);

    /* سجل يومي للإحصاءات */
    var log = read(LOG, {}) || {};
    var t = todayKey(now);
    log[t] = log[t] || { n: 0, ok: 0 };
    log[t].n += 1;
    if (q >= 3) log[t].ok += 1;
    var keys = Object.keys(log).sort();
    while (keys.length > 180) { delete log[keys.shift()]; }
    write(LOG, log);

    return c;
  }

  /* بناء طابور الجلسة: المستحق أولاً (الأقدم استحقاقاً)، ثم الجديد */
  function queue(deck, opts) {
    opts = opts || {};
    var now = opts.now || Date.now();
    var maxNew = opts.maxNew == null ? 8 : opts.maxNew;
    var maxTotal = opts.maxTotal == null ? 30 : opts.maxTotal;
    var s = all();
    var due = [], fresh = [];

    deck.forEach(function (cd) {
      var c = s[cd.id];
      if (!c) { fresh.push(cd); return; }
      if (c.due <= now) due.push({ cd: cd, due: c.due });
    });
    due.sort(function (a, b) { return a.due - b.due; });

    var out = due.map(function (x) { return x.cd; });
    out = out.concat(fresh.slice(0, maxNew));
    return out.slice(0, maxTotal);
  }

  function stats(deck, now) {
    now = now || Date.now();
    var s = all();
    var st = { total: deck.length, fresh: 0, due: 0, later: 0, learned: 0, mature: 0, byLesson: {} };
    deck.forEach(function (cd) {
      var c = s[cd.id];
      var bucket;
      if (!c) { st.fresh++; bucket = "fresh"; }
      else if (c.due <= now) { st.due++; bucket = "due"; }
      else { st.later++; bucket = "later"; }
      if (c && c.reps > 0) st.learned++;
      if (c && c.interval >= 21) st.mature++;
      var L = cd.lesson || "—";
      st.byLesson[L] = st.byLesson[L] || { total: 0, fresh: 0, due: 0, later: 0 };
      st.byLesson[L].total++;
      st.byLesson[L][bucket]++;
    });
    return st;
  }

  /* رسالة عربية لموعد المراجعة القادم */
  function nextLabel(id, now) {
    now = now || Date.now();
    var c = all()[id];
    if (!c || !c.last) return "جديدة";
    var d = Math.round((c.due - startOfDay(now)) / DAY);
    if (d <= 0) return "الآن";
    if (d === 1) return "غداً";
    if (d === 2) return "بعد يومين";
    if (d < 11) return "بعد " + d + " أيام";
    if (d < 30) return "بعد " + d + " يوماً";
    var mo = Math.round(d / 30);
    return mo === 1 ? "بعد شهر" : (mo === 2 ? "بعد شهرين" : "بعد " + mo + " أشهر");
  }

  /* تنبؤ بفواصل الأزرار الأربعة قبل الضغط */
  function preview(id) {
    var base = card(id);
    return [0, 1, 2, 3].map(function (g) {
      var c = { ef: base.ef, reps: base.reps, interval: base.interval };
      var q = Q[g];
      if (q < 3) return "الآن";
      var i;
      if (c.reps === 0) i = (q === 3 ? 1 : (q === 4 ? 2 : 4));
      else if (c.reps === 1) i = (q === 3 ? 3 : (q === 4 ? 6 : 9));
      else i = Math.max(1, Math.round(c.interval * (q === 3 ? 1.2 : (q === 4 ? c.ef : c.ef * 1.3))));
      if (i === 1) return "غداً";
      if (i === 2) return "بعد يومين";
      if (i < 11) return "بعد " + i + " أيام";
      if (i < 30) return "بعد " + i + " يوماً";
      var mo = Math.round(i / 30);
      return mo + (mo === 1 ? " شهر" : " أشهر");
    });
  }

  function history(days) {
    var log = read(LOG, {}) || {};
    var out = [];
    for (var i = (days || 30) - 1; i >= 0; i--) {
      var t = todayKey(Date.now() - i * DAY);
      out.push({ day: t, n: (log[t] || {}).n || 0, ok: (log[t] || {}).ok || 0 });
    }
    return out;
  }

  function reset() { write(KEY, {}); write(LOG, {}); }

  /* بناء مجموعة البطاقات من بيانات البحث المشتركة */
  function buildDeck(data) {
    var deck = [];
    (data || []).forEach(function (les) {
      (les.entries || []).forEach(function (e) {
        if (e.type === "term") {
          deck.push({
            id: "t:" + les.id + ":" + e.title,
            kind: "term",
            lesson: les.id,
            lessonTitle: les.title,
            q: e.title,
            en: e.en || "",
            a: e.text || "",
            url: les.url + (e.anchor || "#glossary")
          });
        } else if (e.type === "lesson") {
          deck.push({
            id: "r:" + les.id,
            kind: "rule",
            lesson: les.id,
            lessonTitle: les.title,
            q: "ما القاعدة الذهبية لدرس «" + les.title + "»؟",
            en: "",
            a: e.text || "",
            url: les.url
          });
        }
      });
    });
    return deck;
  }

  root.LinalgSRS = {
    KEY: KEY, all: all, card: card, state: state, grade: grade,
    queue: queue, stats: stats, nextLabel: nextLabel, preview: preview,
    history: history, reset: reset, buildDeck: buildDeck, todayKey: todayKey
  };
})(window);
