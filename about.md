---
layout: page
---

<div style="display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 10px; border-bottom: 1px solid #eee; margin-bottom: 15px;">
  <h2 style="margin: 0; border: none; padding: 0; color: #403F85; line-height: 1; font-weight: bold;">About the Lab</h2>
  <div class="quick-jump-links" style="font-size: 0.9rem;">
    <a href="#about_history" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">History</a>
    <a href="#stats-section" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">Stats</a>
    <a href="#work-section" style="margin-right: 15px; font-weight: bold; text-decoration: none; color: #0088cc;">Join Us</a>
    <a href="#contact-section" style="font-weight: bold; text-decoration: none; color: #0088cc;">Contact</a>
  </div>
</div>

<style>
  /* Reduce gaps between major sections */
  .container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1.5rem; /* Changed from 4rem to 1.5rem */
  }
  
  /* Tighten internal padding of sections */
  .history-section, .stats-section, .work-section, .contact-section {
    background-color: #fff;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1.5rem 2rem; /* Reduced from 2.5rem */
  }

  .history-title, .stats-title, .work-title, .contact-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #403F85;
  }
  
  .history-underline, .stats-underline, .work-underline, .contact-underline {
    border-bottom: 4px solid #FBBF24;
    padding-bottom: 0.25rem;
  }

  .history-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  @media (min-width: 768px) {
    .history-content { flex-direction: row; align-items: center; }
  }
  
  .image-placeholder img {
    width: 100%;
    max-width: 400px;
    height: auto;
    border-radius: 0.5rem;
  }
  
  .text-wrapper p, .work-text {
    color: #4B5563;
    line-height: 1.6;
    margin: 0;
  }

  /* Stats Grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    text-align: center;
  }
  
  @media (min-width: 640px) {
    .stats-grid { grid-template-columns: repeat(4, 1fr); }
  }
  
  .stat-number {
    display: block;
    font-size: 1.875rem;
    font-weight: 700;
    color: #403F85;
  }

  .work-button {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background-color: #403F85;
    color: #fff;
    font-weight: 500;
    border-radius: 0.5rem;
    text-decoration: none;
    transition: opacity 0.3s;
  }

  .work-button:hover { opacity: 0.8; color: #fff; text-decoration: none; }

  /* Contact Adjustments */
  .contact-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  @media (min-width: 768px) {
    .contact-content { flex-direction: row; }
  }
  
  .contact-info { flex: 1; }
  .contact-map { flex: 1; height: 200px; border-radius: 0.5rem; overflow: hidden; background: #eee; }
  .contact-map img { width: 100%; height: 100%; object-fit: cover; }
</style>

<div class="container">
  <section class="history-section" id="about_history">
    <h2 class="history-title"><span class="history-underline">History</span></h2>
    <div class="history-content">
      <div class="image-placeholder">
        <img src="https://radiant-systems-lab.github.io/images/icons/depaul_map.png" alt="History Image" />
      </div>
      <div class="text-wrapper">
        <p>
          The RADIANT Systems Lab traces its origins to the Data, Infrastructure, Computation, and Environments (DICE) Lab at 
          <a href="https://dice.cs.depaul.edu">DePaul University</a>. Building on this legacy, the RADIANT Systems Lab continues 
          to push the frontiers of reproducible and data-driven computing, actively collaborating with researchers and scientists worldwide.
        </p>
      </div>
    </div>
  </section>
  
  <section class="stats-section" id="stats-section">
    <h2 class="stats-title" style="text-align: center;"><span class="stats-underline">Lab Stats</span></h2>
    <div class="stats-grid">
      <div class="stats-item">
        <span class="stat-number">77</span>
        <p class="stat-label">Publications</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">22</span>
        <p class="stat-label">Team Members</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">12+</span>
        <p class="stat-label">Years of Excellence</p>
      </div>
      <div class="stats-item">
        <span class="stat-number">10+</span>
        <p class="stat-label">Collaborations</p>
      </div>
    </div>
  </section>

  <section class="work-section" id="work-section">
    <h2 class="work-title"><span class="work-underline">Work at Mizzou</span></h2>
    <p class="work-text">
      Interested in joining Radiant Lab? We offer opportunities for graduate students, postdoctoral researchers, and visiting scholars to contribute to groundbreaking projects.
    </p>
    <a href="https://radiant-systems-lab.github.io/people.html" class="work-button">Explore Open Positions</a>
  </section>

  <section class="contact-section" id="contact-section">
    <h2 class="contact-title"><span class="contact-underline">Contact Us</span></h2>
    <div class="contact-content">
      <div class="contact-info">
        <p>Email: <a href="mailto:tanu@missouri.edu" style="color:#0088cc;">tanu@missouri.edu</a></p>
        <p>Phone: <a href="tel:+5738849203" style="color:#0088cc;">+1 (573) 884-9203</a></p>
        <p>
          <strong>Address:</strong><br>
          416, S 6th St., Naka 311<br>
          Columbia, MO 65211
        </p>
      </div>
      <div class="contact-map">
        <img src="assets/map.jpg" alt="Lab location map">
      </div>
    </div>
  </section>
</div>

<script src="https://radiant-systems-lab.github.io/assets/themes/twitter/js/about_history.js"></script>