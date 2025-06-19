---
layout: page
title: people
description: Radiant's members
---

<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="#director">director</a></li>
            <li><a href="#postdocs">postdocs</a></li>
            <li><a href="#phd">phd</a></li>
            <li><a href="#masters">ms</a></li>
            <li><a href="#ug">ug</a></li>
            <li><a href="#alumni">alumni</a></li>
            <li><a href="#openings">openings</a></li>
        </ul>
    </div>
</div>

---

## <a name="director"></a>director

<div class="flex-container people image-container">
{% for person in site.data.faculty %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

## <a name="postdocs"></a>postdocs


## <a name="phd"></a>graduate students

<div class="flex-container people image-container">
{% for person in site.data.phd_students %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

## <a name="ms"></a>masters students

<div class="flex-container people image-container">
{% for person in site.data.master_students %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

## <a name="ug"></a>undergraduate students


## <a name="alumni"></a>alumni

<ul>
{% assign sorted_alumni = (site.data.alumni) %}
{% for person in sorted_alumni %}
  <li>
    {% if person.website %}
    <a href="{{ person.website }}">
      {{person.name}}
    </a>
    {% else %}
      {{person.name}}
    {% endif %}
    {% if person.at %} (now at {{ person.at }}) {% endif %}
  </li>
{% endfor %}
</ul>

## <a name="openings"></a>openings
