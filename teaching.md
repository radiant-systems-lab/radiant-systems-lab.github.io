---
title: Teaching
layout: page
---

<div class="container" style="padding: 0; margin-top:0;">

  <!-- Course Header -->
  <section class="course-section">
    <h2 class="work-title">
      <span class="work-underline">
        <a href="https://radiant-systems-lab.github.io/softwares/flexiflow/" class="work-link">CSC/EE 8001</a>
      </span>
    </h2>
    <p class="work-text">
      Machine learning systems are both complex and unique. Complex because they consist of many different components and involve many different stakeholders. Unique because they're data dependent, with data varying wildly from one use case to the next. 
      In this course we will first learn how to build, deploy, assure, and maintain machine-learned models. It will include starting from prototype ML model to considering an end-to-end pipeline. Students will be able to identify key components of the ML pipeline, evaluate deployment scenarios, and monitor patterns for different production scenarios.
      <br><br>
      We will then cover several topics in responsible AI spanning from ethics, fairness, and accountability. The course will cover projects and reading state-of-the-art papers.
    </p>
  </section>

  <!-- Sticky Submenu Tabs -->
  <section class="stats-section sticky-submenu">
    <div class="submenu-container">
      <span class="submenu-tab active" data-tab="news">News</span>
      <span class="submenu-tab" data-tab="content">Content</span>
      <span class="submenu-tab" data-tab="schedule">Schedule</span>
      <span class="submenu-tab" data-tab="exams">Exams</span>
      <span class="submenu-tab" data-tab="grades">Grades</span>
      <span class="submenu-tab" data-tab="rules">Rules</span>
    </div>
  </section>

  <!-- Submenu Content Placeholders -->
  <section class="course-section" id="course_content">
    <div class="text-wrapper">

      <div class="tab-content" id="news">
        <!-- Enter News content here -->
      </div>

      <div class="tab-content" id="content" style="display:none;">
        <!-- Enter Content tab content here -->
      </div>

      <div class="tab-content" id="schedule" style="display:none;">
        <!-- Enter Schedule tab content here -->
      </div>

      <div class="tab-content" id="exams" style="display:none;">
        <!-- Enter Exams tab content here -->
      </div>

      <div class="tab-content" id="grades" style="display:none;">
        <!-- Enter Grades tab content here -->
      </div>

      <div class="tab-content" id="rules" style="display:none;">
        <!-- Enter Rules tab content here -->
      </div>

    </div>
  </section>

</div>

<style>
/* General Links */
.work-link {
  text-decoration: none;
  color: #000;
}

.work-link:hover {
  text-decoration: underline;
}

/* Course Section */
.course-section {
  background-color: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  padding: 2rem;
  margin-bottom: 2rem;
}

/* Sticky Submenu */
.sticky-submenu {
  position: sticky;
  top: 1rem;
  z-index: 10;
  background-color: #fff;
  padding: 1rem 0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

/* Submenu Tabs */
.submenu-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.submenu-tab {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  background-color: #F3F4F6;
  border-radius: 9999px; /* pill shape */
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

.submenu-tab:hover {
  background-color: #FBBF24;
  color: #000;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.submenu-tab.active {
  background-color: #FBBF24;
  color: #000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* Tab Content */
.tab-content {
  display: block;
  margin-top: 1rem;
}

/* Container bottom spacing to avoid footer clash */
.container {
  padding-bottom: 4rem;
}
</style>

<script>
const tabs = document.querySelectorAll('.submenu-tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    // Remove active from all tabs
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    // Show selected tab content and hide others
    const selected = tab.getAttribute('data-tab');
    tabContents.forEach(tc => {
      tc.style.display = (tc.id === selected) ? 'block' : 'none';
    });
  });
});

// Set default active tab
tabs[0].click();
</script>
