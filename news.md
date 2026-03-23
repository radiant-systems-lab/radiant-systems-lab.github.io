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
                {% assign key_downcase = key | downcase %}
                {% assign key_capitalized = key_downcase | capitalize %}
                {% if key != "links" and key != "categories" %}
                  {% capture wrapped_val %}<span class="news-highlight">{{ field[1] }}</span>{% endcapture %}
                  {% capture t1 %}[[PUB: {{ key }}]]{% endcapture %}{% capture t2 %}[[PUB:{{ key }}]]{% endcapture %}
                  {% capture t3 %}[[PUB: {{ key_downcase }}]]{% endcapture %}{% capture t4 %}[[PUB:{{ key_downcase }}]]{% endcapture %}
                  {% capture t5 %}[[PUB: {{ key_capitalized }}]]{% endcapture %}{% capture t6 %}[[PUB:{{ key_capitalized }}]]{% endcapture %}
                  {% assign rendered = rendered | replace: t1, wrapped_val | replace: t2, wrapped_val | replace: t3, wrapped_val | replace: t4, wrapped_val | replace: t5, wrapped_val | replace: t6, wrapped_val %}
                {% endif %}
              {% endfor %}
            {% endif %}

            {% comment %} 2. Publication link placeholders, including nested access like [[PUB:links:title]] {% endcomment %}
            {% if pub.links %}
              {% for link_item in pub.links %}
                {% assign link_key = link_item[0] %}
                {% assign link_key_downcase = link_key | downcase %}
                {% assign link_key_capitalized = link_key_downcase | capitalize %}
                {% assign link_data = link_item[1] %}
                {% capture html_link %}<a href="{{ link_data.url }}" target="_blank" rel="noopener noreferrer">{{ link_data.text }}</a>{% endcapture %}
                {% capture lt1 %}[[PUB: {{ link_key }}]]{% endcapture %}{% capture lt2 %}[[PUB:{{ link_key }}]]{% endcapture %}
                {% capture lt3 %}[[PUB: {{ link_key_downcase }}]]{% endcapture %}{% capture lt4 %}[[PUB:{{ link_key_downcase }}]]{% endcapture %}
                {% capture lt5 %}[[PUB: {{ link_key_capitalized }}]]{% endcapture %}{% capture lt6 %}[[PUB:{{ link_key_capitalized }}]]{% endcapture %}
                {% capture n1 %}[[PUB:links:{{ link_key }}]]{% endcapture %}{% capture n2 %}[[PUB: links:{{ link_key }}]]{% endcapture %}
                {% capture n3 %}[[PUB:links: {{ link_key }}]]{% endcapture %}{% capture n4 %}[[PUB: links: {{ link_key }}]]{% endcapture %}
                {% capture n5 %}[[PUB:links:{{ link_key_downcase }}]]{% endcapture %}{% capture n6 %}[[PUB: links:{{ link_key_downcase }}]]{% endcapture %}
                {% capture n7 %}[[PUB:links: {{ link_key_downcase }}]]{% endcapture %}{% capture n8 %}[[PUB: links: {{ link_key_downcase }}]]{% endcapture %}
                {% capture n9 %}[[PUB:links:{{ link_key_capitalized }}]]{% endcapture %}{% capture n10 %}[[PUB: links:{{ link_key_capitalized }}]]{% endcapture %}
                {% capture n11 %}[[PUB:links: {{ link_key_capitalized }}]]{% endcapture %}{% capture n12 %}[[PUB: links: {{ link_key_capitalized }}]]{% endcapture %}
                {% assign rendered = rendered | replace: lt1, html_link | replace: lt2, html_link | replace: lt3, html_link | replace: lt4, html_link | replace: lt5, html_link | replace: lt6, html_link | replace: n1, html_link | replace: n2, html_link | replace: n3, html_link | replace: n4, html_link | replace: n5, html_link | replace: n6, html_link | replace: n7, html_link | replace: n8, html_link | replace: n9, html_link | replace: n10, html_link | replace: n11, html_link | replace: n12, html_link %}

                {% if link_data.text %}
                  {% capture nt1 %}[[PUB:links:{{ link_key }}:text]]{% endcapture %}{% capture nt2 %}[[PUB: links:{{ link_key }}:text]]{% endcapture %}
                  {% capture nt3 %}[[PUB:links: {{ link_key }}:text]]{% endcapture %}{% capture nt4 %}[[PUB: links: {{ link_key }}:text]]{% endcapture %}
                  {% capture nt5 %}[[PUB:links:{{ link_key_downcase }}:text]]{% endcapture %}{% capture nt6 %}[[PUB: links:{{ link_key_downcase }}:text]]{% endcapture %}
                  {% capture nt7 %}[[PUB:links: {{ link_key_downcase }}:text]]{% endcapture %}{% capture nt8 %}[[PUB: links: {{ link_key_downcase }}:text]]{% endcapture %}
                  {% capture nt9 %}[[PUB:links:{{ link_key_capitalized }}:text]]{% endcapture %}{% capture nt10 %}[[PUB: links:{{ link_key_capitalized }}:text]]{% endcapture %}
                  {% capture nt11 %}[[PUB:links: {{ link_key_capitalized }}:text]]{% endcapture %}{% capture nt12 %}[[PUB: links: {{ link_key_capitalized }}:text]]{% endcapture %}
                  {% assign rendered = rendered | replace: nt1, link_data.text | replace: nt2, link_data.text | replace: nt3, link_data.text | replace: nt4, link_data.text | replace: nt5, link_data.text | replace: nt6, link_data.text | replace: nt7, link_data.text | replace: nt8, link_data.text | replace: nt9, link_data.text | replace: nt10, link_data.text | replace: nt11, link_data.text | replace: nt12, link_data.text %}
                {% endif %}

                {% if link_data.url %}
                  {% capture nu1 %}[[PUB:links:{{ link_key }}:url]]{% endcapture %}{% capture nu2 %}[[PUB: links:{{ link_key }}:url]]{% endcapture %}
                  {% capture nu3 %}[[PUB:links: {{ link_key }}:url]]{% endcapture %}{% capture nu4 %}[[PUB: links: {{ link_key }}:url]]{% endcapture %}
                  {% capture nu5 %}[[PUB:links:{{ link_key_downcase }}:url]]{% endcapture %}{% capture nu6 %}[[PUB: links:{{ link_key_downcase }}:url]]{% endcapture %}
                  {% capture nu7 %}[[PUB:links: {{ link_key_downcase }}:url]]{% endcapture %}{% capture nu8 %}[[PUB: links: {{ link_key_downcase }}:url]]{% endcapture %}
                  {% capture nu9 %}[[PUB:links:{{ link_key_capitalized }}:url]]{% endcapture %}{% capture nu10 %}[[PUB: links:{{ link_key_capitalized }}:url]]{% endcapture %}
                  {% capture nu11 %}[[PUB:links: {{ link_key_capitalized }}:url]]{% endcapture %}{% capture nu12 %}[[PUB: links: {{ link_key_capitalized }}:url]]{% endcapture %}
                  {% assign rendered = rendered | replace: nu1, link_data.url | replace: nu2, link_data.url | replace: nu3, link_data.url | replace: nu4, link_data.url | replace: nu5, link_data.url | replace: nu6, link_data.url | replace: nu7, link_data.url | replace: nu8, link_data.url | replace: nu9, link_data.url | replace: nu10, link_data.url | replace: nu11, link_data.url | replace: nu12, link_data.url %}
                {% endif %}
              {% endfor %}
            {% endif %}

            {% comment %} 2b. Fallback for [[PUB:links:title]] when there is no dedicated title link {% endcomment %}
            {% assign title_link_url = nil %}
            {% assign title_link_text = nil %}
            {% if pub.links.title and pub.links.title.url %}
              {% assign title_link_url = pub.links.title.url %}
              {% assign title_link_text = pub.links.title.text | default: pub.title %}
            {% elsif pub.links.Title and pub.links.Title.url %}
              {% assign title_link_url = pub.links.Title.url %}
              {% assign title_link_text = pub.links.Title.text | default: pub.title %}
            {% elsif pub.links.PDF and pub.links.PDF.url %}
              {% assign title_link_url = pub.links.PDF.url %}
              {% assign title_link_text = pub.title %}
            {% elsif pub.links.pdf and pub.links.pdf.url %}
              {% assign title_link_url = pub.links.pdf.url %}
              {% assign title_link_text = pub.title %}
            {% endif %}

            {% if title_link_url and title_link_text %}
              {% capture fallback_title_link %}<a href="{{ title_link_url }}" target="_blank" rel="noopener noreferrer">{{ title_link_text }}</a>{% endcapture %}
              {% capture ft1 %}[[PUB:links:title]]{% endcapture %}{% capture ft2 %}[[PUB: links:title]]{% endcapture %}
              {% capture ft3 %}[[PUB:links: title]]{% endcapture %}{% capture ft4 %}[[PUB: links: title]]{% endcapture %}
              {% capture ft5 %}[[PUB:links:Title]]{% endcapture %}{% capture ft6 %}[[PUB: links:Title]]{% endcapture %}
              {% capture ft7 %}[[PUB:links: Title]]{% endcapture %}{% capture ft8 %}[[PUB: links: Title]]{% endcapture %}
              {% assign rendered = rendered | replace: ft1, fallback_title_link | replace: ft2, fallback_title_link | replace: ft3, fallback_title_link | replace: ft4, fallback_title_link | replace: ft5, fallback_title_link | replace: ft6, fallback_title_link | replace: ft7, fallback_title_link | replace: ft8, fallback_title_link %}

              {% capture ftt1 %}[[PUB:links:title:text]]{% endcapture %}{% capture ftt2 %}[[PUB: links:title:text]]{% endcapture %}
              {% capture ftt3 %}[[PUB:links: title:text]]{% endcapture %}{% capture ftt4 %}[[PUB: links: title:text]]{% endcapture %}
              {% capture ftt5 %}[[PUB:links:Title:text]]{% endcapture %}{% capture ftt6 %}[[PUB: links:Title:text]]{% endcapture %}
              {% capture ftt7 %}[[PUB:links: Title:text]]{% endcapture %}{% capture ftt8 %}[[PUB: links: Title:text]]{% endcapture %}
              {% assign rendered = rendered | replace: ftt1, title_link_text | replace: ftt2, title_link_text | replace: ftt3, title_link_text | replace: ftt4, title_link_text | replace: ftt5, title_link_text | replace: ftt6, title_link_text | replace: ftt7, title_link_text | replace: ftt8, title_link_text %}

              {% capture ftu1 %}[[PUB:links:title:url]]{% endcapture %}{% capture ftu2 %}[[PUB: links:title:url]]{% endcapture %}
              {% capture ftu3 %}[[PUB:links: title:url]]{% endcapture %}{% capture ftu4 %}[[PUB: links: title:url]]{% endcapture %}
              {% capture ftu5 %}[[PUB:links:Title:url]]{% endcapture %}{% capture ftu6 %}[[PUB: links:Title:url]]{% endcapture %}
              {% capture ftu7 %}[[PUB:links: Title:url]]{% endcapture %}{% capture ftu8 %}[[PUB: links: Title:url]]{% endcapture %}
              {% assign rendered = rendered | replace: ftu1, title_link_url | replace: ftu2, title_link_url | replace: ftu3, title_link_url | replace: ftu4, title_link_url | replace: ftu5, title_link_url | replace: ftu6, title_link_url | replace: ftu7, title_link_url | replace: ftu8, title_link_url %}
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
