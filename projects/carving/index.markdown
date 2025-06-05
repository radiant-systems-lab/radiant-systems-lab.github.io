---
layout: page
title: ADAE
group: "navigation"
id: "projects"
---
<link rel="stylesheet" href="{{ site.baseurl}}/css/bootstrap.min.css">

<div class="jumbotron" style="background-image: none; background-color: #fff; background-size: cover; height: auto; padding: 5px 0 10px 0; margin-top: 2em">
  <img src="../../images/projects/carving.png" alt="Logo" style="width: 20em" />
  <!--<text style="vertical-align: middle; font-size: 4em; font-weight: bold; letter-spacing: 0px; font-family: 'Verdana';">Text</text>-->
  <h4>Provenance Issues in Forensic Analysis</h4>
</div>


<blockquote>
Database Management Systems generate a multitude of data copies as part of their normal operation. For example, a materialized view stores the pre-computed results of a query drawn from the data tables in order to improve query performance. An index contains a copy of values from the indexed column(s) combined with a pointer back to the source table in order to speed up record access. Many other copies of data are created by DBMS engine actions such as caching, log entries, or internal storage defragmentation. These and other internal copies of data can be extracted from DBMS storage with the help of database carving and used for evidence of database tampering or storage corruption.
</blockquote>

<div id="people"></div>
# People

<div class="flex-container people image-container">

	<div class="flex-item person" title="Alex Rasin">
		<a href="https://facsrv.cs.depaul.edu/~alex">
			<img src="{{ site.baseurl }}/images/people/Alex.jpg"/>
			<p>Alex Rasin</p>
		</a>
	</div>
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
        {% if p.id == 'Wagner-EDBT18-C24' or p.id =='Rasin-TaPP18-P4' or p.id == 'Wagner-CIDR17-C22' or p.id == 'Wagner-VLDB20-W17' or p.id == 'Wagner-EDBT20-W15' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 




&nbsp;
