---
layout: page
---

<style>
  :root { --pill:#FBBF24; --bd:#eee; --fg:#111; }

  .page-wrap { display:grid; grid-template-columns:220px 1fr; gap:1.5rem }
  @media (max-width: 900px){ .page-wrap { grid-template-columns:1fr } .sidebar{ position:static } }

  /* Sidebar */
  .sidebar{
    position:sticky; top:1rem; align-self:start; background:#fff; border:1px solid var(--bd);
    border-radius:12px; padding:.75rem; overflow:hidden;
  }
  .sidebar h3{ margin:.25rem .5rem .5rem; font-size:.95rem; color:#555 }
  .sec-nav{
    position:relative; list-style:none; margin:0; padding:.25rem; display:flex; flex-direction:column; gap:.35rem;
    max-height:70vh; overflow:auto; scroll-behavior:smooth;
  }
  .sec-nav a{
    position:relative; display:block; padding:.55rem .7rem; border-radius:8px; text-decoration:none; color:var(--fg);
    z-index:1;
  }
  .sec-nav a:hover{ background:#f6f6f6 }
  .sec-nav a.active{ color:#000 }

  /* Sliding indicator behind active link */
  .slider{
    position:absolute; left:.25rem; right:.25rem; height:38px; background:var(--pill);
    border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.08);
    transform:translateY(0); transition:transform .25s ease, opacity .2s ease; opacity:.95;
    z-index:0;
    opacity:0;
  }

  /* Content */
  .content{ background:#fff; border:1px solid var(--bd); border-radius:12px; padding:1.25rem }
  .course-title{ margin-top:0; font-size:1.9rem }
  .crumb{ margin-bottom:1rem; }
  .crumb a{ text-decoration:none; color:#555 }
  .crumb a:hover{ text-decoration:underline; }

  /* Sections */
  section[id]{ scroll-margin-top:90px; }
  .course-sec{ min-height:55vh; padding-bottom:2rem; border-top:1px dashed #eee; margin-top:1.25rem; }

  html{ scroll-behavior:smooth }
</style>

<div class="page-wrap">
  <!-- Left sidebar: in-page section nav -->
  <aside class="sidebar" aria-label="Section navigation">
    <h3>CSC/EE 8001</h3>
    <nav>
      <ul class="sec-nav" id="secNav">
        <div class="slider" id="slider" aria-hidden="true"></div>
        <li><a href="#news">News</a></li>
        <li><a href="#content">Content</a></li>
        <li><a href="#schedule">Schedule</a></li>
        <li><a href="#exams">Exams</a></li>
        <li><a href="#grades">Grades</a></li>
        <li><a href="#rules">Rules</a></li>
      </ul>
    </nav>
  </aside>

  <!-- Main area -->
  <main class="content" id="mainContent">
    <div class="crumb">← <a href="https://radiant-systems-lab.github.io/teaching.html#y2025">Back to 2025</a></div>
    <h1 class="course-title">CSC/EE 8001 — Designing End-to-End ML System</h1>

    <section id="news" class="course-sec" aria-labelledby="news-title">
      <h2 id="news-title">News</h2>
      <p><!-- add news items --></p>
    </section>

    <section id="content" class="course-sec" aria-labelledby="content-title">
      <h2 id="content-title">Content</h2>
      <p><!-- readings, slides, links --></p>
    </section>

    <section id="schedule" class="course-sec" aria-labelledby="schedule-title">
      <h2 id="schedule-title">Schedule</h2>
      <p><!-- calendar, week-by-week --></p>
    </section>

    <section id="exams" class="course-sec" aria-labelledby="exams-title">
      <h2 id="exams-title">Exams</h2>
      <p><!-- midterm/final info --></p>
    </section>

    <section id="grades" class="course-sec" aria-labelledby="grades-title">
      <h2 id="grades-title">Grades</h2>
      <p><!-- grading breakdown/policies --></p>
    </section>

    <section id="rules" class="course-sec" aria-labelledby="rules-title">
      <h2 id="rules-title">Rules</h2>
      <p><!-- attendance, late policy, integrity --></p>
    </section>
  </main>
</div>

<script>
  const nav = document.getElementById('secNav');
  const slider = document.getElementById('slider');
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const sections = links
    .map(a => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

  function setActiveById(id){
    links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${id}`));
    const active = links.find(a => a.classList.contains('active'));
    if (active){
      const liRect = active.getBoundingClientRect();
      const listRect = nav.getBoundingClientRect();
      const offsetY = liRect.top - listRect.top + nav.scrollTop - 4;
      slider.style.transform = `translateY(${offsetY}px)`;
      slider.style.height = `${liRect.height}px`;
      active.scrollIntoView({ block: 'nearest' });
    }
  }

  links.forEach(a => {
    a.addEventListener('click', () => {
      const id = a.getAttribute('href').substring(1);
      setActiveById(id);
    });
  });

  const io = new IntersectionObserver((entries) => {
    let top = null;
    entries.forEach(en => {
      if (en.isIntersecting) {
        if (!top || en.intersectionRatio > top.intersectionRatio) top = en;
      }
    });
    if (top) setActiveById(top.target.id);
  }, {
    root: null,
    threshold: [0.25, 0.5, 0.75],
    rootMargin: "-20% 0px -55% 0px"
  });
  sections.forEach(sec => io.observe(sec));

  function initActive(){
    const fromHash = location.hash && sections.find(s => s.id === location.hash.substring(1));
    const initial = fromHash || sections[0];
    setActiveById(initial.id);
  }
  window.addEventListener('hashchange', () => {
    const id = location.hash.substring(1);
    if (id) setActiveById(id);
  });

  const ro = new ResizeObserver(() => {
    const active = document.querySelector('.sec-nav a.active');
    if (active){
      const id = active.getAttribute('href').substring(1);
      setActiveById(id);
    }
  });
  ro.observe(nav);

  initActive();
</script>
