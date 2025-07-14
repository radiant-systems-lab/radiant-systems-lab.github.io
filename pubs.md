---
layout: frontpage
title: Publications
---

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="{{ ASSET_PATH }}/css/publications.css">

# Publications

<p>
  You can also find our articles on our
  <a href="https://scholar.google.com/citations?hl=en&user=ZvYwdsUAAAAJ"
     target="_blank">Google Scholar profile</a>.
</p>

<div class="navbar">
  <div class="navbar-inner">
    <ul id="pub-tabs" class="nav nav-tabs">
      <li id="tab-all"         class="active"><a href="#" data-type="all">All</a></li>
      <li id="tab-article"               ><a href="#" data-type="article">Articles</a></li>
      <li id="tab-chapter"               ><a href="#" data-type="chapter">Chapters</a></li>
      <li id="tab-dissertation"          ><a href="#" data-type="dissertation">Dissertations</a></li>
      <li id="tab-editorial"             ><a href="#" data-type="editorial">Editorials</a></li>
      <li id="tab-other"                 ><a href="#" data-type="other">Others</a></li>
    </ul>
  </div>
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
            <div id="abs-{{ p.id }}" class="pub-section pub-abstract">
              <p>{{ p.Description }}</p>
            </div>
            {% endif %}

            <div id="bib-{{ p.id }}" class="pub-section pub-bibtex">
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

// toggles single section
function toggleSection(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('show');
}
</script>
