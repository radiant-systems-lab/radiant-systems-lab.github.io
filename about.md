---
layout: page
title: About
description: About the Radiant Lab
---

## Welcome to The RADIANT Systems Lab!



The Radiant Systems Lab directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> is located in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia (Mizzou)</a>. This lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. This lab aims to advance reproducible, accountable, explainable, and policy-aware data science by developing systems that enhance the reliability of data-intensive, distributed, and parallel scientific workflows through accountable and reproducible containerization. It also focuses on improving transparency in artificial intelligence by making data, algorithms, and decision-making processes within scientific workflows more interpretable and understandable.


<div style="width:800px; height:400px; margin:auto; position:relative;">
  <style>
    .carousel-container {
      position: relative;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    .carousel-slide {
      display: flex;
      width: 400%;
      height: 100%;
      animation: slide 24s infinite;
    }

    .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      flex-shrink: 0;
    }

    @keyframes slide {
      0%   { transform: translateX(0%); }
      20%  { transform: translateX(0%); }
      25%  { transform: translateX(-100%); }
      45%  { transform: translateX(-100%); }
      50%  { transform: translateX(-200%); }
      70%  { transform: translateX(-200%); }
      75%  { transform: translateX(-300%); }
      95%  { transform: translateX(-300%); }
      100% { transform: translateX(0%); }
    }

    /* Navigation Arrows */
    .nav-btn {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background-color: rgba(0,0,0,0.4);
      border: none;
      color: white;
      font-size: 24px;
      padding: 10px;
      cursor: pointer;
      z-index: 1;
    }

    .nav-btn:hover {
      background-color: rgba(0,0,0,0.7);
    }

    .prev-btn {
      left: 10px;
    }

    .next-btn {
      right: 10px;
    }

    /* Dot Indicators */
    .dots {
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      z-index: 1;
    }

    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background-color: rgba(255,255,255,0.6);
    }

    .dot.active {
      background-color: white;
    }
  </style>

  <div class="carousel-container">
    <div class="carousel-slide">
      <img src="images/icons/provenance.png" alt="Slide 1">
      <img src="images/icons/container.png" alt="Slide 2">
      <img src="images/icons/infrastructure.png" alt="Slide 3">
      <img src="images/icons/policy.png" alt="Slide 4">
    </div>

    <!-- Navigation buttons (non-functional without JS, but stylized) -->
    <button class="nav-btn prev-btn">&#10094;</button>
    <button class="nav-btn next-btn">&#10095;</button>

    <!-- Dots (static visual only) -->
    <div class="dots">
      <div class="dot active"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  </div>
</div>


The focus of the research performed in this lab includes but is not limited to:

- **Reproducible and Accountable Systems (RAS):**  
  Improving data-intensive, distributed, and parallel science workflows with reproducible and accountable containers.

- **Transparent and Explainable AI (XAI):**  
  Make data, algorithms, and decision-making processes in science workflows explainable and understandable.

- **Infrastructure and Policy (INP):**  
  Engage in resource and systems optimization of infrastructure, guided by policy frameworks.


