---
layout: page
title: flexiflow
permalink: /softwares/floability/
---


<!-- Navigation Bar -->
<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="#about">about</a></li>
            <li><a href="#docs">docs</a></li>
            <li><a href="#code">code</a></li>
            <li><a href="#papers">papers</a></li>
            <li><a href="#team">team</a></li>
            <li><a href="#collaborators">collaborators</a></li>
        </ul>
    </div>
</div>


## about

**FlexiFlow** is a new programming model that is aimed at automatic model switching to maximise performance in machine learning workflows.

<div style="display: flex; align-items: flex-start; gap: 2em; margin: 0.2em 0; flex-wrap: wrap; font-size: 20px;">
  <div style="flex: 2 1 350px; min-width: 250px;">
    <p>With the increasing use of machine learning in production systems, engineers often encounter practical problems in deploying and maintaining ML models and workflows. A recurring concern is the issue of soft failures—situations where the model does not crash but delivers incorrect or degraded predictions, often due to factors like data drift. These soft failures compromise prediction accuracy and, in turn, the overall effectiveness of the deployed system. When workflows consist of multiple steps and models, such degradations must be promptly identified and addressed. Developers commonly rely on trace logs to identify problematic data batches, but exhaustively testing alternative model configurations is resource-intensive and time-consuming.</p>

    <p>In practice, only one single model is typically selected for each step based on evaluation over training data. However, this static selection often fails to maintain high accuracy across all real-world inputs during deployment. If a single model underperforms, the entire workflow may need to be re-executed from the beginning with an alternative model, significantly increasing the management burden and latency.</p>
  </div>
  <div style="flex: 1 1 250px; min-width: 200px; text-align: center;">
    <img src="/images/softwares/FlexiFlow-Arch.png" alt="FlexiFlow Architecture Diagram" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <div style="color:#444; margin-top:0.5em; font-style:italic;">FlexiFlow Architecture</div>
  </div>
</div>

As a solution we introduce <strong>FlexiFlow</strong>, a dataflow system that dynamically switches between alternate models when the current model exhibits low accuracy.

**FlexiFlow** learns to rank models using a novel multi-armed bandit approach that accounts for model runtimes, probability of passing user-defined assertions, and the computational structure of the ML workflow. 

-------------

## docs

**FlexiFlow** docs, add the link to the documentation present in the github repository.

-------------

## code

You can find the entire repository here: Link to the github repository here.
The Dockerfile used to build the FlexiFlow environment is present in root directory of the repository linked here.

-------------

## papers

Add the upcoming papers here.

-------------

## team

<div class="flex-container people image-container">
{% assign flexiflow_team = site.data.flexiflow_lab %}
{% for person in flexiflow_team %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

-------------


## collaborators

<div style="display: flex; flex-wrap: wrap; gap: 1.5em 2em;">
  <ul style="list-style: none; padding: 0; margin: 0; width: 100%;">
  {% assign collaborators = site.data.flexiflow_collaborators %}
  {% for person in collaborators %}
    <li style="margin-bottom: 1em; padding: 1em; border-radius: 8px; background: #f8f8f8; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
      <span style="font-weight: bold; font-size: 1.1em;">
        <a href="{{ person.website }}" target="_blank" style="color: #2a6496; text-decoration: none;">{{ person.name }}</a>
      </span><br>
      <span style="color: #555; font-size: 0.98em;">{{ person.affliation }}</span>
    </li>
  {% endfor %}
  </ul>
</div>
