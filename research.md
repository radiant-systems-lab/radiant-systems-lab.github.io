---
layout: page
title: Research
description: Radiant's Research Projects
---

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- Page Heading -->
<h2 style="font-size:1.5rem; font-weight:700; margin-top:2rem;">
  <span style="border-bottom: 4px solid #FBBF24; padding-bottom: 0.25rem;">
    Research
  </span>
</h2>

<!-- Filter dropdown -->
<div class="pub-filter" style="margin-bottom: 2rem;">
  <label for="researchTypeFilter" style="font-weight: 500; margin-right: 0.5rem;">Filter by category:</label>
  <select id="researchTypeFilter" style="padding: 0.5rem 1rem; border: 1px solid #D1D5DB; border-radius: 0.375rem;">
    <option value="all">All</option>
    <option value="RAS">RAS</option>
    <option value="XAI">XAI</option>
    <option value="IAP">IAP</option>
  </select>
</div>

<!-- Section intro -->
<p style="margin-bottom: 1.5rem; font-size: 1rem; color: #4B5563;">
  <strong>Reproducible and Accountable Systems (RAS)</strong><br>
  Improving data-intensive, distributed, and parallel science workflows with reproducible and accountable containers.
</p>

<style>
  .research_subs {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .media {
    display: flex;
    flex-wrap: wrap;
    border: 1px solid #E5E7EB;
    border-radius: 0.375rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }
  .media-left {
    background: #F3F4F6;
    padding: 0;
    flex: 0 0 315px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .media-left img {
    width: 100%;
    height: auto;
    display: block;
  }
  .media-body {
    flex: 1;
    padding: 1.25rem;
  }
  .media-heading {
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.5rem;
  }
  .research_abstract {
    font-size: 0.95rem;
    color: #4B5563;
    margin-bottom: 0.75rem;
  }
  .research_citation {
    font-size: 0.875rem;
    color: #6B7280;
  }
  .research_citation a {
    color: #2563EB;
    font-weight: 500;
    text-decoration: none;
  }
  .research_citation a:hover {
    text-decoration: underline;
  }
</style>

<ul class="research_subs" id="research-list"> 
{% assign rs = site.data.research_ras | sort: 'year' | reverse %}
{% for r in rs limit:8 %}
  <li class="research-entry" data-type="{{ r.category }}">
    <div class="media">
      <div class="media-left">
        <a href="{{r.link}}">
          <img src="{{r.project_image}}" alt="{{r.project}}" class="card-img">
        </a>
      </div>
      <div class="media-body">
        <h4 class="media-heading">{{r.project}}</h4>
        <p class="research_abstract">{{r.abstract}}</p>
        <p class="research_citation">
          <strong>{{r.title}}. </strong>{{r.authors}}
          <strong><i>, {{r.publication}}</i></strong>, {{r.year}}. 
          <a href="{{r.link}}">Read More &raquo;</a>
        </p>
      </div>
    </div>
  </li>
{% endfor %}
</ul>

<script>
// Filter function
function showResearchType(type) {
  document.querySelectorAll('.research-entry').forEach(li => {
    li.style.display =
      (type === 'all' || li.getAttribute('data-type') === type)
        ? '' : 'none';
  });
}

// Wire up filter dropdown
document.getElementById("researchTypeFilter").addEventListener("change", (e) => {
  showResearchType(e.target.value);
});

// Default to All on page load
document.addEventListener('DOMContentLoaded', () => showResearchType('all'));
</script>
