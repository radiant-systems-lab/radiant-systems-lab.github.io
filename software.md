---
layout: page
title: software
description: Radiant's Research Projects 
---

<style>
  /* Clean up theme defaults */
  .page-header { display: none !important; }
  .content { padding-top: 0 !important; }
  h2 { border-bottom: none !important; }
</style>

<div style="display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 10px; border-bottom: 1px solid #eee; margin-bottom: 15px;">
  <h2 style="margin: 0; border: none; padding: 0; color: #403F85; line-height: 1; font-weight: bold; text-transform: capitalize;">software</h2>
  <div class="quick-jump-links" style="font-size: 0.9rem;">
    <a href="https://github.com/radiant-systems-lab/" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;" target="_blank">Lab github</a>
    <a href="#sciunit" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">sciunit</a>
    <a href="#provscope" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">provscope</a>
    <a href="#floability" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">floability</a>
    <a href="#flexiflow" style="font-weight: bold; text-decoration: none; color: #0088cc;">flexiflow</a>
  </div>
</div>

<h2 id="sciunit"><a href="https://radiant-systems-lab.github.io/SciunitSite/" target="_blank">sciunit</a></h2> 

**Sciunit** is a suite of tools for creating lightweight containers from reference executions of an application. It supports command-line, notebook, and data-intensive applications. Each tool enables efficient containerization of multiple executions through content-based deduplication. The resulting containers can be re-executed in compatible x86-based Linux kernel environments, with support for modifying input parameters or datasets to reproduce results. Sciunit simplifies the sharing of self-contained applications among collaborators and leverages audited provenance to ensure repeatability and reproducibility. For installation and usage instructions, see the Sciunit [documentation](<https://github.com/depaul-dice/sciunit/wiki>).

Github: <a href="https://github.com/radiant-systems-lab/sciunit" target="_blank">sciunit</a> <br>
Funding: ICER, ICER, ICER, CISE-CSR, NASA 

------------

<h2 id="provscope">provscope</h2>

**ProvScope** is an accurate and efficient tool for comparing extremely large execution provenance traces generated during reference runs of long-running applications. It uses an LLVM-based specification of the application to identify precise differences between traces, reporting the exact lines and functions where the executions diverge. For MPI-based applications, ProvScope-MPI enables detection of differences across runs that exhibit both communication and input non-determinism. ProvScope reports all divergences and convergences. 

Github: <a href="https://github.com/radiant-systems-lab/ProvScope" target="_blank">provscope</a> <br> 
Funding: CISE-CSR

------------

<h2 id="floability"><a href="/softwares/floability/">floability</a></h2>

**Floability** is a system that will enable the rapid and portable deployment of notebooks expressing complex scientific workflows across a wide range of cyberinfrastructure. The key technical challenge is that workflows are incomplete: the code by itself cannot be moved between facilities without accurately capturing the software dependencies, required datasets, and capabilities of the underlying cluster hardware. In addition it aims to solve the problem of translating notebooks to workflows and vice versa. Floability is collaboratively developed by the University of Notre Dame, the University of Missouri-Columbia, and the University of Illinois.

Funding: <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2516579">NSF</a>  

-------------

<h2 id="flexiflow"><a href="/softwares/flexiflow/">flexiflow</a></h2>

**FlexiFlow** is a system that aims to improve performance and accuracy of end-to-end ML workflows during inference time. 
It will soon be made open-source. 

Funding: MU Seed Funding