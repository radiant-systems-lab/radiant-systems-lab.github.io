---
layout: page
title:  The Radiant Systems Lab
description: The  webpage of Radiant Systems Lab
keywords: machine learning, big data management, resource and system optimization,  data provenance and policy frameworks, scientific workflows, DevOps solutions and practices. 
---

<div id="index_mission" class="container">
    <div class="image-placeholder"></div>
    <div class="text-section">
      <h3 class="section-title">
          Our Mission
          <span class="underline"></span>
      </h3>
      <p>
          The <a href="https://radiant-systems-lab.github.io/">Radiant Systems Lab</a> in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia</a> is dedicated to advancing the path from data to informed decisions across a wide range of domains. The Lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. It is directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> and member expertise spans machine learning, big data management, resource and system optimization,  data provenance and policy frameworks, scientific workflows, and DevOps solutions and practices.
      </p>
    </div>
</div>

<!--<table class="wide">
<tr>
  <td class="left">
    <a href="publpics/rqtl2_fig1.html">
        <img src="publpics/rqtl2_fig1c.png" alt="Broman et al. (2019) Fig 1c" title="Broman et al. (2019) Fig 1c"/>
    </a>
  </td>
  <td class="right">
    <a href="publpics/mppdiag_fig4.html">
        <img src="publpics/mppdiag_fig4.png" alt="Broman et
        al. (2019) Fig 4" title="Broman et al. (2019) Fig 4"/>
    </a>
  </td>
</tr>
<tr>
  <td class="left">
    <a href="publpics/samplemixups_fig7.html">
        <img src="publpics/samplemixups_fig7.png" alt="Broman et al. (2015) Fig 7" title="Broman et al. (2015) Fig 7"/>
    </a>
  </td>
  <td class="right">
    <a href="publpics/mbmixups_fig3.html">
        <img src="publpics/mbmixups_fig3.png" alt="Lobo et al. (2021) Fig 3" title="Lobo et al. (2021) Fig 3"/>
    </a>
  </td>
</tr>
</table>
-->

<h3 class="news-heading">Recent News</h3>
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

<div style="text-align: right; margin-top: 10px;">
  <a class="home-button" href="news.html">More News →</a>
</div>

<div id="index_research_areas" class="container">
  <div class="left-panel">
    <h2 class="section-title">Research Areas <span class="underline"></span></h2>
    <div class="image-placeholder"></div>
    <p class="description">
      Explore our six key research areas that define Radiant Lab’s expertise and innovation.
    </p>
  </div>
  <div class="right-panel">
    <div class="accordion">
      <!-- JavaScript will populate this -->
    </div>
  </div>
</div>
