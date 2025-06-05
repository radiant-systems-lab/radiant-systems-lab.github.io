---
layout: home
title: Home
group: "navigation"
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
The Data, Infrastructure, Computation, and Environments (DICE) Lab aims at expanding the understanding of issues relating to data, infrastructure, computational problems, and environments. The current focus is on provenance data, systems and infrastructure for computational reproducibility, optimization and decision problems arising within this data and systems, and exploration of a variety of virtual environments that are relevant for establishing computational reproducibility.
</p>

<p class="lead">

<!--
<a href="https://twitter.com/uw_db" class="twitter-follow-button" data-size="large" data-show-count="false" data-show-screen-name="false">Follow @uw_db</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<a href="https://medium.com/@uwdb"><img class="icon" src="https://cdn-images-1.medium.com/max/800/1*F6SrJR7_s95r6oCF3ugMZw.png" alt="follow uwdb on medium" title="follow uwdb on medium" height="24"/></a>
-->

<!--<a class="github-button" href="https://github.com/depaul-dice" 
  aria-label="Follow @depaul-dice on GitHub"></a> --> 
<a href="https://github.com/depaul-dice" aria-label="Follow @depaul-dice on GitHub"> <img src="https://s18955.pcdn.co/wp-content/uploads/2018/02/github.png" width="35"> </a>

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
