---
layout: page
title: flexiflow
permalink: /softwares/flexiflow/
---


<!-- Navigation Bar -->
<div class="navbar">
    <div class="navbar-inner">
        <ul class="nav">
            <li><a href="#about">about</a></li>
            <li><a href="#docs">docs</a></li>
            <li><a href="#code">code</a></li>
            <li><a href="#papers">papers</a></li>
            <li><a href="#team">team</a></li>
        </ul>
    </div>
</div>


## about

**FlexiFlow** is a new programming model that is aimed at automatic model switching to maximise performance in machine learning workflows.
The current programming paradigm is to chose the ML model with the best performance and utilize it through the entire workflow. While this may suffice, it may still lead to suboptimal performance even in simpler workflows. Take the example below:

<div style="text-align:center; margin: 2em 0;">
  <embed src="/images/softwares/FlexiFlow-Arch.png" type="application/pdf" width="90%" height="600px" style="border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);" />
  <p style="font-size:0.9em; color:#555;">If the PDF does not display, <a href="/images/softwares/flexiflow-arch.pdf" target="_blank">click here to download or view it</a>.</p>
</div>

Supppose that Model 1 performs suboptimally on a subset of the input called Input A. This Model 1 gives Output 1 for the Input A which does not satisfy a user defined evaluation metric. For this specific input, there exists a Model 2 giving Output 2 which satisfies the evaluation metric.
On a holistic level, the second model may not perform better than the primary model on the entire dataset, but for this specific subset of the data, it may be better to use the secondary model instead.

Current systems lack the capability to adaptively switch between models based on performance, forcing users to manually run the models in a user-defined sequence. This may be feasible for smaller pipelines, but completly infeasible for bigger and more complex workflows with multiple moving components.

Thus, **FlexiFlow** was created to solve this problem. It uses reinforcement learning to learn the order of using models at each node to maximise performance. The reward to the learning algorithm is given by user defined evaluation metrics or assertions.

The learning algorithm is a hybrid thomson sampling strategy that takes into account information at the node level and the job level to effectively learn the optimal order of models to run to reduce runtime and maximise accuracy.

-------------

## docs

**FlexiFlow** docs, add here.

-------------

## code

You can find the entire repository here: Link to the github repository here.

-------------

## papers

Add the upcoming papers here

-------------

## team

<div class="flex-container people image-container">
{% assign flexiflow_team = site.data.flexiflow %}
{% for person in flexiflow_team %}
  {% include person_image image=person.image caption=person.name link=person.website title=person.name %}
{% endfor %}
</div>

