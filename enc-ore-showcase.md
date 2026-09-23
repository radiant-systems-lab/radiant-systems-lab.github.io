---
title: Enc-ORE Research Demonstration
layout: page
description: Enc-ORE turns scientific repositories into launchable, reproducible notebook environments for Audit and Repeat execution.
permalink: /enc-ore-showcase/
stylesheet: /assets/themes/twitter/css/enc-ore-showcase.css
---

<main class="encore-showcase">
  <section class="encore-hero" aria-labelledby="encore-title">
    <div class="encore-kicker">NASA Science Cloud Demonstration</div>
    <h1 id="encore-title">Enc-ORE</h1>
    <p class="encore-expansion">Executable Open Reproducible Environments</p>
    <p class="encore-lead">Agent-assisted infrastructure that turns scientific repositories into launchable notebook environments for capturing, sharing, and repeating computational research.</p>
    <div class="encore-actions">
      <a class="encore-button encore-button-primary" href="#presentation">
        <i class="fa-solid fa-play" aria-hidden="true"></i>
        View presentation
      </a>
      <a class="encore-button encore-button-secondary" href="https://d1p16plaj9ha41.cloudfront.net/" target="_blank" rel="noopener noreferrer">
        <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>
        Explore live portal
      </a>
    </div>
    <dl class="encore-stats" aria-label="Demonstration summary">
      <div><dt>8</dt><dd>curated workflows</dd></div>
      <div><dt>2</dt><dd>notebook kernels</dd></div>
      <div><dt>On demand</dt><dd>cloud execution</dd></div>
    </dl>
  </section>

  <section class="encore-section encore-presentation" id="presentation" aria-labelledby="presentation-title">
    <div class="encore-section-heading">
      <span>Presentation</span>
      <h2 id="presentation-title">Reproducible Research, Built Autonomously</h2>
      <p>The presentation follows one scientific workflow from its source repository through audited execution, portable capture, and independent repeat.</p>
    </div>
    <div class="encore-video-player">
      <iframe
        src="https://www.youtube.com/embed/LxHAwlRH9YA"
        title="Radiant Systems Lab project presentation"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen>
      </iframe>
    </div>
  </section>

  <section class="encore-section" aria-labelledby="workflow-title">
    <div class="encore-section-heading">
      <span>Demonstration flow</span>
      <h2 id="workflow-title">From research repository to repeatable result</h2>
    </div>
    <ol class="encore-flow">
      <li>
        <span class="encore-flow-number">1</span>
        <div><h3>Prepare</h3><p>The Experiment Setup Agent examines a public research repository and prepares separate Audit and Repeat launch paths.</p></div>
      </li>
      <li>
        <span class="encore-flow-number">2</span>
        <div><h3>Audit</h3><p>An on-demand JupyterLab environment runs the notebook while the Audit kernel captures the code, libraries, data, and programs used.</p></div>
      </li>
      <li>
        <span class="encore-flow-number">3</span>
        <div><h3>Share</h3><p>The captured execution is packaged and exposed through a shareable container link for transfer to another environment.</p></div>
      </li>
      <li>
        <span class="encore-flow-number">4</span>
        <div><h3>Repeat</h3><p>A separate Repeat environment opens the capture and re-executes the workflow from its recorded computational context.</p></div>
      </li>
    </ol>
  </section>

  <section class="encore-section encore-science" aria-labelledby="science-title">
    <div class="encore-section-heading">
      <span>Featured science workflow</span>
      <h2 id="science-title">IMERG storm analysis at distributed scale</h2>
      <p>The live demonstration processes NASA IMERG precipitation data to identify connected precipitation features, track storms through time, and render geospatial outputs. Dask workers provide on-demand parallel compute while the notebook coordinates the scientific workflow.</p>
    </div>
    <div class="encore-science-grid">
      <article>
        <i class="fa-solid fa-cloud-rain" aria-hidden="true"></i>
        <h3>Scientific input</h3>
        <p>Time-ordered precipitation observations stored as NetCDF files.</p>
      </article>
      <article>
        <i class="fa-solid fa-diagram-project" aria-hidden="true"></i>
        <h3>Processing</h3>
        <p>Masking, connected-component labeling, temporal feature tracking, and visualization.</p>
      </article>
      <article>
        <i class="fa-solid fa-layer-group" aria-hidden="true"></i>
        <h3>Reproducible output</h3>
        <p>Tracked storm products, maps, and the captured execution needed to repeat them.</p>
      </article>
    </div>
    <a class="encore-text-link" href="https://github.com/radiant-systems-lab/ImergView-Dask" target="_blank" rel="noopener noreferrer">
      View the IMERG workflow repository <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>
    </a>
  </section>

  <section class="encore-section" aria-labelledby="experiments-title">
    <div class="encore-section-heading">
      <span>Curated workflows</span>
      <h2 id="experiments-title">A broader reproducibility testbed</h2>
      <p>The portal brings together workflows spanning precipitation, atmospheric chemistry, marine ecosystems, geospatial statistics, and forest dynamics.</p>
    </div>
    <div class="encore-experiment-list" aria-label="Curated scientific workflows">
      <span>IMERG Dask</span>
      <span>IMERG Feature Database</span>
      <span>IMERG Event Analysis</span>
      <span>Kelp Forest Projection</span>
      <span>Aura OMI Ozone Kriging</span>
      <span>POMD Precipitation Features</span>
      <span>South America Storms</span>
      <span>Tree Mortality Workflow</span>
    </div>
  </section>

  <section class="encore-section encore-presenter" aria-labelledby="presenter-title">
    <img src="{{ BASE_PATH }}/images/people/Tanu.jpg" alt="Tanu Malik">
    <div>
      <span class="encore-label">Presented by</span>
      <h2 id="presenter-title">Tanu Malik</h2>
      <p class="encore-role">Associate Professor, David L. Payne Department of Electrical Engineering and Computer Science, University of Missouri</p>
      <p>Dr. Malik leads the Radiant Systems Lab, where research focuses on reproducible distributed and parallel systems, big-data management, and trustworthy AI.</p>
      <a class="encore-text-link" href="https://engineering.missouri.edu/faculty/tanu-malik/" target="_blank" rel="noopener noreferrer">View faculty profile <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
    </div>
  </section>

  <section class="encore-section encore-qr" aria-labelledby="qr-title">
    <div>
      <span class="encore-label">Continue exploring</span>
      <h2 id="qr-title">Take the demonstration with you</h2>
      <p>Scan the code to revisit this presentation, open the live portal, and explore the research workflow after the event.</p>
      <a class="encore-button encore-button-dark" href="{{ BASE_PATH }}/assets/images/enc-ore-showcase-qr.svg" download>
        <i class="fa-solid fa-download" aria-hidden="true"></i>
        Download QR code
      </a>
    </div>
    <figure>
      <img src="{{ BASE_PATH }}/assets/images/enc-ore-showcase-qr.svg" alt="QR code for the Enc-ORE research demonstration page">
      <figcaption>radiant-systems-lab.github.io/enc-ore-showcase/</figcaption>
    </figure>
  </section>

  <p class="encore-note">Enc-ORE is a Radiant Systems Lab research demonstration. References to NASA datasets and NASA Science Cloud describe the demonstrated research context and do not imply endorsement.</p>
</main>
