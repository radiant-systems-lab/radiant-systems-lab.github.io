---
layout: page
---

<div class="page-teaching">
  <div class="page-hero">
    <h2><i class="fa-solid fa-chalkboard-user"></i> Teaching</h2>
    <div class="quick-jump-links">
      <a href="#y2025">2025</a>
    </div>
  </div>

  <div class="teaching-layout">
    <aside class="teaching-sidebar" aria-label="Year navigation">
      <h3><i class="fa-regular fa-calendar"></i> Years</h3>
      <nav>
        <ul class="teaching-year-nav" id="yearNav">
          <span class="slider" id="yearSlider" aria-hidden="true"></span>
          <li><a href="#y2025">2025</a></li>
        </ul>
      </nav>
    </aside>

    <main class="teaching-main" id="mainContent">
      <section id="y2025" class="teaching-year-block" aria-labelledby="y2025-title">
        <h1 class="teaching-year-header" id="y2025-title">2025</h1>

        <article class="teaching-course-card">
          <h3 class="teaching-course-title">
            <a href="/courses/csc_ee_8001.html">CSC/EE 8001: End-to-End ML Systems</a>
          </h3>
          <p class="teaching-course-desc">
            Machine learning systems are both complex and unique. Complex because they must balance both performance and accuracy.
            Unique because they are data-dependent, with data varying widely across use cases. This course covers ML foundations,
            then dives into data and hypothesis selection, model performance and evaluation, deployment, diagnostics, and MLOps issues
            in large pipelines. The course is project-based and includes state-of-the-art paper discussions.
          </p>
        </article>
      </section>
    </main>
  </div>
</div>

<script>
(() => {
  const nav = document.getElementById("yearNav");
  const slider = document.getElementById("yearSlider");
  if (!nav || !slider) return;

  const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
  const sections = links
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  function keepLinkVisibleInsideNav(linkEl) {
    if (!linkEl) return;
    const top = linkEl.offsetTop;
    const bottom = top + linkEl.offsetHeight;
    const viewTop = nav.scrollTop;
    const viewBottom = viewTop + nav.clientHeight;

    if (top < viewTop) {
      nav.scrollTop = Math.max(0, top - 6);
    } else if (bottom > viewBottom) {
      nav.scrollTop = bottom - nav.clientHeight + 6;
    }
  }

  function setActiveById(id) {
    links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === `#${id}`));
    const active = links.find((a) => a.classList.contains("active"));
    if (!active) return;

    const activeRect = active.getBoundingClientRect();
    const navRect = nav.getBoundingClientRect();
    const offsetY = activeRect.top - navRect.top + nav.scrollTop - 2;
    slider.style.transform = `translateY(${offsetY}px)`;
    slider.style.height = `${activeRect.height}px`;
    keepLinkVisibleInsideNav(active);
  }

  let ioLocked = false;
  let lockTimeout = null;
  function lockIO(ms = 500) {
    ioLocked = true;
    clearTimeout(lockTimeout);
    lockTimeout = setTimeout(() => {
      ioLocked = false;
    }, ms);
  }

  links.forEach((a) => {
    a.addEventListener("click", () => {
      const id = a.getAttribute("href").slice(1);
      setActiveById(id);
      lockIO(600);
    });
  });

  const io = new IntersectionObserver(
    (entries) => {
      if (ioLocked) return;
      const viewportH = window.innerHeight || document.documentElement.clientHeight;
      let best = null;
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const top = entry.target.getBoundingClientRect().top;
        const penalty = top > 0.6 * viewportH ? 100000 : 0;
        const score = Math.abs(top) + penalty;
        if (!best || score < best.score) best = { id: entry.target.id, score };
      });
      if (best) setActiveById(best.id);
    },
    { root: null, threshold: [0, 0.25, 0.5, 0.75, 1], rootMargin: "-15% 0px -60% 0px" }
  );

  sections.forEach((section) => io.observe(section));

  function initActive() {
    const fromHash = location.hash && sections.find((s) => s.id === location.hash.slice(1));
    const initial = fromHash || sections[0];
    if (initial) setActiveById(initial.id);
  }

  window.addEventListener("hashchange", () => {
    const id = location.hash.slice(1);
    if (!id) return;
    setActiveById(id);
    lockIO(400);
  });

  const ro = new ResizeObserver(() => {
    const active = nav.querySelector("a.active");
    if (!active) return;
    setActiveById(active.getAttribute("href").slice(1));
  });
  ro.observe(nav);

  initActive();
})();
</script>
