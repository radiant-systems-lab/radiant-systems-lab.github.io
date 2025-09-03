---
layout: page
---

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

  :root { --pill:#FBBF24; --bd:#eee; --fg:#111; }

  body { font-family: 'Roboto', sans-serif; }

  .page-wrap { display:grid; grid-template-columns:220px 1fr; gap:1.5rem }
  @media (max-width: 900px){ .page-wrap { grid-template-columns:1fr } .sidebar{ position:static } }

  /* Sidebar */
  .sidebar{
    position:sticky; top:1rem; align-self:start; background:#fff;
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
    transform:translateY(0); transition:transform .25s ease, opacity .2s ease; opacity:0;
    z-index:0;
  }

  /* Content */
  .content{ 
    background:#fff; 
    border-radius:12px; 
    padding:1.25rem; 
    line-height:1.6; 
    font-size:1rem;   /* base size for body */
  }
  
  .course-title{ 
    margin-top:0; 
    font-size:2rem; 
    font-weight:700; 
  }
  
  .content h2{ 
    font-size:1.5rem; 
    font-weight:600; 
    margin-top:2rem; 
    margin-bottom:1rem; 
  }
  
  .content p, 
  .content li{ 
    font-size:1rem; 
  }
  
  .content .crumb{ 
    margin-bottom:1rem; 
    font-size:.95rem; 
  }
  
  .content table{ 
    font-size:.95rem; 
  }

  /* Sections */
  section[id]{ scroll-margin-top:90px; }
  .course-sec{ padding-bottom:2rem; margin-top:1.25rem; }

  /* News list */
  .news-list{ margin:.5rem 0 0 1.25rem; }
  .news-list li{ margin:.25rem 0; }

  /* Schedule table */
  .table-wrap{ overflow-x:auto; }
  table.schedule-table{ width:100%; border-collapse:collapse; margin-top:.5rem; }
  .schedule-table th, .schedule-table td{ padding:.65rem .75rem; text-align:left; vertical-align:top; border:none; }
  .schedule-table thead th{ background:#f8f8f8; font-weight:600; }
  .schedule-table tbody tr:nth-child(even){ background:#fcfcfc; }

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
    <h1 class="course-title">CSC/EE 8001: Designing End-to-End ML Systems</h1>

   

    <p><b>Lectures</b>: Wednesday noon-2:50PM in Naka 222</p>
<p><b>Instructor:</b> <a href="https://engineering.missouri.edu/faculty/tanu-malik/"><b>Tanu Malik</b></a></p>
<ul>
<li><p>Email: tanu [at] missouri.edu</p>
</li>
<li><p>Office Hours: Tuesday 5-6pm CT @ Naka 311</p>
</li>
</ul>

    <!-- NEWS: bullet list template -->
    <section id="news" class="course-sec" aria-labelledby="news-title">
      <h2 id="news-title">Announcements</h2>
      <ul class="news-list">
        <!-- Add Content Here -->
        <li><strong>[2025-08-29]</strong> Assignment 1 released on Canvas; see due date under Schedule.</li>
        <li><strong>[2025-08-26]</strong> Office hours: Tuesday 5:00PM-6:00PM Naka 311. Please additionally send me email if you plan to meet on Zoom. </li>
      </ul>
    </section>

    <section id="content" class="course-sec" aria-labelledby="content-title">
      <h2 id="content-title">Course Goals</h2>
      <p>This is a research-based course on systems for machine learning (ML), 
and lies at the intersection of the fields of ML/AI, data management, and systems.  Students will learn about the landscape 
and evolution of ML systems and the latest research. This course will cover key systems topics including systems for 
scalable ML model building, data sourcing and preparation for ML, 
ML platforms, and issues in ML deployment and MLOps.  
A major component of this course is a course project on MLOps and reviewing research papers on these topics.
The course is currently for MS students and PhD students.</p>
<p></p>
    </section>

    <!-- SCHEDULE: table template -->
    <section id="schedule" class="course-sec" aria-labelledby="schedule-title">
      <h2 id="schedule-title">Schedule</h2>
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
            <!-- Eit these rows as needed -->
            <tr>
              <td><time datetime="2025-08-27">Aug 27, 2025</time></td>
              <td>Machine Learning (ML) &amp; ML systems overview</td>
              <td>—</td>
            </tr>
            <tr>
              <td><time datetime="2025-09-03">Sep 03, 2025</time></td>
              <td>Loss functions, Gradient Descent, Bias-Variance,
ML development cycle</td>
              <td>-</td>
            </tr>
            <tr>
              <td><time datetime="2025-09-10">Sep 10, 2025</time></td>
              <td>Neural Networks and Large scale ML systems</td>
              <td>—</td>
            </tr>
                 <tr>
              <td><time datetime="2025-09-10">Sep 17, 2025</time></td>
              <td>Cloud Computing and DevOps for ML</td>
              <td>—</td>
            </tr>
                 <tr>
              <td><time datetime="2025-09-10">Sep 24, 2025</time></td>
              <td>Data Selection</td>
              <td>—</td>
            </tr>
            <tr>
              <td><time datetime="2025-10-01">Oct 1, 2025</time></td>
              <td>Model Performance and Model Evaluation/</td>
              <td>—</td>
            </tr>
          </tbody>
        </table>
      </div>
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
  const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);

  function setActiveById(id){
    links.forEach(a => {
      const isActive = a.getAttribute('href') === `#${id}`;
      a.classList.toggle('active', isActive);
      a.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
    const active = links.find(a => a.classList.contains('active'));
    if (active){
      const liRect = active.getBoundingClientRect();
      const listRect = nav.getBoundingClientRect();
      const offsetY = liRect.top - listRect.top + nav.scrollTop - 4;
      slider.style.transform = `translateY(${offsetY}px)`;
      slider.style.height = `${liRect.height}px`;
      active.scrollIntoView({ block: 'nearest' });
      slider.style.opacity = '0.95';
    }
  }

  // Lock IO during programmatic scrolls to avoid flicker
  let ioLocked = false;
  let lockTimeout = null;
  function lockIO(ms = 600){
    ioLocked = true;
    clearTimeout(lockTimeout);
    lockTimeout = setTimeout(() => ioLocked = false, ms);
  }

  links.forEach(a => {
    a.addEventListener('click', () => {
      const id = a.getAttribute('href').substring(1);
      setActiveById(id);
      lockIO();
    });
  });

  const io = new IntersectionObserver((entries) => {
    if (ioLocked) return;
    const vh = window.innerHeight || document.documentElement.clientHeight;
    let best = null;
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      const top = en.target.getBoundingClientRect().top;
      const penalty = top > 0.6 * vh ? 1e5 : 0;
      const score = Math.abs(top) + penalty;
      if (!best || score < best.score) best = { id: en.target.id, score };
    });
    if (best) setActiveById(best.id);
  }, { root: null, threshold: [0, .25, .5, .75, 1], rootMargin: "-15% 0px -60% 0px" });

  sections.forEach(sec => io.observe(sec));

  function initActive(){
    const fromHash = location.hash && sections.find(s => s.id === location.hash.substring(1));
    const initial = fromHash || sections[0];
    setActiveById(initial.id);
  }
  window.addEventListener('hashchange', () => {
    const id = location.hash.substring(1);
    if (id) { setActiveById(id); lockIO(400); }
  });

  const ro = new ResizeObserver(() => {
    const active = document.querySelector('.sec-nav a.active');
    if (active) setActiveById(active.getAttribute('href').substring(1));
  });
  ro.observe(nav);

  if ('onscrollend' in window) {
    window.addEventListener('scrollend', () => { ioLocked = false; });
  }
  ['wheel','touchmove','keydown'].forEach(evt => {
    window.addEventListener(evt, () => { if (ioLocked) lockIO(150); }, { passive: true });
  });

  initActive();
</script>
