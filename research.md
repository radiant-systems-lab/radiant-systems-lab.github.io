---
layout: page
---

<style>

/* ============================= */
/* HEADER (UNCHANGED STRUCTURE)  */
/* ============================= */

.research-header-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #ddd;
  margin-bottom: 1.5rem;
  padding-bottom: 0.4rem;
}

.research-main-title {
  margin: 0;
  color: #444a84;
  font-size: 2rem;
  font-weight: 700;
}

.research-tabs {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
}

.research-tabs li a {
  text-decoration: none;
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
}

.research-tabs li a.active-link {
  color: #444a84;
  font-weight: 700;
  border-bottom: 3px solid #6b21a8;
  padding-bottom: 6px;
}

/* ============================= */
/* SECTION CONTROL               */
/* ============================= */

.research-section { display: none; }
.research-section.active { display: block; }

.cat-title {
  color: #6b21a8;
  margin-bottom: 0.3rem;
  font-size: 1.6rem;
}

.cat-desc {
  font-style: italic;
  color: #555;
  margin-bottom: 2rem;
  font-size: 1.2rem;
}

/* ============================= */
/* EXACT CARD STYLE (MATCH IMAGE)*/
/* ============================= */

.pub-container {
  display: flex;
  border: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
  background: #ffffff;
  min-height: 260px;   /* controls card height */
}

.pub-image-box {
  width: 300px;
  min-width: 300px;
  background: #d9e1ea;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

/* CONTROL HEIGHT PROPERLY */
.pub-image-box img {
  height: 70%;        /* ← controls how much vertical space it takes */
  width: auto;
  object-fit: contain;
}

/* RIGHT PANEL */
.pub-details {
  padding: 20px 25px;
  flex: 1;
  background: #ffffff;
  border-left: 1px solid #e5e5e5;
}

/* TITLE SMALLER */
.pub-details h3 {
  margin: 0 0 10px 0;
  color: #444a84;
  font-size: 1.3rem;
  font-weight: 700;
  line-height: 1.3;
}

/* LIMIT ABSTRACT HEIGHT */
.pub-abstract {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #333;
  margin-bottom: 12px;

  display: -webkit-box;
  -webkit-line-clamp: 6;   /* number of lines shown */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Citation block */
.pub-citation {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #444;
}

/* Title inside citation */
.pub-citation strong {
  color: #333;
}

/* Read more link */
.pub-link {
  color: #337ab7;
  text-decoration: none;
  margin-left: 6px;
}

.pub-link:hover {
  text-decoration: underline;
}

</style>


<div class="research-header-row">
  <h1 class="research-main-title">Research</h1>
  <ul class="research-tabs">
    {% for cat in site.data.research_categories %}
      <li><a href="#{{ cat[0] }}" id="link-{{ cat[0] }}">{{ cat[0] }}</a></li>
    {% endfor %}
  </ul>
</div>

{% assign publications = site.data.single_data_source %}
{% assign research_groups = site.data.research %}

{% for cat in site.data.research_categories %}
  {% assign cat_id = cat[0] %}
  <section id="{{ cat_id }}" class="research-section">
    <h2 class="cat-title">{{ cat[1].title }}</h2>
    <p class="cat-desc">{{ cat[1].description }}</p>

    {% if research_groups[cat_id] %}
      {% assign items = research_groups[cat_id] | sort: "Research.rank" | reverse %}
      
      {% for item in items %}
        {% assign target_id = item.Research.pubID %}
        {% assign found_pub = nil %}

        {% for p in publications %}
          {% if p.id == target_id %}
            {% assign found_pub = p.Publication %}
            {% break %}
          {% endif %}
        {% endfor %}

        {% if found_pub %}
          <div class="pub-container">
            <div class="pub-image-box">
              {% if found_pub.image and found_pub.image != "" %}
                <img src="{{ found_pub.image }}" alt="Figure">
              {% else %}
                <div style="color:#ccc; font-weight:bold; font-size:10px;">IMAGE PLACEHOLDER</div>
              {% endif %}
            </div>
            <div class="pub-details">
              <h3>{{ found_pub.title }}</h3>
              
              <div class="pub-abstract">
                {{ found_pub.abstract }}
              </div>

              <div class="pub-citation">
                <strong>{{ found_pub.title }}.</strong> 
                {{ found_pub.authors }}. 
                <i>{{ found_pub.journal }}</i>, 
                {{ found_pub.year }}. 
                {% if found_pub.links.PDF %}
                  <a href="{{ found_pub.links.PDF.url }}" class="pub-link">Read More >></a>
                {% endif %}
              </div>
            </div>
          </div>
        {% endif %}
      {% endfor %}
    {% else %}
      <p>Data content for this category is currently being updated.</p>
    {% endif %}
  </section>
{% endfor %}

<script>
function route() {
  const hash = window.location.hash.replace("#", "");
  const first = "{{ site.data.research_categories | first | first }}";
  const active = hash || first;
  
  document.querySelectorAll(".research-section").forEach(s => {
    s.classList.toggle("active", s.id === active);
  });
  document.querySelectorAll(".research-tabs a").forEach(a => {
    a.classList.toggle("active-link", a.getAttribute("href") === "#" + active);
  });
}
window.addEventListener("hashchange", route);
document.addEventListener("DOMContentLoaded", route);
</script>