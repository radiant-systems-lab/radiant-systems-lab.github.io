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
        .media {
            box-sizing: border-box;
        }
        .media-left {
            background: rgb(211, 222, 234);
            vertical-align: middle;
            padding-left: 10px;
            padding-right: 10px;
            width: 315px;
            min-width: 315px;
            max-width: 315px;
            text-align: center;
            display: table-cell;
            unicode-bidi: isolate;
        }
    </style>
    <ul class="research_subs"> 
    {% assign rs = site.data.research_ras | sort: 'year' | reverse %}
    {% for r in rs limit:8 %}
        <div class="media">
            <div class="media-left">
                <a href="#">
                <img src="{{r.project_image}}" class="card-img" alt="{{r.project_image}}" style="width: 26em">
                </a>
            </div>
            <div class="media-body">
                <h4 class="media-heading">{{r.project}}</h4>
                <p>
                {{r.abstract}}</p>
                <p>
                <strong>{{r.title}}. </strong> {{r.authors}}  <strong><i>, {{r.publication}}</i></strong>, {{r.year}}. 
                <a class="btn btn-primary btn-xs" href="{{r.link}}" role="button">Paper</a>
                </p>
            </div>
        </div>
    {% endfor %}

