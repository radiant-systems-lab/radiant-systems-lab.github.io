---
layout: page
title: research
description: Radiant's Research Projects 
---

<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="https://github.com/radiant-systems-lab/ras">RAS</a></li>
            <li><a href="xai">XAI</a></li>
            <li><a href="iap">IAP</a></li>
        </ul>
    </div>
</div>

<div>
    <ul id="ResearchRAS">
    {% assign researches = site.data.reasearch_ras | sort: 'date' | reverse %}
    {% for r in researches %}
      <li>
       <span><b>{{ r.date | date: "%B %-d, %Y" }}</b></span>: {{ r.description | markdownify }}
      </li>
    {% endfor %}
    </ul>
</div>

---
