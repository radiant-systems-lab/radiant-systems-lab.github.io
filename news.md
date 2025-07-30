---
layout: page
title: News
group: "navigation"
id: "news"
---

<!-- see also index.markdown -->
<h3 class="news-heading">News</h3>
<ul id="RecentNews">
{% assign news = site.data.news | sort: 'date' | reverse %}
{% for n in news limit:8 %}
  <li>
    <div class="news-item-box">
      <div class="news-item" style="font-size: 0.9rem;">
        <strong>{{ n.date | date: "%B %-d, %Y" }}</strong> - {{ n.description | markdownify | replace: "<p>", "" | replace: "</p>", "" }}
      </div>
    </div>
  </li>
{% endfor %}
</ul>
