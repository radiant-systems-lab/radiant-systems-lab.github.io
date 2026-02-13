---
layout: page
title: Software
description: Radiant's Research Projects
---

<div class="page-software">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-code-branch"></i> Software</h2>
      <p class="page-subtitle">
        Open-source systems and research software developed by the Radiant Systems Lab.
      </p>
    </div>
    <div class="quick-jump-links">
      <a href="https://github.com/radiant-systems-lab/" target="_blank">Lab GitHub</a>
      <a href="#sciunit">Sciunit</a>
      <a href="#provscope">ProvScope</a>
      <a href="#floability">Floability</a>
      <a href="#flexiflow">FlexiFlow</a>
    </div>
  </div>

  <section class="software-list">
    <article class="software-card" id="sciunit">
      <div class="software-card-top">
        <h3><i class="fa-solid fa-box-open"></i> <a href="https://radiant-systems-lab.github.io/SciunitSite/" target="_blank">Sciunit</a></h3>
        <span class="software-badge">Reproducibility Toolkit</span>
      </div>

      <p>
        <strong>Sciunit</strong> is a suite of tools for creating lightweight containers from reference executions of an application.
        It supports command-line, notebook, and data-intensive applications. Each tool enables efficient containerization of multiple
        executions through content-based deduplication. The resulting containers can be re-executed in compatible x86-based Linux kernel
        environments, with support for modifying input parameters or datasets to reproduce results. Sciunit simplifies sharing
        self-contained applications among collaborators and leverages audited provenance to ensure repeatability and reproducibility.
      </p>

      <div class="software-links">
        <a class="software-link" href="https://radiant-systems-lab.github.io/SciunitSite/" target="_blank">
          <i class="fa-solid fa-globe"></i> Website
        </a>
        <a class="software-link" href="https://github.com/radiant-systems-lab/sciunit" target="_blank">
          <i class="fa-brands fa-github"></i> GitHub
        </a>
        <a class="software-link" href="https://github.com/depaul-dice/sciunit/wiki" target="_blank">
          <i class="fa-solid fa-book"></i> Documentation
        </a>
      </div>

      <p class="software-funding"><strong>Funding:</strong> ICER, ICER, ICER, CISE-CSR, NASA</p>
    </article>

    <article class="software-card" id="provscope">
      <div class="software-card-top">
        <h3><i class="fa-solid fa-magnifying-glass-chart"></i> ProvScope</h3>
        <span class="software-badge">Trace Comparison</span>
      </div>

      <p>
        <strong>ProvScope</strong> is an accurate and efficient tool for comparing extremely large execution provenance traces generated
        during reference runs of long-running applications. It uses an LLVM-based specification of the application to identify precise
        differences between traces, reporting the exact lines and functions where executions diverge. For MPI-based applications,
        ProvScope-MPI enables detection of differences across runs that exhibit both communication and input non-determinism.
        ProvScope reports all divergences and convergences.
      </p>

      <div class="software-links">
        <a class="software-link" href="https://github.com/radiant-systems-lab/ProvScope" target="_blank">
          <i class="fa-brands fa-github"></i> GitHub
        </a>
      </div>

      <p class="software-funding"><strong>Funding:</strong> CISE-CSR</p>
    </article>

    <article class="software-card" id="floability">
      <div class="software-card-top">
        <h3><i class="fa-solid fa-diagram-project"></i> <a href="/softwares/floability/">Floability</a></h3>
        <span class="software-badge">Notebook Workflows</span>
      </div>

      <p>
        <strong>Floability</strong> enables rapid and portable deployment of notebooks expressing complex scientific workflows across
        a wide range of cyberinfrastructure. It addresses the challenge of incomplete workflows by capturing software dependencies,
        required datasets, and cluster hardware capabilities. It also targets translation between notebooks and workflows. Floability
        is collaboratively developed by the University of Notre Dame, the University of Missouri-Columbia, and the University of Illinois.
      </p>

      <div class="software-links">
        <a class="software-link" href="/softwares/floability/">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Project Page
        </a>
        <a class="software-link" href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2516579" target="_blank">
          <i class="fa-solid fa-hand-holding-dollar"></i> NSF Award
        </a>
      </div>

      <p class="software-funding"><strong>Funding:</strong> NSF</p>
    </article>

    <article class="software-card" id="flexiflow">
      <div class="software-card-top">
        <h3><i class="fa-solid fa-sliders"></i> <a href="/softwares/flexiflow/">FlexiFlow</a></h3>
        <span class="software-badge">ML Inference Systems</span>
      </div>

      <p>
        <strong>FlexiFlow</strong> is a system designed to improve both performance and accuracy of end-to-end machine learning workflows
        during inference time. The project is under active development and will be made open-source.
      </p>

      <div class="software-links">
        <a class="software-link" href="/softwares/flexiflow/">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Project Page
        </a>
      </div>

      <p class="software-funding"><strong>Funding:</strong> MU Seed Funding</p>
    </article>
  </section>
</div>
