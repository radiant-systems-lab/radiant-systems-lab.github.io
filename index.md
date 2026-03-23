---
layout: page
title: The Radiant Systems Lab
description: The webpage of Radiant Systems Lab
---

<div class="index-header-row" style="display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 10px; border-bottom: 1px solid #eee; margin-bottom: 15px;">
  <div class="index-heading-block">
    <h2 class="index-page-title" style="margin: 0; border: none; padding: 0; line-height: 1; font-weight: bold;">
      <span class="index-title-word word-1">The</span>
      <span class="index-title-word word-2">Radiant</span>
      <span class="index-title-word word-3">Systems</span>
      <span class="index-title-word word-4">Lab</span>
    </h2>
    <p class="page-subtitle index-page-subtitle">Advancing reproducible, scalable, and trustworthy data-driven systems.</p>
  </div>
  <div class="quick-jump-links" style="font-size: 0.9rem;">
    <a href="#recent-news-section" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">Recent News</a>
    <a href="#research-areas-section" style="font-weight: bold; text-decoration: none; color: #0088cc;">Research Areas</a>
  </div>
</div>

<style>
  /* Clean up theme defaults */
  .page-header { display: none !important; }
  .content { padding-top: 0 !important; }
  h2 { border-bottom: none !important; }

  /* News Highlight Styling */
  .news-highlight {
    font-weight: 700;
    color: #2c3e50;
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
  }
  .news-item a { font-weight: bold; text-decoration: underline; color: #0056b3; }
  .news-item-box { margin-bottom: 0.8rem; line-height: 1.4; }

  /* Research Area Styling */
  #index_research_areas .image-placeholder {
    height: auto !important;
    overflow: visible !important;
    margin-bottom: 15px;
  }
  #research-main-img {
    width: 100%;
    height: auto !important;
    display: block;
    border-radius: 4px;
    transition: opacity 0.3s ease;
  }
</style>

<div id="index_mission" class="container" style="margin-top: 10px; padding-top: 0;">
  <div class="image-placeholder">
    <div class="custom-carousel">
      <div class="carousel-images" id="carousel-images">
        <img src="https://live.staticflickr.com/8790/16890371568_c5bcc96644_b.jpg" alt="University of Missouri campus building" />
        <img src="https://showme.missouri.edu/wp-content/uploads/2022/01/011922JesseHall1.jpg" alt="Jesse Hall at the University of Missouri" />
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/72/University_of_Missouri_-_Memorial_Union.jpg" alt="University of Missouri Memorial Union" />
      </div>
      <div class="carousel-buttons">
        <button type="button" onclick="prevSlide()" aria-label="Show previous slide">&#8249;</button>
        <button type="button" onclick="nextSlide()" aria-label="Show next slide">&#8250;</button>
      </div>
      <div class="carousel-dots" id="carousel-dots" role="tablist" aria-label="Mission carousel slides">
        <button type="button" onclick="goToSlide(0)" aria-label="Go to slide 1"></button>
        <button type="button" onclick="goToSlide(1)" aria-label="Go to slide 2"></button>
        <button type="button" onclick="goToSlide(2)" aria-label="Go to slide 3"></button>
      </div>
    </div>
  </div>

  <div class="text-section">
    <h3 class="section-title" style="margin-top: 0; color: #403F85;">Our Mission</h3>
    <p>
      The <a href="https://radiant-systems-lab.github.io/">Radiant Systems Lab</a> in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia</a> is dedicated to advancing the path from data to informed decisions across a wide range of domains. The Lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. It is directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> and member expertise spans machine learning, big data management, resource and system optimization, data provenance and policy frameworks, scientific workflows, and DevOps solutions and practices.
    </p>
  </div>
</div>

<h3 id="recent-news-section" class="news-heading" style="margin-top: 5px; margin-bottom: 10px; color: #403F85;">Recent News</h3>

<ul id="RecentNews" style="list-style: none; padding-left: 0; margin-bottom: 2px;">
{% assign publications = site.data.single_data_source %}
{% assign sorted_news = site.data.news | sort: "id" | reverse %}
{% for item in sorted_news limit: 8 %}
  {% assign n = item.News %}
  {% assign pub = nil %}
  {% if n.pubID %}
    {% assign pub_entry = publications | where: "id", n.pubID | first %}
    {% if pub_entry %}{% assign pub = pub_entry.Publication %}{% endif %}
  {% endif %}
  <li>
    <div class="news-item-box">
      <div class="news-item" style="font-size: 0.9rem;">
        {% assign display_date = n.date %}
        {% if pub.date %}{% assign display_date = pub.date %}{% endif %}
        {% if display_date %}<span style="color: #666;">{{ display_date | date: "%B %-d, %Y" }}</span> — {% endif %}
        
        {% assign rendered = n.description %}
        
        {% comment %} 1. Handle Publication Text Fields (No Quotes) {% endcomment %}
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

        {% comment %} 2. Handle Publication Links, including nested access like [[PUB:links:title]] {% endcomment %}
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

        {% comment %} 3. Handle Remaining Manual [[Text]] (With Single Quotes) {% endcomment %}
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

<div style="text-align: right; margin-bottom: 2px;">
  <a class="home-button" href="news.html" style="font-size: 0.85rem;">More News &rarr;</a>
</div>

<div id="research-areas-section" style="margin-top: 5px;">
  <div id="index_research_areas" class="container" style="width: 100%; max-width: 1100px; padding-top: 0;">
    <h3 class="section-title" style="margin-top: 0; color: #403F85;">Research Areas</h3>
    <div class="left-panel">
      <div class="image-placeholder">
          <img id="research-main-img" src="/images/research/Research_Area_Default.png" alt="Research Area Image">
      </div>
      <p class="description">Explore our five key research areas that define Radiant Lab’s expertise and innovation.</p>
    </div>
    <div class="right-panel">
      <div class="accordion"></div>
    </div>
  </div>
</div>

<script src="/assets/themes/twitter/js/index_research_areas.js"></script>

<!--<script src="https://radiant-systems-lab.github.io/assets/themes/twitter/js/index_research_areas.js"></script>-->


