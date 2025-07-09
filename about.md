---
layout: page
title: about
---

## Welcome to The RADIANT Systems Lab!



The Radiant Systems Lab directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> is located in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia (Mizzou)</a>. This lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. This lab aims to advance reproducible, accountable, explainable, and policy-aware data science by developing systems that enhance the reliability of data-intensive, distributed, and parallel scientific workflows through accountable and reproducible containerization. It also focuses on improving transparency in artificial intelligence by making data, algorithms, and decision-making processes within scientific workflows more interpretable and understandable.


<div style="max-width:800px; margin:auto; position:relative;">
  <style>
    .carousel-container {
      position: relative;
      width: 100%;
      height: 400px;
      overflow: hidden;
      border-radius: 10px;
    }

    .carousel-slide {
      display: flex;
      transition: transform 0.5s ease-in-out;
      height: 100%;
    }

    .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: contain; /* Show full image inside frame */
      flex-shrink: 0;
    }

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
      z-index: 2;
    }

    .nav-btn:hover {
      background-color: rgba(0,0,0,0.7);
    }

    .prev-btn { left: 10px; }
    .next-btn { right: 10px; }

    .dots {
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      z-index: 2;
    }

    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background-color: rgba(255,255,255,0.5);
      cursor: pointer;
    }

    .dot.active {
      background-color: white;
    }
  </style>

  <div class="carousel-container">
    <div class="carousel-slide" id="carouselSlide">
      <img src="images/icons/provenance.png" alt="Slide 1">
      <img src="images/icons/container.png" alt="Slide 2">
      <img src="images/icons/infrastructure.png" alt="Slide 3">
      <img src="images/icons/policy.png" alt="Slide 4">
    </div>

    <button class="nav-btn prev-btn" onclick="moveSlide(-1)">&#10094;</button>
    <button class="nav-btn next-btn" onclick="moveSlide(1)">&#10095;</button>

    <div class="dots" id="dotsContainer">
      <div class="dot active" onclick="goToSlide(0)"></div>
      <div class="dot" onclick="goToSlide(1)"></div>
      <div class="dot" onclick="goToSlide(2)"></div>
      <div class="dot" onclick="goToSlide(3)"></div>
    </div>
  </div>

  <script>
    const slideContainer = document.getElementById('carouselSlide');
    const dots = document.querySelectorAll('.dot');
    const totalSlides = dots.length;
    let currentSlide = 0;

    function updateCarousel() {
      slideContainer.style.transform = `translateX(-${currentSlide * 100}%)`;
      dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
      });
    }

    function moveSlide(direction) {
      currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
      updateCarousel();
    }

    function goToSlide(index) {
      currentSlide = index;
      updateCarousel();
    }
  </script>
</div>


The focus of the research performed in this lab includes but is not limited to:

- **Reproducible and Accountable Systems (RAS):**  
  Improving data-intensive, distributed, and parallel science workflows with reproducible and accountable containers.

- **Transparent and Explainable AI (XAI):**  
  Make data, algorithms, and decision-making processes in science workflows explainable and understandable.

- **Infrastructure and Policy (INP):**  
  Engage in resource and systems optimization of infrastructure, guided by policy frameworks.

The history of the RADIANT Systems Lab traces back to the DICE (Data, Infrastructure, Computation, and Environments) Lab at <a href="https://www.depaul.edu/Pages/default.aspx">DePaul University</a>, which focused on foundational research in data provenance, computational reproducibility, and optimization within complex systems and virtual environments.  Today, the RADIANT Systems Lab continues this tradition and actively collaborates with researchers and scientists worldwide to advance the frontiers of reproducible and data-driven computing.
