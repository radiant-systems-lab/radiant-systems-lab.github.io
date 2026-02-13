---
layout: page
title: FlexiFlow
permalink: /softwares/flexiflow/
---

<div class="page-floability page-flexiflow">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-sliders"></i> FlexiFlow</h2>
      <p class="page-subtitle">
        Adaptive model-switching for reliable and efficient end-to-end ML workflows.
      </p>
    </div>
    <div class="quick-jump-links">
      <a href="#flex-about">About</a>
      <a href="#flex-docs">Docs</a>
      <a href="#flex-code">Code</a>
      <a href="#flex-papers">Papers</a>
      <a href="#flex-team">Team</a>
      <a href="#flex-collaborators">Collaborators</a>
    </div>
  </div>

  <section class="project-section" id="flex-about">
    <h3 class="section-title"><i class="fa-solid fa-circle-info"></i> About</h3>
    <div class="about-grid">
      <div class="about-text">
        <p>
          <strong>FlexiFlow</strong> is a programming model aimed at automatic model switching
          to maximize performance in machine learning workflows.
        </p>
        <p>
          With increased use of machine learning in production systems, engineers face practical
          challenges in deploying and maintaining ML models and workflows. A recurring issue is
          soft failures: situations where a model does not crash but returns degraded predictions,
          often due to factors such as data drift.
        </p>
        <p>
          In multi-step workflows, these failures reduce end-to-end quality and increase operational
          burden. Static model selection at each step often fails to preserve accuracy across diverse
          real-world inputs. If one model underperforms, re-running the entire workflow with alternatives
          can significantly increase latency and cost.
        </p>
        <p>
          FlexiFlow introduces a dataflow approach that dynamically switches between alternate models
          when current models show low accuracy. It learns model ranking through a multi-armed bandit
          strategy that incorporates runtime, assertion pass probability, and workflow structure.
        </p>
      </div>
      <figure class="about-figure">
        <img src="/images/softwares/FlexiFlow-Arch.png" alt="FlexiFlow architecture diagram">
        <figcaption>FlexiFlow Architecture</figcaption>
      </figure>
    </div>
  </section>

  <section class="project-section" id="flex-docs">
    <h3 class="section-title"><i class="fa-regular fa-file-lines"></i> Docs</h3>
    <p>Documentation links will be published with the public repository release.</p>
  </section>

  <section class="project-section" id="flex-code">
    <h3 class="section-title"><i class="fa-solid fa-code"></i> Code</h3>
    <p>
      The FlexiFlow repository is currently being prepared for open-source release.
      The Dockerfile used to build the FlexiFlow environment will be available in the repository root.
    </p>
  </section>

  <section class="project-section" id="flex-papers">
    <h3 class="section-title"><i class="fa-regular fa-newspaper"></i> Papers</h3>
    <p>Upcoming papers will be added here.</p>
  </section>

  <section class="project-section" id="flex-team">
    <h3 class="section-title"><i class="fa-solid fa-people-group"></i> Team</h3>
    <div class="team-gallery people image-container">
      {% assign flexiflow_team = site.data.flexiflow_lab %}
      {% for person in flexiflow_team %}
        {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
      {% endfor %}
    </div>
  </section>

  <section class="project-section" id="flex-collaborators">
    <h3 class="section-title"><i class="fa-solid fa-handshake"></i> Collaborators</h3>
    <ul class="collab-list">
      {% assign collaborators = site.data.flexiflow_collaborators %}
      {% for person in collaborators %}
        <li class="collab-item">
          <a href="{{ person.website }}" target="_blank">{{ person.name }}</a>
          <span>{{ person.affliation }}</span>
        </li>
      {% endfor %}
    </ul>
  </section>
</div>
