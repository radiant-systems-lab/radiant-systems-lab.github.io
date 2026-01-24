---
layout: page
title: News
group: "navigation"
id: "news"
---

<ul id="RecentNews">

{% assign news_items = site.data.single_data_source
  | where_exp: "i", "i.News"
  | sort: "News.rank" %}

{% for item in news_items %}
  {% assign n = item.News %}

  {%- comment -%}
  Skip individual news without description
  {%- endcomment -%}
  {% if item.entry_kind != "common" and n.description == nil %}
    {% continue %}
  {% endif %}

  <li>
    <div class="news-item-box">
      <div class="news-item" style="font-size: 0.9rem;">

        {% if n.date %}
          <strong>{{ n.date | date: "%B %-d, %Y" }}</strong> –
        {% endif %}

        {%- comment -%}
        Common entry defaulting logic (Liquid-safe)
        {%- endcomment -%}

        {% if item.entry_kind == "common" %}
          {% if n.description == nil or n.description == "" %}
            {% if item.Publication %}
              {% assign p = item.Publication %}
              We are pleased to share that the paper
              <a href="{{ p.link }}">{{ p.title }}</a>
              authored by {{ p.authors }} has been accepted at
              <a href="{{ p.journalLink }}">{{ p.journal }}</a>,
              {{ p.city }}, {{ p.country }}.
            {% endif %}
          {% else %}
            {{ n.description
               | markdownify
               | replace: "<p>", ""
               | replace: "</p>", "" }}
          {% endif %}
        {% else %}
          {{ n.description
             | markdownify
             | replace: "<p>", ""
             | replace: "</p>", "" }}
        {% endif %}

      </div>
    </div>
  </li>

{% endfor %}

</ul>
