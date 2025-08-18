---
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

  <!-- Submenu Tabs -->
  <section class="stats-section">
    <div class="stats-grid">
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="news">News</span></div>
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="content">Content</span></div>
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="schedule">Schedule</span></div>
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="exams">Exams</span></div>
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="grades">Grades</span></div>
      <div class="stats-item"><span class="stat-label submenu-tab" data-tab="rules">Rules</span></div>
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
.work-link {
  text-decoration: none;
  color: #000;
}

.work-link:hover {
  text-decoration: underline;
}

.submenu-tab {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #F3F4F6;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submenu-tab:hover,
.submenu-tab.active {
  background-color: #FBBF24;
  color: #000;
}

.stats-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.stats-item {
  flex: 1 1 120px;
  text-align: center;
}

.tab-content {
  display: block;
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
      if(tc.id === selected) {
        tc.style.display = 'block';
      } else {
        tc.style.display = 'none';
      }
    });
  });
});

// Set default active tab
tabs[0].click();
</script>
