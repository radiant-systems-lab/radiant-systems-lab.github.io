---
layout: page
title: Floability
permalink: /softwares/floability/
---

<div class="page-floability">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-diagram-project"></i> Floability</h2>
      <p class="page-subtitle">
        Portable notebook workflows for distributed scientific cyberinfrastructure.
      </p>
    </div>
    <div class="quick-jump-links">
      <a href="#flo-about">About</a>
      <a href="#flo-docs">Docs</a>
      <a href="#flo-code">Code</a>
      <a href="#flo-papers">Papers</a>
      <a href="#flo-team">Team</a>
      <a href="#flo-collaborators">Collaborators</a>
    </div>
  </div>

  <section class="project-section" id="flo-about">
    <h3 class="section-title"><i class="fa-solid fa-circle-info"></i> About</h3>
    <div class="about-grid">
      <div class="about-text">
        <p>
          <strong>Floability</strong> is a system that enables rapid and portable deployment of notebooks
          expressing complex scientific workflows across a wide range of cyberinfrastructure.
          The key challenge is that workflows are often incomplete: code alone cannot move between facilities
          without accurately capturing software dependencies, required datasets, and cluster capabilities.
        </p>
        <p>
          Floability also addresses translation between notebooks and workflows. The project is collaboratively
          developed by the University of Notre Dame, the University of Missouri-Columbia, and the University of Illinois.
        </p>
      </div>
      <figure class="about-figure">
        <img src="/images/softwares/floability-Arch.png" alt="Floability architecture diagram">
        <figcaption>Floability Architecture</figcaption>
      </figure>
    </div>
  </section>

  <section class="project-section" id="flo-docs">
    <h3 class="section-title"><i class="fa-regular fa-file-lines"></i> Docs</h3>
    <ul class="resource-list">
      <li><a href="https://github.com/floability/floability-cli/blob/main/README.md" target="_blank">Quick start instructions</a></li>
      <li><a href="https://github.com/floability/floability-cli/blob/main/docs/backpack.md" target="_blank">Backpack specifications</a></li>
      <li><a href="https://github.com/floability/floability-examples" target="_blank">Backpack examples</a></li>
    </ul>
  </section>

  <section class="project-section" id="flo-code">
    <h3 class="section-title"><i class="fa-solid fa-code"></i> Code</h3>
    <p>The primary repository for Floability is available on GitHub.</p>
    <div class="project-links">
      <a class="project-link" href="https://github.com/floability/floability-cli" target="_blank">
        <i class="fa-brands fa-github"></i> floability-cli
      </a>
      <a class="project-link" href="https://github.com/floability/floability-examples" target="_blank">
        <i class="fa-solid fa-box-archive"></i> Examples
      </a>
    </div>
  </section>

  <section class="project-section" id="flo-papers">
    <h3 class="section-title"><i class="fa-regular fa-newspaper"></i> Papers</h3>
    <ul class="resource-list">
      <li>
        Islam, M. S., Azaz, T., Ahmad, R., Hossain, A. S. M. S., Baig, F., Wang, S., Lannon, K.,
        Malik, T., and Thain, D., "Backpacks for Notebooks: Enabling Containerized Notebook Workflows in
        Distributed Environments", <em>21st IEEE International Conference on eScience</em>, to appear, 2025.
      </li>
    </ul>
  </section>

  <section class="project-section" id="flo-team">
    <h3 class="section-title"><i class="fa-solid fa-people-group"></i> Team</h3>
    <div class="team-gallery people image-container">
      {% assign floability_team = site.data.floability_lab %}
      {% for person in floability_team %}
        {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
      {% endfor %}
    </div>
  </section>

  <section class="project-section" id="flo-collaborators">
    <h3 class="section-title"><i class="fa-solid fa-handshake"></i> Collaborators</h3>
    <ul class="collab-list">
      {% assign collaborators = site.data.floability_collaborators %}
      {% for person in collaborators %}
        <li class="collab-item">
          <a href="{{ person.website }}" target="_blank">{{ person.name }}</a>
          <span>{{ person.affliation }}</span>
        </li>
      {% endfor %}
    </ul>
  </section>
</div>
