---
layout: page
title: VisualWorld
group: "navigation"
id: "projects"
---
<link rel="stylesheet" href="{{ site.baseurl}}/css/bootstrap.min.css">

# Advanced Containers for Reproducible Science

<blockquote>
A decade ago, sharing a computation implied providing code and data related to the application. There is increasing consensus that to establish the reproducibility of results, authors must also share a description of their computing environments, such as documentation of system libraries, configuration files, and parameters used. Containerization has emerged as a predominant technology for preserving and sharing computational environments. But is containerization sufficient? 
<br><br>
The DICE lab is building advanced containers that combine isolation property offered by containers with data provenance and analysis methods. We are building a variety of containers for data-intensive applications, interactive applications, and analytical applications. 
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

<a id="sciunit" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/Sciunit.png" class="card-img" alt="Sciunit Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading"> Sciunit: a system for easily containerizing, sharing, and tracking scientific applications</h4>
	<p>
   Sciunits are efficient, lightweight, self-contained packages of computational experiments that can be guaranteed to repeat or reproduce regardless of deployment issues. Sciunit answers the call for a reusable research object that containerizes and stores applications simply and efficiently, facilitates sharing and collaboration, and eases the task of executing, understanding, and building on shared work.

To create Sciunits, <a href="https://sciunit.run/install">install</a> our Linux command-line tool.
	</p>

{% assign papers = site.data.publications |  sort: 'Date' | reverse %}
    {% for p in papers %}
        {% if p.id == 'Malik-JCCS15-J2' or p.id == 'Malik-eScience17-C23' or p.id == 'Malik-SOLE14-B3' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 



  </div>
</div>

<a id="sciunit-nb" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/CDMT.png" class="card-img" alt="Sciunit-NB Logo" style="width: 20em" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Content-defined Merkle Trees for Efficient Container Delivery</h4>
	<p>
Containerization simplifies the sharing and deployment of applications when environments change in the software delivery chain. To deploy an application, container delivery methods push and pull container images. These methods operate on file and layer (set of files) granularity, and introduce redundant data within a container. Several container operations such as upgrading, installing, and maintaining become inefficient, because of copying and provisioning of redundant data. CDMT is a content-defined Merkle Tree for deduplicated storage used in containers. CDMT indexes deduplicated and determines changes to blocks in logarithmic time on the client. CDMT efficiently pushes and pulls container images from a registry, especially as containers are upgraded and (re-)provisioned on a client. A registry can efficiently maintain the CDMT index as new image versions are pushed. CDMT are more scalable than Merkle Trees in terms of disk and network I/O savings ias shown using 15 container images and 233 image versions from Docker Hub. 	
</p>
{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-HiPC20-C28' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="midas" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/Midas.png" class="card-img" alt="Midas Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">MiDas: Containerizing Data-Intensive Applications with I/O Specialization </h4>
		<p>
		Scientific applications often depend on data produced from computational models. Model-generated data can be prohibitively large. Current mechanisms for sharing and distributing reproducible applications, such as containers, assume all model data is saved and included with a program to support its successful re-execution. However, including model data increases the sizes of containers. This increases the cost and time required for deployment and further reuse. MiDAS ( Minimizing Datasets) is a framework for specializing I/O libraries which, given an application, automates the process of identifying and including only a subset of the data accessed by the program. To do this, MiDas combines static and dynamic analysis techniques to map high level user inputs to low level file offsets. 
        </p>
{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Niddodi-PRECS20-W16' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{% if p.Book %}, {{p.Book}}{% elsif p.Journal %}, {{p.Journal}}{%  elsif p.Conference %}, {{p.Conference}}{% elsif p.Publisher %}, {{p.Publisher}}{% endif %}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 


  </div>
</div>

<a id="SciInc" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/SciInc.png" class="card-img" alt="SciInc Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">SciInc: A Container Runtime for Incremental Recomputation</h4>
		<p>
   The conduct of reproducible science improves when computations are portable and verifiable. A container runtime provides an isolated environment for running computations and thus is useful for porting applications on new machines. Current container engines, such as LXC and Docker, however, do not track provenance, which is essential for verifying computations. SciInc is a container runtime that tracks the provenance of computations during container creation. SciInc container engines can use audited provenance data for efficient container replay. SciInc observes inputs to computations, and, if they change, propagates the changes, re-using partially memoized computations and data that are identical across replay and original run. 
		</p>

{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-eScience19-C25' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 

  </div>
</div>


<a id="ldv" />
<div class="media">
  <div class="media-left">
    <a href="#">
      <img src="../../images/projects/LDV.png" class="card-img" alt="LDV Logo" />
    </a>
  </div>
  <div class="media-body">
    <h4 class="media-heading">Lightweight Database Virtualization (LDV)</h4>
		<p>
            Light-weight database virtualization (LDV) is a system that allows users to share and re-execute applications that operate on a relational database (DB). Previous methods for sharing DB applications, such as companion websites and virtual machine images (VMIs), support neither easy and efficient re-execution nor the sharing of only a relevant DB subset. LDV addresses these issues by monitoring application execution, including DB operations, and using the resulting execution trace to create a lightweight re-executable package. A LDV package includes, in addition to the application, either the DB management system (DBMS) and relevant data or, if the DBMS and/or data cannot be shared, just the application-DBMS communications for replay during re-execution. LDV uses a linked DB-operating system provenance model and show how to infer data dependencies based on temporal information.
    
		</p>
{% assign papers = site.data.publications %}
    {% for p in papers %}
        {% if p.id == 'Malik-ICDE15-C19' %}
<p>
<strong>{{p.title}}. </strong> {{p.Authors}} <strong><i>{{p.Conference}}</i></strong>, {{p.Year}}. 
{% assign pdfName = p.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"   %}
<a class="btn btn-primary btn-xs" href="{{pdfName}}" role="button">Paper</a>
</p>
        {% endif %}
    {% endfor %} 
 Thanks to <a href="http://www.cs.iit.edu/~dbgroup/research.html"/>Boris Glavic</a> for the LDV logo. 
  </div>
</div>

<div id="people"></div>
# People


<div class="flex-container people image-container">
{% for p in site.data.allpeople %}
  {% if p.key == 'Raza' or p.key == 'Yuta' or p.key == 'Hai' or p.key == 'Zhihao' or p.key == 'Tanu' or p.key == 'Ashish' %}
  {% include person_image image=p.image caption=p.name link=p.website title=p.name %}
  {% endif %}
{% endfor %}
</div>
## Acknowledgments

This work is supported by the NSF through grants
[CNS-1846418](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1846418),
[ICER-1928369](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1928369),
[ICER-1639759](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1639759), and
[BSSw Fellowship](https://bssw.io/);


&nbsp;
