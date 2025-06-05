---
layout: page
title: VisualWorld
group: "navigation"
id: "projects"
---

<link rel="stylesheet" href="{{ site.baseurl}}/css/bootstrap.min.css">
# Provenance for Reproducibility

<blockquote>
Data provenance, is about methodically recording a computation. Our research work is examining different approaches to see how data provenance can optimise re-computation in the presence of changes. This can improve use of provenance in a variety of purposes, including facilitating experiment reproducibility, distributed debugging, and efficiently replay when sharing data and code.

Specific research questions include (1) how, and under what assumptions, can re-computation be optimized using incremental and/or partial processing techniques, and (2) how do we determine the impact of a set of changes on the outcomes, in order to decide when changes should trigger recomputations.
We optimize recomputation while computing <a href="">differences</a>, alignment, and during replay.

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
		width: 315px;
		min-width: 315px;
		max-width: 315px;
		text-align: center;
	}

	.media-left img {
		max-width: 20em;
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

<a id="chex" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/CHEX.png" class="card-img" alt="CHEX Logo" style="width: 26em"/>
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">CHEX: Multiversion Replay with Ordered Checkpoints</h4>
	<p>
	In scientific computing and data science disciplines, it is often necessary to share application workflows and repeat results. Current tools containerize application workflows, and share the resulting container for repeating results. These tools, due to containerization, do improve sharing of results. However, they do not improve the efficiency of replay. The multiversion replay problem arises when multiple versions of an application are containerized, and each version must be replayed to repeat results. To avoid executing each version separately, CHEX, checkpoints program state and determines when it is permissible to reuse program state across versions. It does so using system call-based execution lineage. It optimizes replay using an in-memory cache, based on a checkpoint-restore-switch system. </p>
	
  {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-arxiv22-C30' %}
    <p>
    <strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
  {% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
    <a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
    </p>
        {% endif %}
    {% endfor %} 

  </div>
</div>

<a id="provscope" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/ProvScope.png" class="card-img" alt="provscope Logo" style="width: 26em" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Provenance Difference and Alignment</h4>
	<p>
	Reproducing experiments entails repeating experiments with changes. Changes, such as a change in input arguments, a change in the invoking environment, or a change due to nondeterminism in the runtime may alter results. If results alter significantly, perusing them is not sufficient—users must analyze the impact of a change and determine if the experiment computed the same steps. Making fine-grained, stepwise comparisons can be both challenging and time-consuming. This project compares a reproduced execution with recorded system provenance of the original execution, and determine provenance alignment. The alignment is based on comparing the specific location in the program, the control flow of the execution, and data inputs.
	
	</p>
    {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-TaPP20-C27' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
  {% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 
  </div>
</div>

<a id="ProvUse" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/ProvUse.png" class="card-img" alt="ProvUse Logo" style="width: 26em"/>
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Utilizing Provenance in Reusable Research Objects</h4>
		<p>
        Science is conducted collaboratively, often requiring the sharing of knowledge about computational experiments. When experiments include only datasets, they can be shared using Uniform Resource Identifiers (URIs) or Digital Object Identifiers (DOIs). An experiment, however, seldom includes only datasets, but more often includes software, its past execution, provenance, and associated documentation. The Research Object has recently emerged as a comprehensive and systematic method for aggregation and identification of diverse elements of computational experiments. While a necessary method, mere aggregation is not sufficient for the sharing of computational experiments. Other users must be able to easily recompute on these shared research objects. Computational provenance is often the id to enable such reuse. We show how reusable research objects can utilize provenance to correctly repeat a previous reference execution, to construct a subset of a research object for partial reuse, and to reuse existing contents of a research object for modified reuse. 	</p>
{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-Informatics18-J4' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
  {% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 
  </div>
</div>

<a id="DistPTU" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/ProvDist.png" class="card-img" alt="Dist PTU Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading"> Improving Reproducibility of Distributed Computational Experiments</h4>
	    <p>
   Conference and journal publications increasingly require experiments associated with a submitted article to be repeatable. Authors comply to this requirement by sharing all associated digital artifacts, ie, code, data, and environment configuration scripts. To ease aggregation of the digital artifacts, several tools have recently emerged that automate the aggregation of digital artifacts by auditing an experiment execution and building a portable container of code, data, and environment. However, current tools only package non-distributed computational experiments. Distributed computational experiments must either be packaged manually or supplemented with sufficient documentation. 
		</p>

 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-PRECS18-W13' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"  %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 

  </div>
</div>

<a id="ptu-citation" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/ProvCitation.png" class="card-img" alt="PTU Citation" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Using Provenance for Generating Automatic Citations</h4>
		<p>
		When computational experiments include only datasets, they could be shared through the Uniform Resource Identifiers (URIs) or Digital Object Identifiers (DOIs) which point to these resources. However, experiments seldom include only datasets, but most often also include software, execution results, provenance, and other associated documentation. The Research Object has recently emerged as a comprehensive and systematic method for aggregation and identification of diverse elements of computational experiments. While an entire Research Object may be citable using a URI or a DOI, it is often desirable to cite specific sub-components of a research object to help identify, authorize, date, and retrieve the published sub-components of these objects. We show an approach to automatically generate citations for sub-components of research objects by using the object's recorded provenance. 
		</p>

 {% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-TaPP18-W14' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"  %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>
<!--
<a id="provinsoftpkg" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/provinsoftpkg.png" class="card-img" alt="PISP Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Auditing and Maintaining Provenance in Software Packages</h4>
		<p>
        Science projects are increasingly investing in computational reproducibility. Constructing software pipelines to demonstrate reproducibility is also becoming increasingly common. To aid the process of constructing pipelines, science project members often adopt reproducible methods and tools. One such tool is CDE, which is a software packaging tool that encapsulates source code, datasets and environments. However, CDE does not include information about origins of dependencies. Consequently when multiple CDE packages are combined and merged to create a software pipeline, several issues arise requiring an author to manually verify compatibility of distributions, environment variables, software dependencies and compiler options. This project describes how provenance is to be included as part of CDE so that resulting provenance-included CDE packages can be easily used for creating and sharing provenance-enabled software packages.  
		</p>

	{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-IPAW14-C17' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"  %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 
  </div>
</div>
-->

<a id="ptu" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/PTU.png" class="card-img" alt="PTU Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">PTU: Provenance-to-Use</h4>
	    <p>
Provenance-To-Use (PTU) is a tool that minimizes computation time during repeatability testing. Authors can use PTU to build a package that includes their software program and a provenance trace of an initial reference execution. Testers can select a subset of the package’s processes for a partial deterministic replay—based, for example, on their compute, memory and I/O utilization as measured during the reference execution. Using the provenance trace, PTU guarantees that events are processed in the same order using the same data from one execution to the next. PTU is now part of <a href="http://sciunit.run">Sciunit</a> and helps to conduct repeatability testing of workflow-based scientific programs.
         
		</p>

	{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-TaPP13-W8' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"  %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 
   <!--	{% assign repo = site.data.githubrepo %}
    {% for p in repo %}
        {% if p.id == 'PTU' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. <a class="btn btn-primary btn-xs" href="/projects/Malik-IPAW-14.pdf" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} -->
  </div>
</div>



<div id="people"></div>
# People

<div class="flex-container people image-container">
{% for p in site.data.allpeople %}
  {% if p.key == 'Yuta' or p.key == 'Nithin' or p.key == 'Shilvi' or p.key == 'Hai' or p.key == 'Tanu' %}
  {% include person_image image=p.image caption=p.name link=p.website title=p.name %}
  {% endif %}
{% endfor %}
</div>

## Acknowledgments

This work is supported by the NSF through grants
[CNS-1846418](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1846418),
[ICER-1639759](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1639759),
[ICER-1722152](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1722152), 
[DePaul ORS](https://offices.depaul.edu/research-services/Pages/default.aspx), and
[Smart Data Platform:subaward from University of Chicago, Bloomberg Foundation](https://chicago.github.io/smart-data-platform/)


&nbsp;
