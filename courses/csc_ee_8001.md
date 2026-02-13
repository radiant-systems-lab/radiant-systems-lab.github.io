---
layout: page
---

<div class="page-course">
  <div class="course-layout">
    <aside class="course-sidebar" aria-label="Section navigation">
      <h3><i class="fa-solid fa-book-open-reader"></i> CSC/EE 8001</h3>
      <nav>
        <ul class="course-section-nav" id="secNav">
          <span class="slider" id="courseSlider" aria-hidden="true"></span>
          <li><a href="#announcements">Announcements</a></li>
          <li><a href="#content">Course Goals</a></li>
          <li><a href="#schedule">Schedule</a></li>
          <li><a href="#exams">Exams</a></li>
          <li><a href="#grades">Grades</a></li>
          <li><a href="#rules">Rules</a></li>
        </ul>
      </nav>
    </aside>

    <main class="course-main" id="mainContent">
      <div class="course-crumb">
        <a href="/teaching.html#y2025"><i class="fa-solid fa-arrow-left"></i> Back to 2025</a>
      </div>

      <h1 class="course-page-title">CSC/EE 8001: Designing End-to-End ML Systems</h1>

      <div class="course-meta">
        <p><strong><i class="fa-regular fa-clock"></i> Lectures:</strong> Wednesday noon-2:50PM in Naka 222</p>
        <p><strong><i class="fa-solid fa-user-tie"></i> Instructor:</strong> <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Tanu Malik</a></p>
        <p><strong><i class="fa-regular fa-envelope"></i> Email:</strong> tanu [at] missouri.edu</p>
        <p><strong><i class="fa-solid fa-door-open"></i> Office Hours:</strong> Tuesday 5:00PM-6:00PM CT @ Naka 311</p>
      </div>

      <section id="announcements" class="course-section" aria-labelledby="announcements-title">
        <h2 id="announcements-title"><i class="fa-solid fa-bullhorn"></i> Announcements</h2>
        <ul class="news-list">
          <li><strong>[2025-08-29]</strong> Assignment 1 released on Canvas; see due date under Schedule.</li>
          <li><strong>[2025-08-26]</strong> Office hours: Tuesday 5:00PM-6:00PM Naka 311. Please also send email if you plan to meet on Zoom.</li>
        </ul>
      </section>

      <section id="content" class="course-section" aria-labelledby="content-title">
        <h2 id="content-title"><i class="fa-solid fa-diagram-project"></i> Course Goals</h2>
        <p>
          This is a research-based course on systems for machine learning (ML), at the intersection of ML/AI, data management, and systems.
          Students will learn about the landscape and evolution of ML systems and current research. Topics include scalable model-building systems,
          data sourcing and preparation, ML platforms, deployment concerns, and MLOps. A major component is a project focused on MLOps and research paper reviews.
          The course is currently for MS and PhD students.
        </p>
      </section>

      <section id="schedule" class="course-section" aria-labelledby="schedule-title">
        <h2 id="schedule-title"><i class="fa-regular fa-calendar-days"></i> Schedule</h2>
        <div class="table-wrap">
          <table class="schedule-table" aria-describedby="schedule-caption">
            <thead>
              <tr>
                <th scope="col">Date</th>
                <th scope="col">Details</th>
                <th scope="col">PDFs</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><time datetime="2025-08-27">Aug 27, 2025</time></td>
                <td>Machine Learning (ML) and ML systems overview</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2025-09-03">Sep 03, 2025</time></td>
                <td>Loss functions, Gradient Descent, Bias-Variance, and ML development cycle</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2025-09-10">Sep 10, 2025</time></td>
                <td>Neural Networks and large-scale ML systems</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2025-09-17">Sep 17, 2025</time></td>
                <td>Cloud Computing and DevOps for ML</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2025-09-24">Sep 24, 2025</time></td>
                <td>Data Selection</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2025-10-01">Oct 1, 2025</time></td>
                <td>Model performance and model evaluation</td>
                <td>&mdash;</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="exams" class="course-section" aria-labelledby="exams-title">
        <h2 id="exams-title"><i class="fa-regular fa-pen-to-square"></i> Exams</h2>
        <p></p>
      </section>

      <section id="grades" class="course-section" aria-labelledby="grades-title">
        <h2 id="grades-title"><i class="fa-solid fa-scale-balanced"></i> Grades</h2>
        <p></p>
      </section>

      <section id="rules" class="course-section" aria-labelledby="rules-title">
        <h2 id="rules-title"><i class="fa-solid fa-gavel"></i> Rules</h2>
        <p></p>
      </section>
    </main>
  </div>
</div>

<script>
(() => {
  const nav = document.getElementById("secNav");
  const slider = document.getElementById("courseSlider");
  if (!nav || !slider) return;

  const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
  const sections = links
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  function setActiveById(id) {
    links.forEach((a) => {
      const isActive = a.getAttribute("href") === `#${id}`;
      a.classList.toggle("active", isActive);
      a.setAttribute("aria-current", isActive ? "true" : "false");
    });

    const active = links.find((a) => a.classList.contains("active"));
    if (!active) return;

    const activeRect = active.getBoundingClientRect();
    const navRect = nav.getBoundingClientRect();
    const offsetY = activeRect.top - navRect.top + nav.scrollTop - 2;
    slider.style.transform = `translateY(${offsetY}px)`;
    slider.style.height = `${activeRect.height}px`;
    slider.style.opacity = "0.96";
    active.scrollIntoView({ block: "nearest" });
  }

  let ioLocked = false;
  let lockTimeout = null;
  function lockIO(ms = 600) {
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
      lockIO();
    });
  });

  const io = new IntersectionObserver(
    (entries) => {
      if (ioLocked) return;
      const vh = window.innerHeight || document.documentElement.clientHeight;
      let best = null;
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const top = entry.target.getBoundingClientRect().top;
        const penalty = top > 0.6 * vh ? 100000 : 0;
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
