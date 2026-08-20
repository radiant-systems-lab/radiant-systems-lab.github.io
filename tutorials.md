---
layout: page
title: Tutorials
description: Research tutorials and hands-on materials from the Radiant Systems Lab
---

<div class="page-tutorials">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-person-chalkboard"></i> Research Tutorials</h2>
      <p class="page-subtitle">
        Conference tutorials and hands-on materials that translate our research into reproducible practice.
      </p>
    </div>
    <div class="quick-jump-links" aria-label="Tutorial sections">
      <a href="#upcoming">Upcoming</a>
      <a href="#past">Past</a>
    </div>
  </div>

  {% assign tutorials = site.data.tutorials | sort: "Tutorial.date" | reverse %}
  {% assign upcoming_tutorials = tutorials | where_exp: "item", "item.Tutorial.status == 'upcoming'" %}
  {% assign past_tutorials = tutorials | where_exp: "item", "item.Tutorial.status == 'past'" %}

  <section id="upcoming" class="tutorial-section" aria-labelledby="upcoming-title">
    <div class="tutorial-section-heading">
      <div>
        <p class="tutorial-section-kicker">Research training</p>
        <h3 id="upcoming-title">Upcoming Tutorials</h3>
      </div>
      <span class="tutorial-count">{{ upcoming_tutorials.size }}</span>
    </div>

    {% if upcoming_tutorials.size > 0 %}
      <div class="tutorial-list">
        {% for item in upcoming_tutorials %}
          {% assign tutorial = item.Tutorial %}
          {% include tutorial_card.html item=item tutorial=tutorial %}
        {% endfor %}
      </div>
    {% else %}
      <p class="tutorial-empty">No upcoming research tutorials are currently scheduled.</p>
    {% endif %}
  </section>

  <section id="past" class="tutorial-section" aria-labelledby="past-title">
    <div class="tutorial-section-heading">
      <div>
        <p class="tutorial-section-kicker">Archive and materials</p>
        <h3 id="past-title">Past Tutorials</h3>
      </div>
      <span class="tutorial-count">{{ past_tutorials.size }}</span>
    </div>

    {% if past_tutorials.size > 0 %}
      <div class="tutorial-list">
        {% for item in past_tutorials %}
          {% assign tutorial = item.Tutorial %}
          {% include tutorial_card.html item=item tutorial=tutorial %}
        {% endfor %}
      </div>
    {% else %}
      <p class="tutorial-empty">Past tutorial materials will appear here after an event is completed.</p>
    {% endif %}
  </section>
</div>
