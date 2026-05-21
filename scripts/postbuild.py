from pathlib import Path

WEB_DIR = Path("build/web")
INDEX = WEB_DIR / "index.html"

html = INDEX.read_text(encoding="utf-8")

html = html.replace(
    '<link rel="icon" type="image/png" href="favicon.png" sizes="16x16">',
    '<link rel="icon" type="image/png" href="favicon.png" sizes="16x16">\n'
    '    <link rel="manifest" href="manifest.webmanifest">\n'
    '    <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">\n'
    '    <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">',
)

old_canvas_css = """        canvas.emscripten {
            border: 0px none;
            background-color: transparent;
            width: 100%;
            height: 100%;
            z-index: 5;

            padding: 0;
            margin: 0 auto;

            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
        }

        body {
            font-family: arial;
            margin: 0;
            padding: none;
            background-color:powderblue;
        }"""

new_canvas_css = """        :root {
            color-scheme: light dark;
            --page-bg: #ffffff;
            --game-w: min(480px, 100vw, calc(100vh * 0.75));
            --game-h: min(640px, 100vh, calc(100vw * 1.333333));
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --page-bg: #000000;
            }
        }

        html,
        body {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        canvas.emscripten {
            border: 0px none;
            background-color: transparent;
            width: var(--game-w);
            height: var(--game-h);
            z-index: 5;

            padding: 0;
            margin: auto;

            position: fixed;
            inset: 0;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }

        body {
            font-family: arial;
            margin: 0;
            padding: 0;
            background-color: var(--page-bg);
        }"""

html = html.replace(old_canvas_css, new_canvas_css)

old_infobox = """    // Center in viewport
    const left = (window.innerWidth - w) / 2;
    const top = (window.innerHeight - h) / 2;"""

new_infobox = """    // Center in viewport
    const left = (window.innerWidth - w) / 2;
    const top = (window.innerHeight - h) / 2;"""

html = html.replace(old_infobox, new_infobox)

registration = """    <script>
        if ("serviceWorker" in navigator) {
            window.addEventListener("load", () => {
                navigator.serviceWorker.register("sw.js").catch(console.warn);
            });
        }
    </script>
</body>"""

html = html.replace("</body>", registration)

INDEX.write_text(html, encoding="utf-8")

(WEB_DIR / "manifest.webmanifest").write_text(
    """{
  "name": "Car Mini Game",
  "short_name": "Car Mini",
  "description": "Retro racing game built with Python and Pygame.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "favicon.png",
      "sizes": "96x96",
      "type": "image/png"
    }
  ]
}
""",
    encoding="utf-8",
)

(WEB_DIR / "sw.js").write_text(
    """const CACHE_NAME = "car-mini-game-v1";
const CORE_ASSETS = [
  "/",
  "/index.html",
  "/favicon.png",
  "/manifest.webmanifest",
  "/game_car.tar.gz",
  "/game_car.apk",
  "https://pygame-web.github.io/cdn/0.9.3/pythons.js",
  "https://pygame-web.github.io/cdn/0.9.3/browserfs.min.js"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      Promise.allSettled(CORE_ASSETS.map((asset) => cache.add(asset)))
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;

      return fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match("/index.html"));
    })
  );
});
""",
    encoding="utf-8",
)
