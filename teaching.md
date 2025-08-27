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
  .year-nav{
    position:relative; list-style:none; margin:0; padding:.25rem; display:flex; flex-direction:column; gap:.35rem;
    max-height:70vh; overflow:auto; scroll-behavior:smooth;
  }
  .year-nav a{
    position:relative; display:block; padding:.55rem .7rem; border-radius:8px; text-decoration:none; color:var(--fg);
    z-index:1; /* above slider */
  }
  .year-nav a:hover{ background:#f6f6f6 }
  .year-nav a.active{ color:#000 }

  /* Sliding indicator behind active link */
  .slider{
    position:absolute; left:.25rem; right:.25rem; height:38px; background:var(--pill);
    border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.08);
    transform:translateY(0); transition:transform .25s ease, opacity .2s ease; opacity:.95;
    z-index:0;
  }

  /* Content */
  .content{ background:#fff; border:1px solid var(--bd); border-radius:12px; padding:1.25rem }
  .year-header{ margin-top:0; font-size:1.75rem }
  .course-list{ margin:.5rem 0 0; padding-left:1.25rem }
  .course-list a{ color:#000; text-decoration:none }
  .course-list a:hover{ text-decoration:underline }

  /* Ensure anchor scrolling clears sticky headers */
  section[id]{ scroll-margin-top:90px; }

  /* Make sections tall enough to test scroll/spy */
  .year-block{ min-height:70vh; padding-bottom:2rem; border-top:1px dashed #eee; margin-top:1.5rem; }
  html{ scroll-behavior:smooth }
</style>

<div class="page-wrap">
  <!-- Sidebar -->
  <aside class="sidebar" aria-label="Year navigation">
    <h3>Years</h3>
    <nav>
      <ul class="year-nav" id="yearNav">
        <div class="slider" id="slider" aria-hidden="true"></div>
        <li><a href="#y2025">2025</a></li>
        <li><a href="#y2024">2024</a></li>
        <li><a href="#y2023">2023</a></li>
      </ul>
    </nav>
  </aside>

  <!-- Main -->
  <main class="content" id="mainContent">
    <section id="y2025" class="year-block" aria-labelledby="y2025-title">
      <h1 class="year-header" id="y2025-title">2025</h1>
      <ul class="course-list">
        <li><a href="/courses/csc-ee-8001/">CSC/EE 8001</a></li>
      </ul>
    </section>

    <section id="y2024" class="year-block" aria-labelledby="y2024-title">
      <h1 class="year-header" id="y2024-title">2024</h1>
      <ul class="course-list"><li><em>Placeholder</em></li></ul>
    </section>

    <section id="y2023" class="year-block" aria-labelledby="y2023-title">
      <h1 class="year-header" id="y2023-title">2023</h1>
      <ul class="course-list"><li><em>Placeholder</em></li></ul>
    </section>
  </main>
</div>

<script>
  const nav = document.getElementById('yearNav');
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
      const offsetY = liRect.top - listRect.top + nav.scrollTop - 4; // -4 to center better
      slider.style.transform = `translateY(${offsetY}px)`;
      slider.style.height = `${liRect.height}px`;

      active.scrollIntoView({ block: 'nearest' });
    }
  }

  links.forEach(a => {
    a.addEventListener('click', (e) => {
      // Allow default smooth scroll, just set active early
      const id = a.getAttribute('href').substring(1);
      setActiveById(id);
    });
  });

  const io = new IntersectionObserver((entries) => {
    // Pick the most visible entry
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
    const active = document.querySelector('.year-nav a.active');
    if (active){
      const id = active.getAttribute('href').substring(1);
      setActiveById(id);
    }
  });
  ro.observe(nav);

  initActive();
</script>
