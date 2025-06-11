---
layout: home
title: Home
group: navigation
rank: 0
---

<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.10";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>

<script async defer id="github-bjs" src="https://buttons.github.io/buttons.js"></script>

<p class="lead">
  The <a href="https://radiant-systems-lab.github.io/">Radiant Systems Lab</a> in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia</a> is dedicated to advancing the path from data to informed decisions across a wide range of domains. The Lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. It is directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> and member expertise spans machine learning, big data management, resource and system optimization,  data provenance and policy frameworks, scientific workflows, and DevOps solutions and practices. 

</p>

<p class="lead">

<!--
<a href="https://twitter.com/mu-radiant" class="twitter-follow-button" data-size="large" data-show-count="false" data-show-screen-name="false">Follow @uw_db</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<a href="https://medium.com/@mu-radiant"><img class="icon" src="https://cdn-images-1.medium.com/max/800/1*F6SrJR7_s95r6oCF3ugMZw.png" alt="follow mu-radiant on medium" title="follow mu-radiant on medium" height="24"/></a>
-->

<!--<a class="github-button" href="https://github.com/depaul-dice" 
  aria-label="Follow @depaul-dice on GitHub"></a> --> 
<a href="https://github.com/radiant-systems-lab" aria-label="Follow @radiant-systems-lab on GitHub"> <img src="https://s18955.pcdn.co/wp-content/uploads/2018/02/github.png" width="35"> </a>

</p>


## Recent News
<!-- see also news.markdown -->
<style>
#RecentNews li>p {display: inline;}
</style>
<ul id="RecentNews">
{% assign news = site.data.news | sort: 'date' | reverse %}
{% for n in news limit:8 %}
  <li>
   <span><b>{{ n.date | date: "%B %-d, %Y" }}</b></span>: {{ n.description | markdownify }}
  </li>
{% endfor %}
  <li>
   <a href="news.html">View all news</a>
  </li>
</ul>


## Current Projects

{% include current_projects %}

## Sponsors

<div height="50" class="flex-container logos images-container">
    <a href="https://offices.depaul.edu/research-services/Pages/default.aspx">
    <img src="{{ site.baseurl }}/images/depaul-logo.png" class="img-thumbnail" style="min-height:70px; height:70px;">
    </a>

    <a href="http://www.nsf.gov/">
    <img src="{{ site.baseurl }}/images/nsf-logo.png" class="img-thumbnail" style="min-height:70px; height:70px;">
    </a>

    <a href="http://www.bssw.io/">
    <img src="{{ site.baseurl }}/images/bssw-logo.png" class="img-thumbnail" style="min-height:70px; height:70px;">
    </a>

</div>
