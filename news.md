---
layout: page
title: News
group: "navigation"
id: "news"
---

<style>
  /* News Highlight Styling */
  .news-highlight {
    font-weight: 700;
    color: #2c3e50;
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
  }
  .news-item a { font-weight: bold; text-decoration: underline; color: #0056b3; }
  .news-item-box { margin-bottom: 1.5rem; line-height: 1.6; }
</style>

<ul id="RecentNews" style="list-style: none; padding-left: 0;">
{% assign news_items = site.data.news | sort: "News.rank" | reverse %}
{% assign publications = site.data.single_data_source %}

{% for item in news_items %}
  {% assign n = item.News %}
  {% assign pub = nil %}
  {% if n.pubID %}
    {% assign pub_entry = publications | where: "id", n.pubID | first %}
    {% if pub_entry %}{% assign pub = pub_entry.Publication %}{% endif %}
  {% endif %}

  <li>
    <div class="news-item-box">
      <div class="news-item" style="font-size:0.95rem;">
        {% assign display_date = n.date %}
        {% if pub.date %}{% assign display_date = pub.date %}{% endif %}
        {% if display_date %}<span style="color: #666;">{{ display_date | date: "%B %-d, %Y" }}</span> — {% endif %}

        {% assign rendered = n.description %}

        {% comment %} 1. Publication Text Fields (No Quotes) {% endcomment %}
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

        {% comment %} 2. Publication Links (Standard Link) {% endcomment %}
        {% if pub.links %}
          {% for link_item in pub.links %}
            {% assign link_key = link_item[0] %}
            {% assign link_data = link_item[1] %}
            {% capture html_link %}<a href="{{ link_data.url }}" target="_blank">{{ link_data.text }}</a>{% endcapture %}
            {% capture lt1 %}[[PUB: {{ link_key }}]]{% endcapture %}{% capture lt2 %}[[PUB:{{ link_key }}]]{% endcapture %}
            {% assign rendered = rendered | replace: lt1, html_link | replace: lt2, html_link %}
          {% endfor %}
        {% endif %}

        {% comment %} 3. Remaining Manual [[Text]] (With Single Quotes) {% endcomment %}
        {% assign parts = rendered | split: "[[" %}
        {% assign rendered = parts[0] %}
        {% for part in parts offset: 1 %}
          {% assign subparts = part | split: "]]" %}
          {% capture manual_highlight %}<span class="news-highlight">'{{ subparts[0] }}'</span>{% endcapture %}
          {% assign rendered = rendered | append: manual_highlight | append: subparts[1] %}
        {% endfor %}

        {{ rendered | markdownify | replace: "<p>", "" | replace: "</p>", "" }}
      </div>
    </div>
  </li>
{% endfor %}
</ul>