---
layout: page
title: floability
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

**Floability** is a system that will enable the rapid and portable deployment of notebooks expressing complex scientific workflows across a wide range of cyberinfrastructure. The key technical challenge is that workflows are incomplete: the code by itself cannot be moved between facilities without accurately capturing the software dependencies, required datasets, and capabilities of the underlying cluster hardware. In addition it aims to solve the problem of translating notebooks to workflows and vice versa. Floability is collaboratively developed by the University of Notre Dame, the University of Missouri-Columbia, and the University of Illinois.

<div style="display: flex; align-items: flex-start; gap: 2em; margin: 0.2em 0; flex-wrap: wrap; font-size: 20px;">
  <div style="flex: 2 1 600px; min-width: 500px;">

  </div>
  <div style="flex: 1 1 500px; min-width: 450px; text-align: center;">
    <img src="/images/softwares/floability-Arch.png" alt="floability Architecture Diagram" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <div style="color:#444; margin-top:0.5em; font-style:italic;">floability Architecture</div>
  </div>
</div>

-------------

## docs


- [Quick start instructions](https://github.com/floability/floability-cli/blob/main/README.md)
- [Backpack specification](https://github.com/floability/floability-cli/blob/main/docs/backpack.md)
- [Backpack examples](https://github.com/floability/floability-examples)


-------------

## code

You can find the entire repository here: <a href= "https://github.com/floability/floability-cli">https://github.com/floability/floability-cli</a>

-------------

## papers

- Islam, M. S., Azaz, T., Ahmad, R., Hossain, A. S. M. S., Baig, F., Wang, S., Lannon, K., Malik, T., and Thain, D., "Backpacks for Notebooks: Enabling Containerized Notebook Workflows in Distributed Environments", _21st IEEE International Conference on eScience_, to appear, 2025

-------------

## team

<div class="flex-container people image-container">
{% assign floability_team = site.data.floability_lab %}
{% for person in floability_team %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

-------------


## collaborators

<div style="display: flex; flex-wrap: wrap; gap: 1.5em 2em;">
  <ul style="list-style: none; padding: 0; margin: 0; width: 100%;">
  {% assign collaborators = site.data.floability_collaborators %}
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
