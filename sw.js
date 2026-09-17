/* Offline cache for مختبر الجبر الخطي. Bump CACHE to force refresh. */
const CACHE = "linalg-v7";

/* Precached on install: the shell every page needs. */
const CORE = [
  "./",
  "./index.html",
  "./map.html",
  "./summary.html",
  "./review.html",
  "./search.html",
  "./playground.html",
  "./404.html",
  "./manifest.webmanifest",
  "./assets/lesson-fonts.css",
  "./assets/lesson.css",
  "./assets/ui.css",
  "./assets/site.js",
  "./assets/ui.js",
  "./assets/srs.js",
  "./assets/figure.js",
  "./assets/graph-data.js",
  "./assets/search-data.js",
  "./assets/exercises.js",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./lessons/0001-linear-systems.html",
  "./lessons/0002-matrices-inverse.html",
  "./lessons/0003-gaussian-elimination.html",
  "./lessons/0004-matrix-properties.html",
  "./lessons/0005-euclidean-spaces.html",
  "./lessons/0006-subspaces.html",
  "./lessons/0007-linear-combinations.html",
  "./lessons/0008-span-independence.html",
  "./lessons/0009-basis-dimension.html",
  "./lessons/0010-determinants.html",
  "./lessons/0011-drills.html",
  "./lessons/0012-rank.html",
  "./lessons/0013-linear-mappings.html",
  "./lessons/0014-transformation-matrix.html",
  "./lessons/0015-affine-spaces.html",
  "./lessons/0016-norms-inner-products.html",
  "./lessons/0017-orthogonality.html",
  "./lessons/0018-gram-schmidt.html",
  "./lessons/0019-projections-rotations.html",
  "./assets/fonts/thmanyahsans-Black.woff2",
  "./assets/fonts/thmanyahsans-Bold.woff2",
  "./assets/fonts/thmanyahsans-Medium.woff2",
  "./assets/fonts/thmanyahsans-Regular.woff2",
  "./assets/fonts/thmanyahserifdisplay-Black.woff2",
  "./assets/fonts/thmanyahserifdisplay-Bold.woff2",
  "./assets/fonts/thmanyahserifdisplay-Medium.woff2",
  "./assets/fonts/thmanyahserifdisplay-Regular.woff2",
  "./assets/fonts/thmanyahseriftext-Bold.woff2",
  "./assets/fonts/thmanyahseriftext-Medium.woff2",
  "./assets/fonts/thmanyahseriftext-Regular.woff2"
];

/* Third-party origins worth keeping offline. KaTeX renders every formula in
   the course: without it the lessons fall back to raw TeX, so it is cached on
   first successful load instead of being skipped as "cross-origin". */
const CDN_HOSTS = ["cdn.jsdelivr.net"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      /* One bad URL must not fail the whole install, so add them one by one. */
      .then((c) => Promise.all(CORE.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === location.origin;
  const cdn = CDN_HOSTS.indexOf(url.hostname) !== -1;
  if (!sameOrigin && !cdn) return;

  /* Range requests (video seeking) must reach the network untouched: a cached
     200 answer to a Range request makes Safari refuse to play the file. */
  if (req.headers.has("range")) return;

  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) {
        /* Cached CDN assets refresh quietly in the background. */
        if (cdn) fetch(req).then((res) => {
          if (res && (res.ok || res.type === "opaque")) {
            caches.open(CACHE).then((c) => c.put(req, res.clone())).catch(() => {});
          }
        }).catch(() => {});
        return hit;
      }
      return fetch(req).then((res) => {
        const keep = res && (res.ok || res.type === "opaque") &&
          (cdn || req.destination === "video" || req.destination === "" ||
           /\.(html|css|js|woff2|png|jpg|mp4|srt|vtt|webmanifest|xml)$/.test(url.pathname));
        if (keep) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      }).catch(() =>
        req.mode === "navigate"
          ? caches.match("./404.html").then((p) => p || caches.match("./index.html"))
          : undefined
      );
    })
  );
});
