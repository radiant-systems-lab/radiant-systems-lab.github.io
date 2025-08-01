---
layout: page
title: about
---

## Welcome to The RADIANT Systems Lab!



The Radiant Systems Lab directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> is located in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia (Mizzou)</a>. This lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. This lab aims to advance reproducible, accountable, explainable, and policy-aware data science by developing systems that enhance the reliability of data-intensive, distributed, and parallel scientific workflows through accountable and reproducible containerization. It also focuses on improving transparency in artificial intelligence by making data, algorithms, and decision-making processes within scientific workflows more interpretable and understandable.  


The history of the RADIANT Systems Lab traces back to the Data, Infrastructure, Computation, and Environments (DICE) Lab at <a href="https://www.depaul.edu/Pages/default.aspx">DePaul University</a>, which focused on foundational research in data provenance, computational reproducibility, and optimization within complex systems and virtual environments.  Today, the RADIANT Systems Lab continues this tradition and actively collaborates with researchers and scientists worldwide to advance the frontiers of reproducible and data-driven computing.

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
      object-fit: contain;
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

    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 2rem;
      display: flex;
      flex-direction: column;
      gap: 4rem;
    }
    
    .history-section {
      background-color: #fff;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 2.5rem;
    }
    
    .history-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    
    .history-underline {
      border-bottom: 4px solid #FBBF24;
      padding-bottom: 0.25rem;
    }
    
    .history-content {
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }
    
    @media (min-width: 768px) {
      .history-content {
        flex-direction: row;
      }
    }
    
    .image-wrapper {
      flex: 1 1 50%;
    }
    
    .image-wrapper img {
      width: 100%;
      height: 16rem;
      object-fit: cover;
      border-radius: 0.5rem;
      background-color: #D1D5DB;
    }
    
    .text-wrapper {
      flex: 1 1 50%;
      display: flex;
      align-items: center;
    }
    
    .text-wrapper p {
      color: #4B5563;
      line-height: 1.75;
    }
    
    .stats-section {
      background-color: #fff;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 2.5rem 0;
    }
    
    .stats-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      text-align: center;
    }
    
    .stats-underline {
      border-bottom: 4px solid #FBBF24;
      padding-bottom: 0.25rem;
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
      text-align: center;
    }
    
    @media (min-width: 640px) {
      .stats-grid {
        grid-template-columns: repeat(4, 1fr);
      }
    }
    
    .stats-item .stat-number {
      display: block;
      font-size: 1.875rem;
      font-weight: 600;
      color: #000;
    }
    
    .stats-item .stat-label {
      color: #4B5563;
      margin-top: 0.25rem;
    }
  </style>

  <div class="carousel-container">
    <div class="carousel-slide" id="carouselSlide">
      <img src="images/icons/provenance.png" alt="Slide 1">
      <img src="images/icons/container.png" alt="Slide 2">
      <img src="images/icons/infrastructure.png" alt="Slide 3">
      <img src="images/icons/policy.png" alt="Slide 4">
      <!-- Clone of the first image for smooth transition -->
      <img src="images/icons/provenance.png" alt="Clone Slide 1">
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
    let currentSlide = 0;
    const slideContainer = document.getElementById("carouselSlide");
    const dots = document.querySelectorAll(".dot");
    const totalSlides = dots.length; // excludes clone

    function showSlide(index, skipTransition = false) {
      const realIndex = (index + totalSlides) % totalSlides;
      currentSlide = index;
      if (skipTransition) {
        slideContainer.style.transition = "none";
      } else {
        slideContainer.style.transition = "transform 0.5s ease-in-out";
      }
      slideContainer.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((dot, i) => dot.classList.toggle("active", i === realIndex));
    }

    function moveSlide(step) {
      if (currentSlide === totalSlides - 1 && step === 1) {
        // Going from last real slide to clone
        showSlide(currentSlide + 1);
        setTimeout(() => {
          showSlide(0, true); // jump instantly to first (real) slide
        }, 500); // match transition duration
      } else if (currentSlide === 0 && step === -1) {
        // Going from first to last
        slideContainer.style.transition = "none";
        slideContainer.style.transform = `translateX(-${totalSlides * 100}%)`;
        currentSlide = totalSlides;
        setTimeout(() => moveSlide(-1), 20);
      } else {
        showSlide(currentSlide + step);
      }
    }

    function goToSlide(index) {
      showSlide(index);
    }

    // Auto-transition every 2 seconds
    setInterval(() => {
      moveSlide(1);
    }, 2000);

    // Initialize
    showSlide(0);
  </script>
</div>

<div class="container">
  <!-- History Section -->
  <section class="history-section">
    <h2 class="history-title">
      <span class="history-underline">History</span>
    </h2>
    <div class="history-content">
      <div class="image-wrapper">
        <!-- Swap in your actual image path -->
        <img src="history.jpg" alt="History image">
      </div>
      <div class="text-wrapper">
        <p>
          Founded in [Year], Radiant Lab has continuously pushed the boundaries of interdisciplinary research at Mizzou. Our journey began with a small group of visionaries committed to transforming cutting-edge theoretical insights into practical solutions that serve both academia and industry.
        </p>
      </div>
    </div>
  </section>
  <section class="stats-section">
    <h2 class="stats-title">
      <span class="stats-underline">Stats</span>
    </h2>
    <div class="stats-grid">
      <div class="stats-item">
        <span class="stat-number">50+</span>
        <p class="stat-label">Publications</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">20</span>
        <p class="stat-label">Team Members</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">10</span>
        <p class="stat-label">Years of Excellence</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">5</span>
        <p class="stat-label">Departments Collaborated</p>
      </div>
    </div>
  </section>
</div>
