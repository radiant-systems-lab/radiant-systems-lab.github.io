---
layout: frontpage
title: Publications
---

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="{{ ASSET_PATH }}/css/publications.css">

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

<div class="pub-filter" style="margin-bottom: 2rem;">
  <label for="pubTypeFilter" style="font-weight: 500; margin-right: 0.5rem;">Filter by type:</label>
  <select id="pubTypeFilter" style="padding: 0.5rem 1rem; border: 1px solid #D1D5DB; border-radius: 0.375rem;">
    <option value="all">All</option>
    <option value="article">Articles</option>
    <option value="chapter">Chapters</option>
    <option value="dissertation">Dissertations</option>
    <option value="editorial">Editorials</option>
    <option value="other">Others</option>
  </select>
</div>

{% assign pubs  = site.data.publications %}
{% assign years = pubs | map: "Year" | uniq | sort | reverse %}

<div id="pub-list">
  {% for y in years %}
    <h3 class="pubyear">{{ y }}</h3>
    <ol>
      {% for p in pubs %}
        {% if p.Year == y %}
          {% comment %}
            Classify each pub by type. There's no YAML key for editorials,
            so those are left out unless you add one later.
          {% endcomment %}
          {% if p.Conference or p.Journal %}
            {% assign typeForP = "article" %}
          {% elsif p.Book %}
            {% assign typeForP = "chapter" %}
          {% elsif p.Institution %}
            {% assign typeForP = "dissertation" %}
          {% else %}
            {% assign typeForP = "other" %}
          {% endif %}

          <li class="pub-entry" data-type="{{ typeForP }}">
            <h4 class="pub-title">{{ p.title }}</h4>
            <div class="pub-authors">{{ p.Authors }}</div>
            <div class="pub-venue">
              <em>
                {% if p.Book       %}{{ p.Book       }}
                {% elsif p.Conference %}{{ p.Conference }}
                {% elsif p.Journal  %}{{ p.Journal   }}
                {% elsif p.Publisher %}{{ p.Publisher }}
                {% endif %}
              </em>
            </div>

            <div class="pub-icons">
              {% if p.Description %}
              <button class="pub-action"
                      onclick="toggleSection('abs-{{ p.id }}')">
                <i class="fas fa-file-alt"></i> Abstract
              </button>
              {% endif %}
              <button class="pub-action"
                      onclick="toggleSection('bib-{{ p.id }}')">
                <i class="fas fa-code"></i> BibTeX
              </button>
              {% if p.pdf_link %}
              <a href="{{ p.pdf_link }}"
                 class="pub-action" target="_blank">
                <i class="fas fa-file-pdf"></i> PDF
              </a>
              {% endif %}
            </div>

            {% if p.Description %}
            <div id="abs-{{ p.id }}" class="pub-section pub-abstract" style="display:none;">
              <p>{{ p.Description }}</p>
            </div>
            {% endif %}

            <div id="bib-{{ p.id }}" class="pub-section pub-bibtex" style="display:none;">
<pre>@article{ {{ p.id }},
  title     = { {{ p.title }} },
  author    = { {{ p.bibAuthors | default: p.Authors }} },
  {% if p.Journal   %}journal   = { {{ p.Journal }} },{% endif %}
  {% if p.Publisher %}publisher = { {{ p.Publisher }} },{% endif %}
  year      = {{ p.Year }},
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
// filter function
function showPubType(type) {
  document.querySelectorAll('.pub-entry').forEach(li => {
    li.style.display =
      (type === 'all' || li.getAttribute('data-type') === type)
        ? '' : 'none';
  });
  // hide empty year blocks
  document.querySelectorAll('.pubyear').forEach(h3 => {
    const ol = h3.nextElementSibling;
    const any = ol && Array.from(ol.children)
                          .some(li=>li.style.display!== 'none');
    h3.style.display = ol.style.display = any ? '' : 'none';
  });
  // update active tab
  document.querySelectorAll('#pub-tabs li').forEach(tab => {
    const t = tab.querySelector('a').getAttribute('data-type');
    tab.classList.toggle('active', t === type);
  });
}

// wire up nav clicks
document.querySelectorAll('#pub-tabs a').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    showPubType(a.getAttribute('data-type'));
  });
});

// default to All
document.addEventListener('DOMContentLoaded', ()=> showPubType('all'));
document.getElementById("pubTypeFilter").addEventListener("change", (e) => {
  showPubType(e.target.value);
});

// toggles single section
function toggleSection(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const isHidden = el.style.display === 'none' || !el.classList.contains('show');
  if (isHidden) {
    el.style.display = 'block';
    el.classList.add('show');
  } else {
    el.style.display = 'none';
    el.classList.remove('show');
  }
}
</script>
