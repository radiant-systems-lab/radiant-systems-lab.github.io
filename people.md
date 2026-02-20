---
title: Members of Radiant Lab
layout: page
description: Radiant's members
---

<div class="page-people">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-people-group"></i> Members of Radiant Lab</h2>
      <p class="page-subtitle">Meet our current team, alumni, and open research positions.</p>
    </div>
    <div class="quick-jump-links">
      <a href="#phd">Graduate Students</a>
      <a href="#ms">Master's Students</a>
      <a href="#alumni">Alumni</a>
      <a href="#openings">Openings</a>
    </div>
  </div>

  <section class="people-section" id="director">
    <h2 class="people-section-title"><i class="fa-solid fa-user-tie"></i> Director</h2>
    <div class="people image-container people-grid director-grid">
      {% for person in site.data.faculty %}
        {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
      {% endfor %}
    </div>
  </section>

  <section class="people-section" id="postdocs">
    <h2 class="people-section-title"><i class="fa-solid fa-flask"></i> Postdocs</h2>
    <p class="role-note">We are currently recruiting postdocs. See <a href="#openings">open positions</a>.</p>
  </section>

  <section class="people-section" id="phd">
    <h2 class="people-section-title"><i class="fa-solid fa-user-graduate"></i> Graduate Students</h2>
    <div class="people image-container people-grid">
      {% for person in site.data.phd_students %}
        {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
      {% endfor %}
    </div>
  </section>

  <section class="people-section" id="ms">
    <h2 class="people-section-title"><i class="fa-solid fa-user"></i> Master's Students</h2>
    <div class="people image-container people-grid">
      {% for person in site.data.master_students %}
        {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
      {% endfor %}
    </div>
  </section>

  <section class="people-section" id="ug">
    <h2 class="people-section-title"><i class="fa-solid fa-laptop-code"></i> Undergraduate Students</h2>
    <p class="role-note">Interested in joining? See <a href="#openings">open positions</a>.</p>
  </section>

  <section class="people-section" id="alumni">
    <h2 class="people-section-title"><i class="fa-solid fa-users-line"></i> Alumni</h2>
    {% if site.data.alumni %}
      <ul class="alumni-list">
        {% assign sorted_alumni = site.data.alumni | sort: "name" %}
        {% for person in sorted_alumni %}
          <li>
            {% if person.website %}
              <a href="{{ person.website }}">{{ person.name }}</a>
            {% else %}
              <span class="alumni-name">{{ person.name }}</span>
            {% endif %}
            {% if person.at %}<span class="at">Now at {{ person.at }}</span>{% endif %}
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p>No alumni data available.</p>
    {% endif %}
  </section>

  <section class="people-section" id="openings">
    <h2 class="people-section-title"><i class="fa-solid fa-briefcase"></i> Current Openings</h2>
    <div class="openings">
      <div class="opening-card">
        <h3><i class="fa-solid fa-user-doctor"></i> Post-doctoral Position</h3>
        <p>
          The <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a>
          in the <a href="https://engineering.missouri.edu/">College of Engineering</a> at
          <a href="https://missouri.edu/">University of Missouri, Columbia</a>
          is seeking talented and motivated postdoctoral fellows to work on exciting scientific research projects.
        </p>

        <p>
          <strong>Areas:</strong> Graph data management, data provenance/lineage, workflow systems, notebooks, and scientific data management.
          Focus on capturing, tracking, and making understandable large-scale distributed scientific experiments using HPC and finite-element models.
        </p>

        <ul class="opening-meta">
          <li>
            <span class="meta-label">Eligibility</span>
            <span class="meta-value">Ph.D. within the last three years in systems, workflows, data management, HPC, or related fields.</span>
          </li>
          <li>
            <span class="meta-label">Start Date</span>
            <span class="meta-value">Anytime after January 1, 2026.</span>
          </li>
          <li>
            <span class="meta-label">Duration</span>
            <span class="meta-value">Up to 4 years.</span>
          </li>
          <li>
            <span class="meta-label">Benefits</span>
            <span class="meta-value">Competitive salary and excellent benefits.</span>
          </li>
          <li>
            <span class="meta-label">Supervisors</span>
            <span class="meta-value">Tanu Malik and advisory team.</span>
          </li>
          <li>
            <span class="meta-label">Location</span>
            <span class="meta-value">Multi-university, multi-disciplinary center with opportunities for travel, training, and dissemination.</span>
          </li>
        </ul>

        <p><strong>How to Apply:</strong> Send your CV and Research Statement to <a href="mailto:tanu@missouri.edu">tanu@missouri.edu</a>.</p>
      </div>
    </div>
  </section>
</div>
