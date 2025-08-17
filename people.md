--- 
description: Radiant's members 
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
