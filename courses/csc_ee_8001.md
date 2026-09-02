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
          <li><a href="#prerequisites">Prerequisites</a></li>
          <li><a href="#schedule">Schedule</a></li>
          <li><a href="#labs">Class Labs</a></li>
          <li><a href="#project">Project</a></li>
          <li><a href="#exams">Exams</a></li>
          <li><a href="#grades">Grades</a></li>
          <li><a href="#rules">Rules</a></li>
        </ul>
      </nav>
    </aside>

    <main class="course-main" id="mainContent">
      <div class="course-crumb">
        <a href="/teaching.html#y2026"><i class="fa-solid fa-arrow-left"></i> Back to Teaching</a>
      </div>

      <h1 class="course-page-title">CSC/EE 8001: Designing End-to-End ML Systems</h1>

      <div class="course-meta">
        <p><strong><i class="fa-regular fa-clock"></i> Lectures:</strong> Wednesday noon-2:50PM in Naka 222</p>
        <p><strong><i class="fa-solid fa-user-tie"></i> Instructor:</strong> <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Tanu Malik</a></p>
        <p><strong><i class="fa-regular fa-envelope"></i> Email:</strong> tanu@missouri.edu</p>
        <p><strong><i class="fa-solid fa-door-open"></i> Office Hours:</strong> Tuesday 5:00PM-6:00PM CT @ Naka 311</p>
      </div>

      <section id="announcements" class="course-section" aria-labelledby="announcements-title">
        <h2 id="announcements-title"><i class="fa-solid fa-bullhorn"></i> Announcements</h2>
        <ul class="news-list">
          <li><strong>[2026-09-02]</strong> Labs 1&ndash;3 (Hello + Cloud) are due September 6.</li>
          <li><strong>[2026-08-26]</strong> Welcome to Designing End-to-End ML Systems! The <a href="/Miz-E2EML-SyllabusF26.pdf">Fall 2026 syllabus</a> and course schedule are now available.</li>
        </ul>
      </section>

      <section id="content" class="course-section" aria-labelledby="content-title">
        <h2 id="content-title"><i class="fa-solid fa-diagram-project"></i> Course Goals</h2>
        <p>
          The objective is to transition students from &ldquo;using models&rdquo; to &ldquo;engineering systems.&rdquo; By the end,
          students will have built a complete end-to-end ML pipeline and optimized it for real-world deployment constraints.
        </p>
        <ul>
          <li>Comprehend the need for Machine Learning Systems and why ML system is beyond the model.</li>
          <li>Trace the end-to-end ML pipeline from data to deployment. Identify throughput, I/O, memory allocations, FLOPs bottlenecks at each pipeline stage.</li>
          <li>Experiment with batching strategies for inference (static, dynamic, continuous). Calculate the throughput-latency tradeoff for a given SLA.</li>
          <li>Quantify the impact of data quality and quantization on model performance</li>
          <li>Comprehend model drift (data drift, concept drift) and explain why it matters for production systems. Design a monitoring pipeline that detects drift before accuracy degrades.</li>
        </ul>
      </section>

      <section id="prerequisites" class="course-section" aria-labelledby="prerequisites-title">
        <h2 id="prerequisites-title"><i class="fa-solid fa-list-check"></i> Prerequisites</h2>
        <p>
          If you are not sure that you have satisfied the prerequisites, speak to the instructor before the second lecture.
          Prerequisite courses and experience include:
        </p>
        <ul>
          <li>This is a programming heavy course. Expertise with Python is a must. Significant expertise in handling infrastructure, debugging, and being able to learn at an abstract level.</li>
          <li>Familiarity with basic probability theory and linear algebra.</li>
          <li>Student must have taken some introduction class on data science or be willing to take it along with the course.</li>
        </ul>
      </section>

      <section id="schedule" class="course-section" aria-labelledby="schedule-title">
        <h2 id="schedule-title"><i class="fa-regular fa-calendar-days"></i> Schedule</h2>
        <div class="table-wrap">
          <table class="schedule-table">
            <thead>
              <tr>
                <th scope="col">Dates</th>
                <th scope="col">Description</th>
                <th scope="col">PDFs</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><time datetime="2026-08-26">Aug 26th</time></td>
                <td>Introduction to ML Systems</td>
                <td><a href="/course_pdfs/E2E_ML/Introduction.pdf">Introduction</a></td>
              </tr>
              <tr>
                <td><time datetime="2026-09-02">Sept 2nd</time></td>
                <td>Types of ML Systems</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-09-09">Sept 9th</time></td>
                <td>ML Workflows</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-09-16">Sept 16th</time></td>
                <td>Data Engineering</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-09-23">Sept 23rd</time></td>
                <td>Model Development and Frameworks</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-09-30">Sept 30th</time></td>
                <td>Model Training</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-10-07">Oct 7th</time></td>
                <td>Midterm-1 and Project Presentations</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-10-14">Oct 14th</time></td>
                <td>Optimization Principles</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-10-21">Oct 21st</time></td>
                <td>Data Selection</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-10-28">Oct 28th</time></td>
                <td>Model Compression and Benchmarking</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-11-04">Nov 4th</time></td>
                <td>Model Deployment</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-11-11">Nov 11th</time></td>
                <td>Model Serving</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-11-18">Nov 18th</time></td>
                <td>Midterm-2 and Project Presentations</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-12-02">Dec 2nd</time></td>
                <td>LLMs</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-12-09">Dec 9th</time></td>
                <td>Agentic AI</td>
                <td>&mdash;</td>
              </tr>
              <tr>
                <td><time datetime="2026-12-16">Dec 16th</time></td>
                <td>Final Project Presentations</td>
                <td>&mdash;</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="labs" class="course-section" aria-labelledby="labs-title">
        <h2 id="labs-title"><i class="fa-solid fa-flask"></i> Class Labs</h2>
        <p>
          One class lab a week, following the lectures. Each runs entirely in your browser, so
          there is nothing to install and nothing to set up. Work through them in order, because
          each one builds on the week before. Every lab ends by writing a short report for you to
          download and hand in.
        </p>
        <div class="lab-grid">
          {% assign course_labs = site.data.labs | sort: "number" %}
          {% for lab in course_labs %}
            {% include lab_card.html lab=lab %}
          {% endfor %}
        </div>
      </section>

      <section id="project" class="course-section" aria-labelledby="project-title">
        <h2 id="project-title"><i class="fa-solid fa-diagram-project"></i> Project</h2>
        <p>
          The course project is completed in three phases. Together, the three phases build a complete end-to-end ML pipeline.
        </p>
      </section>

      <section id="exams" class="course-section" aria-labelledby="exams-title">
        <h2 id="exams-title"><i class="fa-regular fa-pen-to-square"></i> Exams</h2>
        <p>
          There are two midterm exams, held according to the dates listed in the course schedule.
        </p>
      </section>

      <section id="grades" class="course-section" aria-labelledby="grades-title">
        <h2 id="grades-title"><i class="fa-solid fa-scale-balanced"></i> Grades</h2>
        <h3>Assessment</h3>
        <div class="table-wrap">
          <table class="grade-table">
            <thead>
              <tr>
                <th scope="col">Component</th>
                <th scope="col">Weight</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Assignments (5 Quizzes, 5 Reflections, Labs)</td>
                <td>25%</td>
              </tr>
              <tr>
                <td>Midterm</td>
                <td>30%</td>
              </tr>
              <tr>
                <td>Final Project</td>
                <td>40%</td>
              </tr>
              <tr>
                <td>Participation</td>
                <td>5%</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>Grade Boundaries</h3>
        <div class="table-wrap">
          <table class="grade-table">
            <thead>
              <tr>
                <th scope="col">Letter Grade</th>
                <th scope="col">Percentage &ge;</th>
                <th scope="col">Letter Grade</th>
                <th scope="col">Percentage &ge;</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>A+</td><td>95</td><td>C+</td><td>77</td></tr>
              <tr><td>A</td><td>92</td><td>C</td><td>73</td></tr>
              <tr><td>A-</td><td>90</td><td>C-</td><td>70</td></tr>
              <tr><td>B+</td><td>88</td><td>D</td><td>60</td></tr>
              <tr><td>B</td><td>84</td><td>F</td><td>Below 60</td></tr>
              <tr><td>B-</td><td>80</td><td aria-hidden="true">&mdash;</td><td aria-hidden="true">&mdash;</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="rules" class="course-section" aria-labelledby="rules-title">
        <h2 id="rules-title"><i class="fa-solid fa-gavel"></i> Rules</h2>
        <h3>Course Expectations</h3>
        <ul>
          <li>Students are expected to complete the labs on a weekly basis as the lectures proceed.</li>
          <li>Lecture discussions, lab assignments, and the course project are the core delivery mechanisms for the course material.</li>
          <li>Lecture topics may include quizzes and discussions to gauge comprehension and attendance. Missed participation events cannot be made up and receive a grade of zero.</li>
        </ul>

        <h3>Labs and Deadlines</h3>
        <ul>
          <li>All labs are an individual effort. Understanding of the labs will be assessed through in-class exercises and quizzes.</li>
          <li>Each lab must be submitted by the end of the week. Late submissions are not allowed unless acute circumstances have been communicated in a timely manner.</li>
          <li>Exceptions may be made for an illness documented by a medical professional or when the instructor receives advance notice concerning illness, family-related matters, or career-related matters.</li>
          <li>Information-technology problems, failures, or challenges are not appropriate excuses for late work.</li>
        </ul>

        <h3>Communication</h3>
        <ul>
          <li>The subject of course-related email must contain &ldquo;CS.&rdquo; Otherwise, a response is not guaranteed.</li>
          <li>All electronic interactions are an extension of the classroom and must remain respectful and professional.</li>
        </ul>

        <h3>AI and Academic Integrity</h3>
        <ul>
          <li>Unless explicitly permitted as part of an assignment, students may not use ChatGPT or similar tools to solve course assignments.</li>
          <li>All exercises and projects are intended to be an individual effort. Unauthorized collaboration or copying will result in a grade of zero for all students involved.</li>
          <li>Academic-dishonesty violations involving programming exercises or projects will be reported to the Office of Academic Integrity.</li>
        </ul>
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
    keepLinkVisibleInsideNav(active);
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
