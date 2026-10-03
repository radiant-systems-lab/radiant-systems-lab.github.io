---
layout: page
title: Talks
description: Keynotes, invited talks, panels, seminars, and research presentations from the Radiant Systems Lab
---

<div class="page-talks">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-microphone-lines"></i> Talks &amp; Keynotes</h2>
      <p class="page-subtitle">
        Keynotes, invited talks, panels, seminars, and research presentations from the Radiant Systems Lab.
      </p>
    </div>
    <div class="quick-jump-links" aria-label="Talk sections">
      <a href="#upcoming">Upcoming</a>
      <a href="#past">Past</a>
    </div>
  </div>

  {% assign talks = site.data.talks | sort: "Talk.date" | reverse %}
  {% assign upcoming_talks = talks | where_exp: "item", "item.Talk.status == 'upcoming'" %}
  {% assign past_talks = talks | where_exp: "item", "item.Talk.status == 'past'" %}

  <section id="upcoming" class="talk-section" aria-labelledby="upcoming-title">
    <div class="talk-section-heading">
      <div>
        <p class="talk-section-kicker">On the calendar</p>
        <h3 id="upcoming-title">Upcoming Talks</h3>
      </div>
      <span class="talk-count">{{ upcoming_talks.size }}</span>
    </div>

    {% if upcoming_talks.size > 0 %}
      <div class="talk-list">
        {% for item in upcoming_talks %}
          {% assign talk = item.Talk %}
          {% include talk_card.html item=item talk=talk %}
        {% endfor %}
      </div>
    {% else %}
      <p class="talk-empty">No upcoming talks are currently scheduled.</p>
    {% endif %}
  </section>

  <section id="past" class="talk-section" aria-labelledby="past-title">
    <div class="talk-section-heading">
      <div>
        <p class="talk-section-kicker">Archive and materials</p>
        <h3 id="past-title">Past Talks</h3>
      </div>
      <span class="talk-count">{{ past_talks.size }}</span>
    </div>

    {% if past_talks.size > 0 %}
      <div class="talk-list">
        {% for item in past_talks %}
          {% assign talk = item.Talk %}
          {% include talk_card.html item=item talk=talk %}
        {% endfor %}
      </div>
    {% else %}
      <p class="talk-empty">Past talk materials will appear here after an event is completed.</p>
    {% endif %}
  </section>
</div>

