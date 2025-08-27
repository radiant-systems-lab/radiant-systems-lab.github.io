---
layout: page
---

<style>
  .page-wrap { display: grid; grid-template-columns: 220px 1fr; gap: 1.5rem; }
  @media (max-width: 900px){ .page-wrap { grid-template-columns: 1fr; } .sidebar { position: static; } }
  .sidebar {
    position: sticky; top: 1rem; align-self: start; background:#fff; border:1px solid #eee;
    border-radius: 12px; padding: 1rem;
  }
  .sidebar h3 { margin:0 0 .5rem; font-size: 0.95rem; color:#555; letter-spacing:.02em; }
  .year-nav { list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:.35rem; }
  .year-nav a {
    display:block; padding:.5rem .65rem; border-radius: 8px; text-decoration:none; color:#111;
  }
  .year-nav a:hover { background:#f5f5f5; }
  .year-nav a.active { background:#FBBF24; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .content { background:#fff; border:1px solid #eee; border-radius:12px; padding:1.25rem; }
  .year-header { margin-top:0; font-size:1.75rem; }
  .course-list { margin:.5rem 0 0; padding-left:1.25rem; }
  .course-list a { color:#000; text-decoration:none; }
  .course-list a:hover { text-decoration:underline; }
</style>

<div class="page-wrap">
  <!-- Sidebar: Years -->
  <aside class="sidebar" aria-label="Year navigation">
    <h3>Years</h3>
    <nav>
      <ul class="year-nav">
        <!-- Add/remove years as needed -->
        <li><a href="#y2025" class="active">2025</a></li>
        <li><a href="#y2024">2024</a></li>
        <li><a href="#y2023">2023</a></li>
      </ul>
    </nav>
  </aside>

  <!-- Content: Only the requested course under header 2025 -->
  <main class="content">
    <section id="y2025" aria-labelledby="y2025-title">
      <h1 class="year-header" id="y2025-title">2025</h1>
      <ul class="course-list">
        <li>
          <a href="https://radiant-systems-lab.github.io/softwares/flexiflow/">CSC/EE 8001</a>
        </li>
      </ul>
    </section>
  </main>
</div>

<script>
  // Highlight current year in sidebar based on hash or visible section (future friendly)
  const links = document.querySelectorAll('.year-nav a');
  function setActive(targetId){
    links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${targetId}`));
  }
  if (location.hash) setActive(location.hash.replace('#',''));

  // Optional: observe sections if you add more years later
  const sections = document.querySelectorAll('main section[id]');
  if ('IntersectionObserver' in window && sections.length > 0){
    const io = new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { rootMargin: "-40% 0px -50% 0px", threshold: 0 });
    sections.forEach(s=>io.observe(s));
  }
</script>
