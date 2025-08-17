---
title: Radiant Members
layout: page
description: Radiant's members
---

<style>
/* Flex container for people */
.flex-container.people {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}

/* Individual image container */
.image-container > div {
  position: relative;
  text-align: center;
  width: 150px; /* Adjust as needed */
}

/* Person image styling */
.image-container img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
}

/* Hover effect */
.image-container img:hover {
  transform: scale(1.05);
}

/* Caption below image */
.image-container .caption {
  margin-top: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .image-container > div {
    width: 45%;
  }
}

@media (max-width: 480px) {
  .image-container > div {
    width: 100%;
  }
}
</style>

## <a name="director"></a>Director
<div class="flex-container people image-container">
  {% for person in site.data.faculty %}
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
  {% endfor %}
</div>

## <a name="postdocs"></a>Postdocs
See <a href="#openings">open positions.</a>

## <a name="phd"></a>Graduate Students
<div class="flex-container people image-container">
  {% for person in site.data.phd_students %}
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
  {% endfor %}
</div>

## <a name="ms"></a>Master's Students
<div class="flex-container people image-container">
  {% for person in site.data.master_students %}
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
  {% endfor %}
</div>

## <a name="ug"></a>Undergraduate Students
See <a href="#openings">open positions.</a>

## <a name="alumni"></a>Alumni
{% if site.data.alumni %}
  <ul>
    {% assign sorted_alumni = site.data.alumni | sort: "name" %}
    {% for person in sorted_alumni %}
      <li>
        {% if person.website %}
          <a href="{{ person.website }}">{{ person.name }}</a>
        {% else %}
          {{ person.name }}
        {% endif %}
        {% if person.at %} (now at {{ person.at }}) {% endif %}
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>No alumni data available.</p>
{% endif %}

## <a name="openings"></a>Current Openings
