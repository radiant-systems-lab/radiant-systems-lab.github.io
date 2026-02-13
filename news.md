---
layout: page
title: News
group: "navigation"
id: "news"
---

<div class="page-news">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-regular fa-newspaper"></i> News</h2>
      <p class="page-subtitle">Latest updates, publications, and milestones from the Radiant Systems Lab.</p>
    </div>
  </div>

  <section class="news-section" id="news-feed">
    <h2 class="news-section-title"><i class="fa-solid fa-bullhorn"></i> Recent News</h2>
    <ul id="RecentNews" class="news-feed-list">
      {% assign news_items = site.data.news | sort: "News.rank" | reverse %}
      {% assign publications = site.data.single_data_source %}

      {% for item in news_items %}
        {% assign n = item.News %}
        {% assign pub = nil %}
        {% if n.pubID %}
          {% assign pub_entry = publications | where: "id", n.pubID | first %}
          {% if pub_entry %}{% assign pub = pub_entry.Publication %}{% endif %}
        {% endif %}

        <li class="news-feed-item">
          <article class="news-card">
            {% assign display_date = n.date %}
            {% if pub.date %}{% assign display_date = pub.date %}{% endif %}
            {% if display_date %}
              <div class="news-card-date">
                <i class="fa-regular fa-calendar"></i>
                <time datetime="{{ display_date | date: "%Y-%m-%d" }}">{{ display_date | date: "%B %-d, %Y" }}</time>
              </div>
            {% endif %}

            {% assign rendered = n.description %}

            {% comment %} 1. Publication text field placeholders {% endcomment %}
            {% if pub %}
              {% for field in pub %}
                {% assign key = field[0] %}
                {% if key != "links" and key != "categories" %}
                  {% capture wrapped_val %}<span class="news-highlight">{{ field[1] }}</span>{% endcapture %}
                  {% capture t1 %}[[PUB: {{ key }}]]{% endcapture %}{% capture t2 %}[[PUB:{{ key }}]]{% endcapture %}
                  {% assign rendered = rendered | replace: t1, wrapped_val | replace: t2, wrapped_val %}
                {% endif %}
              {% endfor %}
            {% endif %}

            {% comment %} 2. Publication link placeholders {% endcomment %}
            {% if pub.links %}
              {% for link_item in pub.links %}
                {% assign link_key = link_item[0] %}
                {% assign link_data = link_item[1] %}
                {% capture html_link %}<a href="{{ link_data.url }}" target="_blank">{{ link_data.text }}</a>{% endcapture %}
                {% capture lt1 %}[[PUB: {{ link_key }}]]{% endcapture %}{% capture lt2 %}[[PUB:{{ link_key }}]]{% endcapture %}
                {% assign rendered = rendered | replace: lt1, html_link | replace: lt2, html_link %}
              {% endfor %}
            {% endif %}

            {% comment %} 3. Remaining manual [[text]] placeholders {% endcomment %}
            {% assign parts = rendered | split: "[[" %}
            {% assign rendered = parts[0] %}
            {% for part in parts offset: 1 %}
              {% assign subparts = part | split: "]]" %}
              {% capture manual_highlight %}<span class="news-highlight">{{ subparts[0] }}</span>{% endcapture %}
              {% assign rendered = rendered | append: manual_highlight | append: subparts[1] %}
            {% endfor %}

            <div class="news-content">
              {{ rendered | markdownify | replace: "<p>", "" | replace: "</p>", "" }}
            </div>
          </article>
        </li>
      {% endfor %}
    </ul>
  </section>
</div>
