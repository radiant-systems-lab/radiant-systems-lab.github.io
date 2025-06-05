---
layout: page
title: Publications 
group: "navigation"
id: "publications"
---
<head>
    <meta charset="utf-8">
    <link href="{{site.baseurl}}/css/publications.css" rel="stylesheet">
    <script type="text/javascript">
        /* When the user clicks on the button,
        toggle between hiding and showing the dropdown content */
        function dropDown(id) {
          document.getElementById(id).classList.toggle("show");
        }

        // Close the dropdown menu if the user clicks outside of it
        window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
              var openDropdown = dropdowns[i];
              if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
              }
            }
            
          }
        }
        function openTab(th)
        {
            window.open(th.name,'_blank');
        }
    </script>
</head>

# Publications #
<!--
{% capture dblp_url %}{{ site.data.faculty | map: 'dblp' | join: '|' }}{% endcapture %}

<p><a href="//dblp.uni-trier.de/search/publ?q={{ dblp_url }}" target="_blank">View in new window</a></p>
<iframe class="papers-iframe" src="//dblp.uni-trier.de/search/publ?q={{ dblp_url }}"></iframe>
-->

<p> 
You can also find my articles on my 
<a href= "https://scholar.google.com/citations?hl=en&user=ZvYwdsUAAAAJ"> Google Scholar profile</a>.  
</p> 

<!-- 
<p>
* Indicates equal contribution.
</p> 

<a href="/publicationbytopic/"><button type="button" class="btn" style="outline:none">By Topic </button></a> 
<a href="/publicationbyyear/"><button type="button" class="btn" style="outline:none">By Year  </button></a> 

<h3  class="pubyear">In the Pipeline</h3>
-->
<ol class="bibliography">
<!--
<li><b>Nakamura, Y.</b>, Raza, A, Malik, T, Sampath, D., &amp; Coombes, K. R. (2019). <i>Identification and comparison of genes differentially regulate by transcription factors and miRNAs</i>. 
<button onclick="openAbstract('abstract-example')" class="dropbtn">Abstract</button>
<button onclick="openBibtex()" class="dropbtn">BibTeX</button>

<div class="dropdown-content" id = "abstract-example">
    Transcription factors and microRNAs (miRNA) both play a critical role in gene regulation and in the development of many diseases such as cancer. Understanding how transcription factors and miRNAs influence gene expression is thus important to understand, but complicated due to the large and interconnected nature of the human genome. To help better understand what genes are being regulated by transcription factors and/or miRNAs we looked at it over 8000 patient samples from 32 different cancer types collected from The Cancer Genome Atlas (TCGA). We started by clustering the transcription factors and miRNAs using Thresher to reduce the number of features. Using both the mRNA and miRNA sequencing data we constructed linear models to calculate the coefficient of determination (R2) for each mRNA based on the Thresher cluster expression. We generated three types of linear models: transcription factor, miRNA and transcription factor plus miRNA. We then determined genes that were highly explained or poorly explained by each of the three models based on the genes R2 value. We performed downstream gene enrichment analysis using ToppGene on the sets of well and poorly explained genes. This identified differences in gene regulation between transcription factors and miRNAs and showed what groups of gene are differentially regulated.
</div>
<div class="dropdown-content" id="bibtex-dropdown">
   <pre>@article{aans19a,
      title = {Identification and comparison of genes differentially regulated
                    by transcription factors and {miRNAs}},
      author = {Asiaee*, Amir and Abrams*, Zachary B and Nakayiza, Samantha and Sampath, Deepa and Coombes, Kevin R},
      archiveprefix = {bioRxiv},
      eprint = {803643},
      note = {https://doi.org/10.1101/803643},
      year = {2019}
    }
   </pre>
</div>
</li>
-->

{% assign publications = site.data.publications |  sort: 'Date' | reverse %}
{% assign prev = blank %}
{% for publication in publications %}
{% if prev != publication.Year %}
<h3 class="pubyear">{{publication.Year}}</h3>
{% assign prev = publication.Year %}
{% endif %}
  <li>
  {{publication.Authors}}, "{{publication.title}}"<i>{% if publication.Book %}, {{publication.Book}}{% elsif publication.Journal %}, {{publication.Journal}}{% elsif publication.Conference %}, {{publication.Conference}}{% elsif publication.Publisher %}, {{publication.Publisher}}{% endif %}</i>{% if publication.Volume %}, vol. {{publication.Volume}}{% endif %}{% if publication.Pages %}, pp. {{publication.Pages}}{% endif %}{% if publication.Month %}, {{publication.Month}}{% endif %}{% if publication.Year %}, {{publication.Year}}{% endif %}
  <div class = "btns">
  <button onclick="dropDown('{{publication.id}}-abstract')" class="dropbtn btnAbstract">Abstract</button>
  <button onclick="dropDown('{{publication.id}}-bibtex')" class="dropbtn btnBibtex">Bibtex</button>
  {% assign pdfName = publication.id | split: "-" | last | append: ".pdf" | prepend: "/pdfs/pubs/"  %}
  {% for static_file in site.static_files %}
    {% if static_file.path == pdfName %}
  <button onClick="openTab(this)" href="#" name="{{ pdfName }}" class="dropbtn btnPdf">PDF</button>
    {% endif %}
  {% endfor %}
  </div>
  <div class="dropdown-content dropdown-abstract" id = "{{publication.id}}-abstract">
  {{publication.Description}}
  </div> 
  <div class="dropdown-content dropdown-bibtex" id = "{{publication.id}}-bibtex">
  <pre>
  {% if publication.Book %} @book{% raw %}{{% endraw %}{{publication.id}},
  {% elsif publication.Journal %} @article{% raw %}{{% endraw %}{{publication.id}}, 
  {% elsif publication.Conference %} @inproceedings{% raw %}{{% endraw %}{{publication.id}},
  {% else %} @misc{% raw %}{{% endraw %}{{publication.id}},
  {% endif %} {% if publication.title %}    title = {% raw %}{{% endraw %}{{publication.title}}{% raw %}}{% endraw %},
  {% endif %} {% if publication.Authors %}    author = {% raw %}{{% endraw %}{{publication.bibAuthors}}{% raw %}}{% endraw %},
  {% endif %} {% if publication.Journal %}    journal = {% raw %}{{% endraw %}{{publication.Journal}}{% raw %}}{% endraw %},
  {% endif %} {% if publication.Conference %}   booktitle = {% raw %}{{% endraw %}{{publication.Conference}}{% raw %}}{% endraw %},
  {% endif %} {% if publication.Publisher %}   publisher = {% raw %}{{% endraw %}{{publication.Publisher}}{% raw %}}{% endraw %},
  {% endif %} {% if publication.Year %}    year = {{publication.Year}},
  {% endif %} {% if publication.Pages %}    pages = {% raw %}{{% endraw %}{{publication.Pages}}{% raw %}}{% endraw %},
  {% endif %} {% raw %}}{% endraw %}
  </pre>
  </div>
  <div class="dropdown-content dropdown-pdf" id = "{{publication.id}}-pdf">
  </div>
  </li>
{% endfor %}

</ol>

