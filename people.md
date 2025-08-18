---
title: Radiant Members
layout: page
description: Radiant's members
---

---

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
        {% if person.at %} <span class="at">(now at {{ person.at }})</span> {% endif %}
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>No alumni data available.</p>
{% endif %}

## <a name="openings"></a>Current Openings
<div class="openings">
  <div class="opening-card">
    <h3>Post-doctoral Position</h3>
    <p>
      The <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> 
      in the <a href="https://engineering.missouri.edu/">College of Engineering</a> at 
      <a href="https://missouri.edu/">University of Missouri, Columbia</a> 
      is seeking talented and motivated postdoctoral fellows to work on exciting scientific research projects.
    </p>

    <p>
      <strong>Areas:</strong> Graph data management, data provenance/lineage, workflow systems, notebooks, and scientific data management.  
      Focus on capturing, tracking, and making understandable large-scale distributed scientific experiments using HPC and finite-element models.
    </p>

    <p>
      <strong>Eligibility:</strong> Ph.D. within the last three years in systems, workflows, data management, HPC, or related fields.  
      <strong>Start Date:</strong> Anytime after Jan 1, 2025.  
      <strong>Duration:</strong> Up to 4 years.  
      <strong>Benefits:</strong> Competitive salary and excellent benefits.
    </p>

    <p>
      <strong>Supervisors:</strong> Tanu Malik and advisory team.  
      <strong>Location:</strong> Multi-university, multi-disciplinary center with opportunities for travel, training, and dissemination.
    </p>

    <p><strong>How to Apply:</strong> Send your CV and Research Statement to <a href="mailto:tanu@missouri.edu">tanu at missouri dot edu</a>.</p>
  </div>
</div>
