---
layout: frontpage
title: Publications
---

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="{{ BASE_PATH }}/assets/css/publications.css">



# Publications

<div class="navbar">
    <div class="navbar-inner">
        <ul id="pub-tabs" class="nav nav-tabs">
            <li id="tab-article" class="active"><a href="javascript:showPubType('article')">Articles</a></li>
            <li id="tab-chapter"><a href="javascript:showPubType('chapter')">Chapters</a></li>
            <li id="tab-dissertation"><a href="javascript:showPubType('dissertation')">Dissertations</a></li>
            <li id="tab-editorial"><a href="javascript:showPubType('editorial')">Editorials</a></li>
            <li id="tab-other"><a href="javascript:showPubType('other')">Others</a></li>
        </ul>
    </div>
</div>

<p>
You can also find my articles on my
<a href="https://scholar.google.com/citations?hl=en&user=ZvYwdsUAAAAJ">Google Scholar profile</a>.
</p>

{% assign publications = site.data.publications %}
{% assign years = publications | map: 'Year' | uniq | sort | reverse %}
{% for year in years %}
<h3 class="pubyear">{{ year }}</h3>
<ol>
{% for pub in publications %}
  {% if pub.Year == year %}
    <li>
      {{ pub.title }}<br>
      <em>{% if pub.Book %}{{ pub.Book }}{% elsif pub.Journal %}{{ pub.Journal }}{% elsif pub.Conference %}{{ pub.Conference }}{% elsif pub.Publisher %}{{ pub.Publisher }}{% endif %}</em>
      <div class="pub-icons">
        {% if pub.abstract_link %}
          <a href="{{ pub.abstract_link }}" target="_blank"><i class="fas fa-file-alt"></i></a>
        {% else %}
          <i class="fas fa-file-alt disabled"></i>
        {% endif %}
        {% if pub.bibtex_link %}
          <a href="{{ pub.bibtex_link }}" target="_blank"><i class="fas fa-code"></i></a>
        {% else %}
          <i class="fas fa-code disabled"></i>
        {% endif %}
        {% if pub.pdf_link %}
          <a href="{{ pub.pdf_link }}" target="_blank"><i class="fas fa-file-pdf"></i></a>
        {% else %}
          {% assign pdfName = pub.id | split: '-' | last | append: '.pdf' | prepend: '/pdfs/pdfs/pubs/' %}
          {% assign hasPdf = site.static_files | map:'path' | join:' ' | contains: pdfName %}
          {% if hasPdf %}
            <a href="{{ pdfName }}" target="_blank"><i class="fas fa-file-pdf"></i></a>
          {% else %}
            <i class="fas fa-file-pdf disabled"></i>
          {% endif %}
        {% endif %}
      </div>
    </li>
  {% endif %}
{% endfor %}
</ol>
{% endfor %}

<div id="pub-lists">
{% assign pub_types = "article,chapter,dissertation,editorial,other" | split: "," %}
{% for t in pub_types %}
  <div id="pub-{{ t }}" class="pub-type{% if forloop.first %} active{% endif %}">
    {% assign pubs_of_type = site.data.publications | where: 'type', t %}
    {% assign years = pubs_of_type | map: 'year' | uniq | sort | reverse %}
    {% for y in years %}
      <h3>{{ y }}</h3>
      <ol>
      {% for p in pubs_of_type %}
        {% if p.year == y %}
          <li>
            {{ p.title }}<br>
            <em>{{ p.venue }}</em>
            <div class="pub-icons">
              {% if p.abstract_link %}
                <a href="{{ p.abstract_link }}" target="_blank"><i class="fas fa-file-alt"></i></a>
              {% else %}
                <i class="fas fa-file-alt disabled"></i>
              {% endif %}
              {% if p.bibtex_link %}
                <a href="{{ p.bibtex_link }}" target="_blank"><i class="fas fa-code"></i></a>
              {% else %}
                <i class="fas fa-code disabled"></i>
              {% endif %}
              {% if p.pdf_link %}
                <a href="{{ p.pdf_link }}" target="_blank"><i class="fas fa-file-pdf"></i></a>
              {% else %}
                {% assign pdfName = p.id | split: '-' | last | append: '.pdf' | prepend: '/pdfs/pdfs/pubs/' %}
                {% assign hasPdf = site.static_files | map:'path' | join:' ' | contains: pdfName %}
                {% if hasPdf %}
                  <a href="{{ pdfName }}" target="_blank"><i class="fas fa-file-pdf"></i></a>
                {% else %}
                  <i class="fas fa-file-pdf disabled"></i>
                {% endif %}
              {% endif %}
            </div>
          </li>
        {% endif %}
      {% endfor %}
      </ol>
    {% endfor %}
  </div>
{% endfor %}
</div>

<script>
function showPubType(type){
  document.querySelectorAll('.pub-type').forEach(function(div){
    if(div.id === 'pub-'+type){
      div.classList.add('active');
    } else {
      div.classList.remove('active');
    }
  });
  document.querySelectorAll('#pub-tabs li').forEach(function(li){
    if(li.id === 'tab-'+type){
      li.classList.add('active');
    } else {
      li.classList.remove('active');
    }
  });
}
</script>

