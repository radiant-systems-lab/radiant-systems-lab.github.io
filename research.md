---
layout: page
---

<div class="page-research">
  <div class="research-header-row">
    <div class="research-heading-block">
      <h1 class="research-main-title"><i class="fa-solid fa-microscope"></i> Research</h1>
      <p class="research-subtitle">Select an area to view related projects and publications.</p>
    </div>
    <div class="research-tabs-wrap" aria-label="Research areas">
      <ul class="research-tabs">
        {% for cat in site.data.research_categories %}
          <li><a href="#{{ cat[0] }}" id="link-{{ cat[0] }}">{{ cat[0] }}</a></li>
        {% endfor %}
      </ul>
    </div>
  </div>

  {% assign publications = site.data.single_data_source %}
  {% assign research_groups = site.data.research %}

  {% for cat in site.data.research_categories %}
    {% assign cat_id = cat[0] %}
    <section id="{{ cat_id }}" class="research-section">
      <h2 class="cat-title"><i class="fa-solid fa-layer-group"></i> {{ cat[1].title }}</h2>
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
            <article class="pub-container">
              <div class="pub-image-box">
                {% if found_pub.image and found_pub.image != "" %}
                  <img src="{{ found_pub.image }}" alt="Figure for {{ found_pub.title }}">
                {% else %}
                  <div class="pub-image-placeholder"><i class="fa-regular fa-image"></i> Figure</div>
                {% endif %}
              </div>
              <div class="pub-details">
                <h3>{{ found_pub.title }}</h3>

                <div class="pub-abstract">
                  {{ found_pub.abstract }}
                </div>

                <div class="pub-citation">
                  {% if found_pub.authors %}
                    <div class="citation-row"><i class="fa-solid fa-users"></i> {{ found_pub.authors }}</div>
                  {% endif %}
                  {% if found_pub.journal %}
                    <div class="citation-row"><i class="fa-regular fa-newspaper"></i> <em>{{ found_pub.journal }}</em></div>
                  {% endif %}
                  {% if found_pub.year %}
                    <div class="citation-row"><i class="fa-regular fa-calendar"></i> {{ found_pub.year }}</div>
                  {% endif %}
                </div>

                {% if found_pub.links.PDF %}
                  <a href="{{ found_pub.links.PDF.url }}" class="pub-link" target="_blank" rel="noopener noreferrer">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Read Publication
                  </a>
                {% endif %}
              </div>
            </article>
          {% endif %}
        {% endfor %}
      {% else %}
        <p>Data content for this category is currently being updated.</p>
      {% endif %}
    </section>
  {% endfor %}
</div>

<script>
function routeResearchTabs() {
  const links = Array.from(document.querySelectorAll(".research-tabs a"));
  const sections = Array.from(document.querySelectorAll(".research-section"));
  const first = "{{ site.data.research_categories | first | first }}";
  const hash = window.location.hash.replace("#", "");
  const validIds = new Set(sections.map(s => s.id));
  const active = validIds.has(hash) ? hash : first;

  sections.forEach(s => {
    s.classList.toggle("active", s.id === active);
  });

  links.forEach(a => {
    const isActive = a.getAttribute("href") === "#" + active;
    a.classList.toggle("active-link", isActive);
    a.setAttribute("aria-current", isActive ? "true" : "false");
  });
}

window.addEventListener("hashchange", routeResearchTabs);
document.addEventListener("DOMContentLoaded", routeResearchTabs);
</script>
