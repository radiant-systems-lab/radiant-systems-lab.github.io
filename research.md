---
layout: page
title: Research
description: Radiant's Research Projects
---

<div class="navbar">
  <div class="navbar-inner">
    <ul class="nav">
        {% for cat in site.data.research_categories %}
            <li><a href="#{{ cat[0] }}">{{ cat[0] }}</a></li>
        {% endfor %}
    </ul>
  </div>
</div>

<style>
.research-section {
  display: none;
}

.research-section.active {
  display: block;
}

.research-header {
  color: #6b21a8; /* purple */
  margin-top: 1.5rem;
}
/*
.media {
  box-sizing: border-box;
  border: 1px solid rgba(0,0,0,.125);
  margin-bottom: 1rem;
  display: table;
  width: 100%;
}

.media-left {
  width: 315px;
  min-width: 315px;
  max-width: 315px;
  height: 220px;              
  background: rgb(211, 222, 234);
  display: table-cell;
  vertical-align: middle;
  text-align: center;
  overflow: hidden;
}

.media-body {
  padding: 20px;
  display: table-cell;
  vertical-align: top;
}*/

.media {
  display: flex;
  align-items: flex-start;   
  border: 1px solid rgba(0,0,0,.125);
  margin-bottom: 1rem;
}

.media-left {
  width: 315px;
  min-width: 315px;
  height: 220px;
  background: rgb(211, 222, 234);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.media-body {
  padding: 20px;
  flex: 1;
}

</style>

{% assign all_items = site.data.single_data_source %}

{% for cat in site.data.research_categories %}
<section id="{{ cat[0] }}" class="research-section">

  <h2 class="research-header">{{ cat[1].title }}</h2>
  <p>{{ cat[1].description }}</p>

  {% assign shown = 0 %}

  {% for item in all_items %}
    {% if item.Research and item.Research.categories %}
      {% if item.Research.categories contains cat[0] %}
        {% if shown < 8 %}

          {% assign r = item.Research %}
          {% assign pub_ids = r.publicationIDs %}

          <div class="media">
            <div class="media-left">
              {% if r.image %}
                <img src="{{ r.image }}" style="width:100%; height:100%; object-fit: contain; ">
              {% endif %}
            </div>

            <div class="media-body">
              <h4>{{ r.researchTitle }}</h4>

              {% if r.abstract %}
                <p>{{ r.abstract }}</p>
              {% endif %}

              {% if pub_ids %}
                {% for pid in pub_ids %}

                  {%- comment -%}
                  Step 1: Try finding a standalone publication entry
                  {%- endcomment -%}
                  {% assign pub_item = all_items | where: "id", pid | first %}

                  {% if pub_item and pub_item.Publication %}
                    {% assign pub = pub_item.Publication %}
                  {% else %}
                    {%- comment -%}
                    Step 2: Fallback — search inside common entries
                    {%- endcomment -%}
                    {% assign pub = nil %}
                    {% for it in all_items %}
                      {% if it.entry_kind == "common" and it.Publication and it.Publication.id == pid %}
                        {% assign pub = it.Publication %}
                      {% endif %}
                    {% endfor %}
                  {% endif %}

                  {% if pub %}
                    <p>
                      <strong>{{ pub.title }}.</strong>
                      {{ pub.authors }},
                      <strong><i>{{ pub.journal }}</i></strong>,
                      {{ pub.date | date: "%Y" }}.
                      <a href="{{ pub.link }}">Read More &gt;&gt;</a>
                    </p>
                  {% endif %}

                {% endfor %}
              {% endif %}
            </div>
          </div>

          {% assign shown = shown | plus: 1 %}

        {% endif %}
      {% endif %}
    {% endif %}
  {% endfor %}

</section>
{% endfor %}


<script>
function activateCategory() {
  const hash = window.location.hash.replace("#", "") || "RAS";
  document.querySelectorAll(".research-section").forEach(section => {
    section.classList.toggle("active", section.id === hash);
  });
}

window.addEventListener("hashchange", activateCategory);
document.addEventListener("DOMContentLoaded", activateCategory);
</script>
