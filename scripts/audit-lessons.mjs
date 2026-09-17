#!/usr/bin/env node
/* audit-lessons.mjs — بوابة جودة الدروس، بلا متصفح وبلا نموذج لغوي.
 *
 * تحوّل الحكم البشري المكلف إلى فحص آلي مجاني. كل فحص هنا وُلد من عيب
 * حقيقي وُجد في درس فعلي، لا من تخمين.
 *
 *   node scripts/audit-lessons.mjs                 كل الدروس
 *   node scripts/audit-lessons.mjs 0012 0017       دروس بعينها
 *   node scripts/audit-lessons.mjs --errors-only   الأخطاء القاطعة فقط
 *   node scripts/audit-lessons.mjs --only bidi     فئة واحدة
 *   node scripts/audit-lessons.mjs --json          مخرج JSON للأدوات
 *
 * المخرجات نوعان:
 *   ERROR — عيب موضوعي، يجب إصلاحه.
 *   hint  — مؤشر عمق، تحكم أنت: هل ينقص الدرس هذا فعلاً؟
 *
 * الخروج بـ 1 إن وُجد ERROR واحد على الأقل.
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const LESSONS = join(ROOT, "lessons");

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const optVal = (n) => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const ONLY = optVal("--only");
const ERRORS_ONLY = flag("--errors-only");
const AS_JSON = flag("--json");
const ids = args.filter((a) => /^\d{4}$/.test(a));

/* ------------------------------------------------------------------ */
/* أدوات صغيرة على نص HTML — لا نحتاج محلّلاً كاملاً                   */

const stripTags = (h) => h.replace(/<(script|style)[\s\S]*?<\/\1>/g, " ").replace(/<[^>]+>/g, " ");
const section = (html, id) => {
  const i = html.indexOf(`id="${id}"`);
  if (i < 0) return "";
  const start = html.lastIndexOf("<", i);
  const end = html.indexOf("</section>", i);
  return end < 0 ? html.slice(start) : html.slice(start, end);
};
const inlineScript = (html) => {
  const m = html.match(/<script>\n\(function\(\)\{[\s\S]*?\n\}\)\(\);\n<\/script>/);
  return m ? m[0] : "";
};

/* ------------------------------------------------------------------ */
/* الفحوص                                                              */

const CHECKS = [
  {
    id: "bidi",
    level: "ERROR",
    why: "رقم أو صيغة خارج span.coord داخل نص عربي — سيُعرض مقلوباً",
    run(L) {
      const body = L.html.slice(L.html.indexOf("<body"));
      const prose = body
        .replace(/<(script|style|canvas)[\s\S]*?<\/\1>/g, " ")
        .replace(/<span class="coord">[\s\S]*?<\/span>/g, " ")
        .replace(/<bdi[\s\S]*?<\/bdi>/g, " ")
        .replace(/<code[\s\S]*?<\/code>/g, " ")
        /* الحاويات اللاتينية سياقها LTR، فالأرقام فيها لا تنقلب */
        .replace(/<span class="en[- ][^"]*"[\s\S]*?<\/span>/g, " ")
        .replace(/<[^>]*(?:lang="en"|dir="ltr")[^>]*>[\s\S]*?<\/[a-z]+>/g, " ")
        .replace(/<[^>]+>/g, " ");
      const hits = [];
      /* رقمان بينهما فاصل أو شرطة داخل جملة عربية: أخطر حالة للقلب */
      const re = /[؀-ۿ][^.!؟\n]{0,40}?(\d+\s*[-–,،]\s*\d+)/g;
      let m;
      while ((m = re.exec(prose)) && hits.length < 4) hits.push(m[1].trim());
      return hits.map((h) => `نطاق رقمي غير معزول: «${h}»`);
    },
  },
  {
    id: "worked-example",
    level: "hint",
    why: "لا مثال محسوب بالأرقام يستطيع المتعلم إعادته على ورقة",
    run: (L) => (/<pre[\s>]/.test(L.html) ? [] : ["أضف <pre> فيه العملية سطراً سطراً"]),
  },
  {
    id: "prediction",
    level: "hint",
    why: "لا سؤال توقّع قبل الكشف — الاسترجاع النشط يبدأ بالتوقّع",
    run: (L) => (/توقّع|توقع قبل/.test(L.text) ? [] : ["أضف بطاقة «توقّع قبل أن تجرّب» ثم أجب عنها"]),
  },
  {
    id: "glossary",
    level: "ERROR",
    why: "قاموس الدرس ناقص (عربي · English · معنى مبسّط)",
    run(L) {
      const g = section(L.html, "glossary");
      if (!g) return ["لا قسم glossary"];
      const rows = (g.match(/<tr>/g) || []).length - 1;
      return rows >= 2 ? [] : [`صفوف القاموس ${rows} — المطلوب مصطلحان على الأقل`];
    },
  },
  {
    id: "gain",
    level: "ERROR",
    why: "لا قسم «ماذا كسبت؟» بصيغة قبل/بعد",
    run: (L) => (section(L.html, "gain") ? [] : ["لا قسم gain"]),
  },
  {
    id: "golden-rule",
    level: "ERROR",
    why: "لا بطاقة card idea تحمل القاعدة الذهبية",
    run: (L) => (/class="card idea"/.test(L.html) ? [] : ["لا بطاقة card idea"]),
  },
  {
    id: "quiz",
    level: "ERROR",
    why: "الاختبار الختامي ناقص",
    run(L) {
      const n = (L.html.match(/class="q" id="q\d+"/g) || []).length;
      return n >= 3 ? [] : [`أسئلة الاختبار ${n} — المطلوب ثلاثة على الأقل`];
    },
  },
  {
    id: "quiz-answers",
    level: "ERROR",
    why: "سؤال بلا إجابة صحيحة واحدة في جدول ANS",
    run(L) {
      const js = inlineScript(L.html);
      const qs = [...L.html.matchAll(/class="q" id="(q\d+)"/g)].map((m) => m[1]);
      const out = [];
      for (const q of qs) {
        const m = js.match(new RegExp(`${q}\\s*:\\s*\\{([\\s\\S]*?)\\}\\s*(,\\s*q\\d+\\s*:|\\}\\s*;)`));
        if (!m) { out.push(`${q}: لا مدخل في ANS`); continue; }
        const trues = (m[1].match(/,\s*true\s*\]/g) || []).length;
        if (trues !== 1) out.push(`${q}: عدد الإجابات الصحيحة ${trues}`);
      }
      return out;
    },
  },
  {
    id: "practice",
    level: "ERROR",
    why: "لا ملف تمرين مقابل، أو لا حل له",
    run(L) {
      const out = [];
      if (!existsSync(join(ROOT, "practice", L.slug + ".py"))) out.push(`practice/${L.slug}.py مفقود`);
      if (!existsSync(join(ROOT, "practice", "solutions", L.slug + ".py")))
        out.push(`practice/solutions/${L.slug}.py مفقود`);
      return out;
    },
  },
  {
    id: "fn-named",
    level: "hint",
    why: "دالة يطلبها التمرين ولا يسمّيها الدرس — يصل المتعلم بلا قاعدة",
    run(L) {
      const f = join(ROOT, "practice", L.slug + ".py");
      if (!existsSync(f)) return [];
      const names = [...readFileSync(f, "utf8").matchAll(/^def (\w+)\(/gm)]
        .map((m) => m[1])
        .filter((n) => !n.startsWith("_"));
      const missing = names.filter((n) => {
        const bare = n.replace(/_/g, " ");
        return !L.html.includes(n) && !L.text.includes(bare);
      });
      return missing.length ? [`غير مذكورة في الدرس: ${missing.join(", ")}`] : [];
    },
  },
  {
    id: "figure",
    level: "hint",
    why: "لا لوحة رسم — المفهوم المكاني يحتاج صورة لا وصفاً",
    run: (L) => (/<canvas/.test(L.html) ? [] : ["فكّر في لوحة تشرح المفهوم"]),
  },
  {
    id: "figure-core",
    level: "ERROR",
    why: "لوحة رسم بلا assets/figure.js — ستبقى ضبابية ولن تتبع الوضع الداكن",
    run: (L) => (!/<canvas/.test(L.html) || /assets\/figure\.js/.test(L.html) ? [] : ["حمّل assets/figure.js قبل سكربت الدرس"]),
  },
  {
    id: "panel-variety",
    level: "hint",
    why: "لوحات الدرس ببصمة واحدة — ضغط زر يبدّل العنوان فوق الرسم نفسه",
    run(L) {
      const demos = (L.html.match(/class="demo"/g) || []).length;
      if (demos < 3) return [];
      const modes = new Set();
      if (/type="range"/.test(L.html)) modes.add("منزلق");
      if (/<select/.test(L.html)) modes.add("اختيار");
      if (/type="number"/.test(L.html)) modes.add("إدخال رقمي");
      if (/<canvas/.test(L.html)) modes.add("لوحة");
      return modes.size >= 3 ? [] : [`${demos} لوحات بـ${modes.size} قاعدة تفاعل: ${[...modes].join("، ")}`];
    },
  },
  {
    id: "emoji",
    level: "ERROR",
    why: "إيموجي في متن الدرس — الوسم النصي أوضح وأثبت عبر الأنظمة",
    run(L) {
      const body = stripTags(L.html.slice(L.html.indexOf("<body")));
      const hits = body.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu);
      return hits ? [`إيموجي: ${[...new Set(hits)].join(" ")}`] : [];
    },
  },
  {
    id: "meta",
    level: "ERROR",
    why: "وسوم الصفحة الأساسية ناقصة",
    run(L) {
      const out = [];
      if (!/data-lesson-id="\d{4}"/.test(L.html)) out.push("data-lesson-id مفقود");
      if (!/<link rel="canonical"/.test(L.html)) out.push("canonical مفقود");
      if (!/name="description"/.test(L.html)) out.push("description مفقود");
      if (!/application\/ld\+json/.test(L.html)) out.push("بيانات JSON-LD مفقودة");
      return out;
    },
  },
  {
    id: "wiring",
    level: "ERROR",
    why: "الدرس غير مربوط بمنظومة الموقع",
    run(L) {
      const out = [];
      const files = {
        "assets/graph-data.js": `"${L.id}": "${L.slug}"`,
        "index.html": `lessons/${L.slug}.html`,
        "review.html": `id="l${L.id}"`,
        "summary.html": `id="c${L.id}"`,
        "playground.html": `value="${L.slug}"`,
        "sitemap.xml": `lessons/${L.slug}.html`,
        "sw.js": `lessons/${L.slug}.html`,
      };
      for (const [f, needle] of Object.entries(files)) {
        const p = join(ROOT, f);
        if (existsSync(p) && !readFileSync(p, "utf8").includes(needle)) out.push(`غير مذكور في ${f}`);
      }
      return out;
    },
  },
];

/* ------------------------------------------------------------------ */

const files = readdirSync(LESSONS)
  .filter((f) => f.endsWith(".html"))
  .filter((f) => !ids.length || ids.includes(f.slice(0, 4)))
  .sort();

const report = [];
let errors = 0, hints = 0;

for (const f of files) {
  const html = readFileSync(join(LESSONS, f), "utf8");
  const L = { id: f.slice(0, 4), slug: f.replace(/\.html$/, ""), html, text: stripTags(html) };
  const findings = [];
  for (const c of CHECKS) {
    if (ONLY && c.id !== ONLY) continue;
    if (ERRORS_ONLY && c.level !== "ERROR") continue;
    for (const msg of c.run(L)) {
      findings.push({ check: c.id, level: c.level, msg, why: c.why });
      c.level === "ERROR" ? errors++ : hints++;
    }
  }
  report.push({ lesson: L.id, slug: L.slug, findings });
}

if (AS_JSON) {
  console.log(JSON.stringify({ errors, hints, report }, null, 1));
} else {
  for (const r of report) {
    if (!r.findings.length) { console.log(`\x1b[32m✓\x1b[0m ${r.lesson}  ${r.slug}`); continue; }
    console.log(`\x1b[1m•\x1b[0m ${r.lesson}  ${r.slug}`);
    for (const f of r.findings) {
      const tag = f.level === "ERROR" ? "\x1b[31mERROR\x1b[0m" : "\x1b[33mhint \x1b[0m";
      console.log(`    ${tag} ${f.check.padEnd(15)} ${f.msg}`);
    }
  }
  console.log(`\nالدروس: ${report.length} · ERROR: ${errors} · hint: ${hints}`);
}

process.exit(errors ? 1 : 0);
