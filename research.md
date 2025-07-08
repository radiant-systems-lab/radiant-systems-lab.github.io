---
layout: page
title: research
description: Radiant's Research Projects 
---

<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="#" style="text-decoration: underline;">RAS</a></li>
            <li><a href="https://radiant-systems-lab.github.io/research_xai.html">XAI</a></li>
            <li><a href="https://radiant-systems-lab.github.io/research_iap.html">IAP</a></li>
        </ul>
    </div>
</div>

**Reproducible and Accountable Systems (RAS)**
Improving data-intensive, distributed, and parallel science workflows with reproducible and accountable containers.

<div>
    <style>
    </style>
    <ul class="research_subs"> 
    {% assign rs = site.data.research_ras | sort: 'date' | reverse %}
    {% for r in rs limit:8 %}
    <li class="news-font">
    <span><b>{{ r.date | date: "%B %-d, %Y" }}</b></span>: {{ r.description | markdownify }}
    </li>
    {% endfor %}
</div>

---
