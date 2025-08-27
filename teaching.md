---
layout: page
---

<style>
  .page-wrap { display:grid; grid-template-columns:220px 1fr; gap:1.5rem }
  @media (max-width: 900px){ .page-wrap { grid-template-columns:1fr } .sidebar{ position:static } }
  .sidebar{ position:sticky; top:1rem; align-self:start; background:#fff; border:1px solid #eee; border-radius:12px; padding:1rem }
  .sidebar h3{ margin:0 0 .5rem; font-size:.95rem; color:#555 }
  .year-nav{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:.35rem }
  .year-nav a{ display:block; padding:.5rem .65rem; border-radius:8px; text-decoration:none; color:#111 }
  .year-nav a:hover{ background:#f5f5f5 }
  .year-nav a.active{ background:#FBBF24; box-shadow:0 2px 8px rgba(0,0,0,.08) }
  .content{ background:#fff; border:1px solid #eee; border-radius:12px; padding:1.25rem }
  .year-header{ margin-top:0; font-size:1.75rem }
  .course-list{ margin:.5rem 0 0; padding-left:1.25rem }
  .course-list a{ color:#000; text-decoration:none }
  .course-list a:hover{ text-decoration:underline }
  html{ scroll-behavior:smooth }
</style>

<div class="page-wrap">
  <aside class="sidebar" aria-label="Year navigation">
    <h3>Years</h3>
    <nav>
      <ul class="year-nav">
        <li><a href="#y2027">2027</a></li>
        <li><a href="#y2026">2026</a></li>
        <li><a href="#y2025" class="active">2025</a></li>
        <li><a href="#y2024">2024</a></li>
        <li><a href="#y2023">2023</a></li>
      </ul>
    </nav>
  </aside>

  <main class="content">
    <section id="y2025" aria-labelledby="y2025-title">
      <h1 class="year-header" id="y2025-title">2025</h1>
      <ul class="course-list">
        <!-- Link to your internal course subpage -->
        <li><a href="/courses/csc-ee-8001/">CSC/EE 8001</a></li>
      </ul>
    </section>

    <!-- Optional placeholders so sidebar jumps work now -->
    <section id="y2026"><h2>2026</h2></section>
    <section id="y2027"><h2>2027</h2></section>
    <section id="y2024"><h2>2024</h2></section>
    <section id="y2023"><h2>2023</h2></section>
  </main>
</div>

<script>
  const links = document.querySelectorAll('.year-nav a');
  function setActive(id){ links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${id}`)); }
  if (location.hash) setActive(location.hash.substring(1));
  const sections = document.querySelectorAll('main section[id]');
  if ('IntersectionObserver' in window){
    const io = new IntersectionObserver(es=>{
      es.forEach(e=>{ if(e.isIntersecting) setActive(e.target.id); });
    },{ rootMargin:"-40% 0px -50% 0px" });
    sections.forEach(s=>io.observe(s));
  }
</script>
