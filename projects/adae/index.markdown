---
layout: page
title: ADAE
group: "navigation"
id: "projects"
---
<link rel="stylesheet" href="{{ site.baseurl}}/css/bootstrap.min.css">

<div class="jumbotron" style="background-image: none; background-color: #fff; background-size: cover; height: auto; padding: 5px 0 10px 0; margin-top: 2em">
  <img src="../../images/projects/policy.png" alt="Logo" style="width: 20rem" />
  <!--<text style="vertical-align: middle; font-size: 4em; font-weight: bold; letter-spacing: 0px; font-family: 'Verdana';">Text</text>-->
  <h4>Reproducible Policies and Community Impact</h4>
</div>


<blockquote>The project examines policies that encourage reproducible practices such as the Artifact Description and Artifact Evaluation, and the impact of such policies on community engagement. 
</blockquote>



<div id="people"></div>
# People

<div class="flex-container people image-container">
	<div class="flex-item person" title="Tanu Malik">
		<a href="https://facsrv.cs.depaul.edu/~tmalik1">
			<img src="{{ site.baseurl }}/images/people/Tanu.jpg"/>
			<p>Tanu Malik</p>
		</a>
	</div>


</div>

#  Publications


{% assign papers = site.data.publications |  sort: 'Date' | reverse %}
    {% for p in papers %}
        {% if p.id == 'Malik-IEEE21-J6' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 



&nbsp;
