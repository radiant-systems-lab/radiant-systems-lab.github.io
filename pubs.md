---
layout: frontpage
title: Publications
---

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<h2 style="font-size:1.5rem; font-weight:700; margin-top:2rem;">
  <span style="border-bottom: 4px solid #FBBF24; padding-bottom: 0.25rem;">
    Publications
  </span>
</h2>

<p>
  You can also find our articles on our
  <a href="https://scholar.google.com/citations?hl=en&user=ZvYwdsUAAAAJ"
     target="_blank">Google Scholar profile</a>.
</p>

<div class="pub-filter" style="margin-bottom:1rem;">
  <label for="pubTypeFilter" style="font-weight:500;margin-right:0.25rem;">
    Filter by type:
  </label>
  <select id="pubTypeFilter"
          style="height:2.5rem;padding:0 0.75rem;border:1px solid #D1D5DB;border-radius:0.375rem;">
    <option value="all">All</option>
    <option value="article">Articles</option>
    <option value="chapter">Chapters</option>
    <option value="dissertation">Dissertations</option>
    <option value="editorial">Editorials</option>
    <option value="other">Others</option>
  </select>
</div>

{%- comment -%}
Collect all publications safely
{%- endcomment -%}
{% assign pubs = site.data.single_data_source
  | where_exp: "i", "i.Publication"
  | where_exp: "i", "i.Publication.date"
  | sort: "Publication.date"
  | reverse %}

{%- comment -%}
Extract unique publication YEARS (as strings)
{%- endcomment -%}
{% assign years = "" | split: "" %}
{% for item in pubs %}
  {% assign y = item.Publication.date | date: "%Y" %}
  {% assign years = years | push: y %}
{% endfor %}
{% assign years = years | uniq | sort | reverse %}

<div id="pub-list">
{% for y in years %}
  <h3 class="pubyear">{{ y }}</h3>
  <ol>

  {% for item in pubs %}
    {% assign p = item.Publication %}
    {% assign uid = item.id %}
    {% assign pub_year = p.date | date: "%Y" %}

    {% if pub_year == y %}
      {% assign type = p.pubType | default: "other" | downcase %}

      <li class="pub-entry" data-type="{{ type }}">
        <h4 class="pub-title">{{ p.title }}</h4>

        {% if p.authors %}
          <div class="pub-authors">{{ p.authors }}</div>
        {% endif %}

        {% if p.journal %}
          <div class="pub-venue">
            <em>{{ p.journal }}</em>
          </div>
        {% endif %}

        <div class="pub-icons">

          {% if p.abstract %}
          <button class="pub-action"
                  onclick="toggleSection('abs-{{ uid }}')"
                  title="Abstract">
            <i class="fas fa-file-alt"></i>
          </button>
          {% endif %}

          <button class="pub-action"
                  onclick="toggleSection('bib-{{ uid }}')"
                  title="BibTeX">
            <i class="fas fa-code"></i>
          </button>

          {%- comment -%}
          ONLY show PDF link (hard-coded)
          {%- endcomment -%}
          {% if p.links and p.links.PDF %}
            <a href="{{ p.links.PDF.url }}"
               class="pub-action"
               target="_blank"
               title="{{ p.links.PDF.text }}">
              <i class="fas fa-file-pdf"></i>
            </a>
          {% endif %}

        </div>

        {% if p.abstract %}
        <div id="abs-{{ uid }}" class="pub-section" style="display:none;">
          <p>{{ p.abstract }}</p>
        </div>
        {% endif %}

        <div id="bib-{{ uid }}" class="pub-section" style="display:none;">
<pre>@{{ p.pubType | downcase | default: "article" }}{ {{ p.citationKey }},
  title     = { {{ p.title }} },
  author    = { {{ p.authors }} },
{% if p.journal %}  journal   = { {{ p.journal }} },
{% endif %}{% if p.Publisher %}  publisher = { {{ p.Publisher }} },
{% endif %}  year      = {{ p.year }},
}
</pre>
</div>

      </li>
    {% endif %}
  {% endfor %}
  </ol>
{% endfor %}
</div>

<script>
function showPubType(type) {
  document.querySelectorAll('.pub-entry').forEach(li => {
    li.style.display =
      (type === 'all' || li.dataset.type === type) ? '' : 'none';
  });

  document.querySelectorAll('.pubyear').forEach(h => {
    const ol = h.nextElementSibling;
    const visible = [...ol.children]
      .some(li => li.style.display !== 'none');
    h.style.display = ol.style.display = visible ? '' : 'none';
  });
}

document.addEventListener('DOMContentLoaded', () => showPubType('all'));

document.getElementById('pubTypeFilter')
  .addEventListener('change', e => showPubType(e.target.value));

function toggleSection(id) {
  const el = document.getElementById(id);
  if (el) {
    el.style.display = el.style.display === 'block' ? 'none' : 'block';
  }
}
</script>
