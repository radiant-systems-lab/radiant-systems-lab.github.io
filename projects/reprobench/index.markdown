---
layout: page
title: VisualWorld
group: "navigation"
id: "projects"
---
<link rel="stylesheet" href="{{ site.baseurl}}/css/bootstrap.min.css">

# Infrastructure for Enabling Reproducibility

<blockquote>
We see container technology as key to achieving the reproducibility goals. Containers are widely used tools to address dependency challenges and to make complicated software tools more portable. Currently available container technologies, such as Docker and Singularity, improve dependency and configuration management i.e., portability of the application. However, container solutions have a steep learning curve and often require dedicated personnel for management.
<br><br>
The goal of the Reproducibility Infrastructure project is to assess the requirements of existing infrastructure, examine how containers can be seamlessly adopted as part of existing infrastructure, and determine to what extent can emerging containers can containers solve solve some reproducibility infrastructure issues. 
</blockquote>

<style type="text/css">
	.media {
		border: 1px solid rgba(0,0,0,.125);
	}
	.media-left {
		background: rgb(211, 222, 234);
		vertical-align: middle;
		padding-left: 10px;
		padding-right: 10px;
		width: 175px;
		min-width: 175px;
		max-width: 175px;
		text-align: center;
	}

	.media-left img {
		max-width: 10em;
	}

	.media-body {
		padding: 20px;
	}

	.media-heading {
		font-size: 20px;
		font-weight: 750;
		line-height: 1.2;
	}
</style>

<a id="Sciunit-Hydroshare" />
<div class="media">
  <!--<div class="media-left">
    <a href="#">
      <img src="../../images/projects/Sciunit-Hydroshare.png" class="card-img" alt="Taxonomy Logo" />
    </a>
  </div>-->
  <div class="media-body">
    <!--<h4 class="media-heading">An Approach for Open and Reproducible Hydrological Modeling using Sciunit and HydroShare</h4>
	--><p>
    
	</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Choi-EGU21' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 


</div>
</div>

<a id="Taxonomy" />
<div class="media">
  <div class="media-body">
    <!--<h4 class="media-heading">A taxonomy for reproducible and replicable research in environmental modelling</h4>
	--><p>
	</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-EMS20-O5' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}.
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
 <a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="ci" />
<div class="media">

  <div class="media-body">
    <!--<h4 class="media-heading">Leveraging Scientific Cyberinfrastructures to Achieve Computational Hydrologic Model Reproducibility</h4>-->
		<p>
	</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-AGU18' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 


</div>
</div>

<a id="integrating" />
<div class="media">
  <div class="media-body">
    <!--<h4 class="media-heading">Integrating scientific cyberinfrastructures to improve reproducibility in computational hydrology: Example for HydroShare and GeoTrust</h4>-->
		<p>
		</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-EMS18-O4' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="achieving" />
<div class="media">
 
  <div class="media-body">
    <!--<h4 class="media-heading">Achieving Reproducible Computational Hydrologic Models by Integrating Scientific Cyberinfrastructures</h4>-->
	    <p>
		</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-IEMS18' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 


</div>
</div>

<a id="GeoTrust" />
<div class="media">
  <div class="media-body">
    <!--<h4 class="media-heading">GeoTrust Hub: A Platform For Sharing And Reproducing Geoscience Applications</h4>-->
	    <p>
		</p>

 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-AGU17' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="ci-collaborative" />
<div class="media">
   <div class="media-body">
    <!--<h4 class="media-heading">Cyberinfrastructure to Support Collaborative and Reproducible Computational Hydrologic Modeling</h4>-->
		<p>
		</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-AGU17' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="challenges" />
<div class="media">
   <div class="media-body">
    <!--<h4 class="media-heading">Challenges with Maintaining Legacy Software to Achieve Reproducible Computational Analyses: An Example for Hydrologic Modeling Data Processing Pipelines</h4>-->
		<p>
		</p>
 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Essawy-IEMS16' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
</p>
        {% endif %}
    {% endfor %} 



  </div>
</div>

<div id="people"></div>
# People

<div class="flex-container people image-container">
{% for p in site.data.allpeople %}
  {% if p.key == 'Raza' or p.key == 'Zhihao' or p.key == 'Tanu'%}
  {% include person_image image=p.image caption=p.name link=p.website title=p.name %}
  {% endif %}
{% endfor %}
</div>
## Acknowledgments

This work is supported by the NSF through grant
[ICER-1928369](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1928369),
[ICER-1639759](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1639759),
[ICER-1661918](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1661918), and
[ICER-1722152](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1722152).

&nbsp;
