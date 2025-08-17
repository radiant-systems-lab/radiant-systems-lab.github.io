---
title: 'Radiant Members'
layout: page
description: Radiant's members
---

<style>
/* Fonts */
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500,700|Roboto+Slab:400,700&display=swap');

/* Container */
.container-narrow {
  margin: 0 auto;
  max-width: 1100px;
  padding: 0 20px;
}

/* Section Titles */
h2 {
  font-family: 'Roboto Slab', serif;
  font-size: 2rem;
  margin: 60px 0 20px; /* add spacing above/below */
  position: relative;
  display: inline-block;
}
h2::after {
  content: "";
  display: block;
  width: 80px;
  height: 4px;
  background-color: #fbbf24;
  margin-top: 4px;
}

/* Flex layout for people */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
  margin-bottom: 40px;
}

/* Individual person card */
.person {
  background-color: #fff;
  width: 140px;
  text-align: center;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.person:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}
.person img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-bottom: 2px solid #fbbf24;
}
.person p {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  font-size: 1rem;
  margin: 10px 0;
  color: #333;
  background-color: transparent; /* no overlay text */
}

/* Alumni list */
ul.alumni-list {
  list-style: none;
  padding-left: 0;
  margin-bottom: 40px;
}
ul.alumni-list li {
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  margin-bottom: 8px;
}
ul.alumni-list li a {
  color: #007BFF;
  text-decoration: none;
}
ul.alumni-list li a:hover {
  text-decoration: underline;
}

/* Links */
a {
  color: #007BFF;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}

/* Current openings box */
#openings {
  background-color: #f9f9f9;
  border-left: 4px solid #800080;
  border-radius: 6px;
  padding: 15px 20px;
  margin-bottom: 60px;
  font-family: 'Roboto', sans-serif;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .flex-container {
    justify-content: center;
  }
  h2 {
    font-size: 1.6rem;
  }
  .person {
    width: 120px;
  }
  .person img {
    height: 140px;
  }
}
</style>

<div class="container-narrow">

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
    <ul class="alumni-list">
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
  <div id="openings">
    <!-- Openings content here -->
  </div>

</div>
