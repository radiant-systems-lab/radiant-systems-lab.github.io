---
layout: page
title:  The Radiant Systems Lab
description: The  webpage of Radiant Systems Lab
keywords: machine learning, big data management, resource and system optimization,  data provenance and policy frameworks, scientific workflows, DevOps solutions and practices. 
---

<p>
The <a href="https://radiant-systems-lab.github.io/">Radiant Systems Lab</a> in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia</a> is dedicated to advancing the path from data to informed decisions across a wide range of domains. The Lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. It is directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> and member expertise spans machine learning, big data management, resource and system optimization,  data provenance and policy frameworks, scientific workflows, and DevOps solutions and practices.
</p>

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

<div class="navbarleft">
  <div class="navbar-inner">
      <ul class="nav">
          <li>news</li>
          <!--<li><a href="https://github.com/radiant-systems-lab">github</a></li>
          <li><a href="https://www.discord.com">discord</a></li>
          <li><a href="https://kn.org/blog">blog</a></li>-->
      </ul>
  </div>
</div>

<ul id="RecentNews">
{% assign news = site.data.news | sort: 'date' | reverse %}
{% for n in news limit:8 %}
  <li>
   <span><b>{{ n.date | date: "%B %-d, %Y" }}</b></span>: {{ n.description | markdownify }}
  </li>
{% endfor %}


<div class="navbar">
  <div class="navbar-inner">
      <ul class="nav">
          <li><a href="news.html">more news</a></li>
      </ul>
  </div>
</div>
