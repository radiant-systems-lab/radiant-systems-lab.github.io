---
layout: page
title: about
---

## Welcome to The RADIANT Systems Lab!



The Radiant Systems Lab directed by <a href="https://engineering.missouri.edu/faculty/tanu-malik/">Dr. Tanu Malik</a> is located in the <a href="https://engineering.missouri.edu/departments/eecs/">Department of Electrical Engineering and Computer Science</a> at the <a href="http://www.missouri.edu">University of Missouri-Columbia (Mizzou)</a>. This lab is a front runner in the design of reproducible, accountable, and trustworthy data-driven systems and infrastructure. This lab aims to advance reproducible, accountable, explainable, and policy-aware data science by developing systems that enhance the reliability of data-intensive, distributed, and parallel scientific workflows through accountable and reproducible containerization. It also focuses on improving transparency in artificial intelligence by making data, algorithms, and decision-making processes within scientific workflows more interpretable and understandable.  
<!-- <div style="max-width:800px; margin:auto; position:relative;"> -->
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

    .work-section {
      background-color: #fff;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 2.5rem;
    }
    
    /* Title styling */
    .work-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    
    .work-underline {
      border-bottom: 4px solid #FBBF24;
      padding-bottom: 0.25rem;
    }
    
    .work-text {
      color: #4B5563;
      line-height: 1.75;
      margin-bottom: 1.5rem;
    }
    
    *, *::before, *::after {
      box-sizing: border-box;
    }
    
    .work-button {
      display: inline-block;
      padding: 0.5rem 1.5rem;
      background-color: #000;
      color: #fff;
      font-weight: 500;
      border-radius: 0.5rem;
      border: 1px solid transparent;
      
      text-decoration: none;
      transition: background 0.3s, color 0.3s, border-color 0.3s;
    }
    
    .work-button:hover {
      background-color: #fff;
      color: #000;
      border-color: #000;
    }

    /* Contact Us Section */
    .contact-section {
      background-color: #fff;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 2.5rem;
    }
    
    .contact-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
    }
    
    .contact-underline {
      border-bottom: 4px solid #FBBF24;
      padding-bottom: 0.25rem;
    }
    
    .contact-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2rem;
    }
    
    @media (min-width: 768px) {
      .contact-content {
        flex-direction: row;
        align-items: flex-start;
      }
    }
    
    .contact-info {
      flex: 1 1 50%;
      color: #4B5563;
      line-height: 1.5;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .contact-link {
      color: #FBBF24;
      text-decoration: none;
    }
    
    .contact-link:hover {
      text-decoration: underline;
    }
    
    .contact-map {
      flex: 1 1 50%;
      height: 12rem;
      background-color: #D1D5DB;
      border-radius: 0.5rem;
      overflow: hidden;
    }
    
    .contact-map img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  </style>
  <!-- <div class="carousel-container">
    <div class="carousel-slide" id="carouselSlide">
      <img src="images/icons/provenance.png" alt="Slide 1">
      <img src="images/icons/container.png" alt="Slide 2">
      <img src="images/icons/infrastructure.png" alt="Slide 3">
      <img src="images/icons/policy.png" alt="Slide 4">
      <img src="images/icons/provenance.png" alt="Clone Slide 1">
    </div>
  </div> -->
  
<div class="container" style="padding: 0">
  <!-- History Section -->
  <section class="history-section" id="about_history">
    <div>
      <h2 class="history-title">
        <span class="history-underline">History</span>
      </h2>
    </div>
    <div class="history-content">
      <div class="image-placeholder">
        <div class="custom-carousel">
          <div class="carousel-images" id="carousel-images">
            <img src="images/icons/provenance.png" alt="1" />
            <img src="images/icons/container.png" alt="2" />
            <img src="images/icons/infrastructure.png" alt="3" />
          </div>
          <div class="carousel-buttons">
            <button onclick="prevSlide()">‹</button>
            <button onclick="nextSlide()">›</button>
          </div>
          <div class="carousel-dots" id="carousel-dots">
            <span onclick="goToSlide(0)"></span>
            <span onclick="goToSlide(1)"></span>
            <span onclick="goToSlide(2)"></span>
          </div>
        </div>
      </div>
      <div class="text-wrapper">
        <p>
          The history of the RADIANT Systems Lab traces back to the Data, Infrastructure, Computation, and Environments (DICE) Lab at <a href="https://www.depaul.edu/Pages/default.aspx">DePaul University</a>, which focused on foundational research in data provenance, computational reproducibility, and optimization within complex systems and virtual environments.  Today, the RADIANT Systems Lab continues this tradition and actively collaborates with researchers and scientists worldwide to advance the frontiers of reproducible and data-driven computing.
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
  <section class="work-section">
    <h2 class="work-title">
      <span class="work-underline">Work at Mizzou</span>
    </h2>
    <p class="work-text">
      Interested in joining Radiant Lab? We offer opportunities for graduate students, postdoctoral researchers, and visiting scholars to contribute to groundbreaking projects. At Mizzou, you’ll collaborate with experts, access state-of-the-art facilities, and impact real-world innovations.
    </p>
    <a href="mailto:join@radiantlab.edu" class="work-button">
      Join Our Team
    </a>
  </section>

  <section class="contact-section">
    <h2 class="contact-title">
      <span class="contact-underline">Contact Us</span>
    </h2>
    <div class="contact-content">
      <div class="contact-info">
        <p>
          Email:
          <a href="mailto:contact@radiantlab.edu" class="contact-link">
            contact@radiantlab.edu
          </a>
        </p>
        <p>
          Phone:
          <a href="tel:+1234567890" class="contact-link">
            +1 (234) 567-890
          </a>
        </p>
        <p>
          Address: University of Missouri - Columbia, Naka Hall, MO 65201
        </p>
      </div>
      <div class="contact-map">
        <!-- Swap in your actual map image path -->
        <img src="map.png" alt="Lab location map">
      </div>
    </div>
  </section>
</div>


<script src="https://radiant-systems-lab.github.io/assets/themes/twitter/js/about_history.js"></script>
