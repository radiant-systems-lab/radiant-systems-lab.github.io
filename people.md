---
layout: page
description: Radiant's members
---

<style>
.navbar {
  background: #f8f8f8;
  border-bottom: 1px solid #ddd;
  position: sticky;
  top: 0;
  z-index: 1000;
}
    
.navbar-inner {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0.5rem;
}

.nav li {
  display: inline-block;
  margin: 0 10px;
}
    
.nav a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 6px 10px;
  border-radius: 5px;
  transition: background 0.2s;
}
    
.nav a:hover {
  background: #eaeaea;
}

h2 {
  border-bottom: 2px solid #eee;
  padding-bottom: 4px;
  margin-top: 2rem;
  text-transform: capitalize;
}

.flex-container.people.image-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
}

.person-card {
  text-align: center;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 10px;
  width: 160px;
  transition: transform 0.2s, box-shadow 0.2s;
}
    
.person-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
    
.person-card img {
  border-radius: 50%;
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-bottom: 8px;
}
    
.person-card h3 {
  font-size: 1rem;
  margin: 0;
}
    
.person-card p {
  font-size: 0.85rem;
  color: #666;
}

ul.alumni-list {
  list-style: none;
  padding: 0;
}
    
ul.alumni-list li {
  margin: 5px 0;
  padding: 6px;
  border-bottom: 1px solid #eee;
}
    
ul.alumni-list li a {
  font-weight: 500;
  color: #0066cc;
  text-decoration: none;
}
    
ul.alumni-list li a:hover {
  text-decoration: underline;
}
    
</style>

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
  <div class="person-card">
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
    <h3>{{ person.name }}</h3>
    <p>Director</p>
  </div>
{% endfor %}
</div>

## <a name="postdocs"></a>postdocs

See <a href="#openings">open positions.</a>
 
## <a name="phd"></a>graduate students

<div class="flex-container people image-container">
{% for person in site.data.phd_students %}
  <div class="person-card">
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
    <h3>{{ person.name }}</h3>
    <p>PhD Student</p>
  </div>
{% endfor %}
</div>

## <a name="ms"></a>masters students

<div class="flex-container people image-container">
{% for person in site.data.master_students %}
  <div class="person-card">
    {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
    <h3>{{ person.name }}</h3>
    <p>Masters Student</p>
  </div>
{% endfor %}
</div>

## <a name="ug"></a>undergraduate students

See <a href="#openings">open positions.</a>

## <a name="alumni"></a>alumni

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

## <a name="openings"></a>openings
