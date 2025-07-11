---
layout: page
title: software
description: Radiant's Research Projects 
---

<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="https://github.com/radiant-systems-lab/">Lab github</a></li>
            <li><a href="#sciunit">sciunit</a></li>
            <li><a href="#provscope">provscope</a></li>
            <li><a href="#floability">floability</a></li>
            <li><a href="#flexiflow">flexiflow</a></li>
        </ul>
    </div>
</div>



## sciunit


**Sciunit** is a suite of tools for creating lightweight containers from reference executions of an application. It supports command-line, notebook, and data-intensive applications. Each tool enables efficient containerization of multiple executions through content-based deduplication. The resulting containers can be re-executed in compatible x86-based Linux kernel environments, with support for modifying input parameters or datasets to reproduce results. Sciunit simplifies the sharing of self-contained applications among collaborators and leverages audited provenance to ensure repeatability and reproducibility. For installation and usage instructions, see the Sciunit [documentation](<https://github.com/depaul-dice/sciunit/wiki>).

<!--For latest research papers and publications on this project, visit `here <https://dice.cs.depaul.edu/publications>`_.-->

Github: <a href="https://sciunit.github.io/">sciunit</a> <br>
Funding: ICER, ICER, ICER, CISE-CSR, NASA 

------------
## provscope

**ProvScope** is an accurate and efficient tool for comparing extremely large execution provenance traces generated during reference runs of long-running applications. It uses an LLVM-based specification of the application to identify precise differences between traces, reporting the exact lines and functions where the executions diverge. For MPI-based applications, ProvScope-MPI enables detection of differences across runs that exhibit both communication and input non-determinism. ProvScope reports all divergences and convergences. 

Github: <a href="https://sciunit.github.io/">provscope</a> <br> 
Funding: CISE-CSR


## <a href="/softwares/floability/">floability</a>

**Floability** is a system that will enable the rapid and portable deployment of notebooks expressing complex scientific workflows across a wide range of cyberinfrastructure. The key technical challenge is that workflows are incomplete: the code by itself cannot be moved between facilities without accurately capturing the software dependencies, required datasets, and capabilities of the underlying cluster hardware. In addition it aims to solve the problem of translating notebooks to workflows and vice versa. Floability is collaboratively developed by the University of Notre Dame, the University of Missouri-Columbia, and the University of Illinois.

Funding: <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2516579">NSF</a>  

-------------
## <a href="/softwares/flexiflow/">flexiflow</a>

**FlexiFlow** is a system that aims to improve performance and accuracy of end-to-end ML workflows during inference time. 
It will soon be made open-source. 

Funding: MU Seed Funding
