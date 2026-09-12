/* Offline cache for مختبر الجبر الخطي. Bump CACHE to force refresh. */
const CACHE = "linalg-v1";
const CORE = [
  "./",
  "./index.html",
  "./review.html",
  "./search.html",
  "./playground.html",
  "./manifest.webmanifest",
  "./assets/lesson-fonts.css",
  "./assets/lesson.css",
  "./assets/site.js",
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

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
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
  if (url.origin !== location.origin) return;
  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req).then((res) => {
        if (res && res.ok && (req.destination === "video" || req.destination === "" ||
            /\.(html|css|js|woff2|png|mp4|srt|webmanifest)$/.test(url.pathname))) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      }).catch(() => (req.mode === "navigate" ? caches.match("./index.html") : undefined));
    })
  );
});
