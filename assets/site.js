/* Shared behaviours: dark theme, unified progress, service worker. */
(function () {
  "use strict";
  var THEME_KEY = "linalg:theme";
  var DONE_KEY = "linalg:done";
  var IDS = ["0001","0002","0003","0004","0005","0006","0007","0008","0009","0010","0011"];

  function read(key, fb) {
    try { var v = JSON.parse(localStorage.getItem(key)); return v === null ? fb : v; }
    catch (e) { return fb; }
  }
  function write(key, v) {
    try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {}
  }

  /* ---------- theme ---------- */
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    var en = (document.documentElement.lang || "ar").indexOf("en") === 0;
    var btns = document.querySelectorAll(".theme-btn");
    for (var i = 0; i < btns.length; i++) {
      btns[i].textContent = t === "dark" ? (en ? "Light mode" : "الوضع الفاتح")
                                          : (en ? "Dark mode" : "الوضع الداكن");
      btns[i].setAttribute("aria-pressed", t === "dark" ? "true" : "false");
    }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", t === "dark" ? "#14130f" : "#faf7f2");
  }
  window.applyLinalgLabels = function () { applyTheme(theme); };
  var theme = read(THEME_KEY, null);
  if (!theme) {
    theme = (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }
  applyTheme(theme);

  /* ---------- progress ---------- */
  function doneObj() { return read(DONE_KEY, {}) || {}; }
  function syncDone() {
    var d = doneObj();
    var btns = document.querySelectorAll(".done-toggle");
    for (var i = 0; i < btns.length; i++) {
      var on = !!d[btns[i].getAttribute("data-lesson")];
      btns[i].setAttribute("aria-pressed", on ? "true" : "false");
      btns[i].classList.toggle("is-done", on);
      btns[i].textContent = on ? "✓ أتممت الدرس" : "أتممت الدرس";
    }
    var cards = document.querySelectorAll("[data-card-done]");
    for (var j = 0; j < cards.length; j++) {
      cards[j].classList.toggle("is-done", !!d[cards[j].getAttribute("data-card-done")]);
    }
    var n = 0;
    for (var k = 0; k < IDS.length; k++) if (d[IDS[k]]) n++;
    var fill = document.getElementById("progFill");
    var text = document.getElementById("progText");
    if (fill) fill.style.width = (n / IDS.length * 100) + "%";
    if (text) {
      var en = (document.documentElement.lang || "ar").indexOf("en") === 0;
      text.textContent = en
        ? (n === IDS.length ? "Course complete — well done" : "Completed " + n + " of " + IDS.length)
        : (n === IDS.length ? "أكملت المسار كله — أحسنت" : "أكملت " + n + " من " + IDS.length);
    }
  }
  window.applyLinalgProgress = syncDone;

  /* ---------- shared click handler ---------- */
  document.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target.closest(".theme-btn") : null;
    if (t) {
      theme = theme === "dark" ? "light" : "dark";
      write(THEME_KEY, theme);
      applyTheme(theme);
      return;
    }
    var b = e.target.closest ? e.target.closest(".done-toggle") : null;
    if (b) {
      var id = b.getAttribute("data-lesson");
      var d = doneObj();
      if (d[id]) delete d[id]; else d[id] = 1;
      write(DONE_KEY, d);
      syncDone();
    }
  });

  window.addEventListener("storage", function (e) {
    if (!e.key || e.key === DONE_KEY || e.key === "linalg:done") syncDone();
    if (e.key === THEME_KEY) { theme = read(THEME_KEY, theme); applyTheme(theme); }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", syncDone);
  } else {
    syncDone();
  }

  /* ---------- service worker ---------- */
  if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
    var here = (document.currentScript && document.currentScript.src) || "";
    var root = here.replace(/assets\/site\.js.*$/, "");
    navigator.serviceWorker.register(root + "sw.js", { scope: root }).catch(function () {});
  }
})();
