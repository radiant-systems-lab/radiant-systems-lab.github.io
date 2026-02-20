// --- CAROUSEL LOGIC ---
let currentSlide = 0;
const carouselImages = document.getElementById("carousel-images");
const dots = Array.from(
  document.querySelectorAll("#carousel-dots button, #carousel-dots span")
);
const carouselAutoMs = 3000;
let carouselTimerId = null;
const reduceMotionQuery = window.matchMedia
  ? window.matchMedia("(prefers-reduced-motion: reduce)")
  : null;

function updateCarousel() {
  if (!carouselImages || dots.length === 0) return;

  currentSlide = (currentSlide + dots.length) % dots.length;
  carouselImages.style.transform = `translateX(-${currentSlide * 100}%)`;

  dots.forEach((dot, idx) => {
    const isActive = idx === currentSlide;
    dot.classList.toggle("active", isActive);
    dot.setAttribute("aria-current", isActive ? "true" : "false");
  });
}

function nextSlide() {
  currentSlide += 1;
  updateCarousel();
}

function prevSlide() {
  currentSlide -= 1;
  updateCarousel();
}

function goToSlide(index) {
  currentSlide = index;
  updateCarousel();
}

function stopCarouselAutoplay() {
  if (carouselTimerId) {
    window.clearInterval(carouselTimerId);
    carouselTimerId = null;
  }
}

function startCarouselAutoplay() {
  stopCarouselAutoplay();
  if (!carouselImages || dots.length === 0) return;
  if (reduceMotionQuery && reduceMotionQuery.matches) return;

  carouselTimerId = window.setInterval(() => {
    nextSlide();
  }, carouselAutoMs);
}

if (carouselImages && dots.length > 0) {
  updateCarousel();
  startCarouselAutoplay();

  carouselImages.addEventListener("mouseenter", stopCarouselAutoplay);
  carouselImages.addEventListener("mouseleave", startCarouselAutoplay);
  carouselImages.addEventListener("focusin", stopCarouselAutoplay);
  carouselImages.addEventListener("focusout", startCarouselAutoplay);

  if (reduceMotionQuery) {
    if (typeof reduceMotionQuery.addEventListener === "function") {
      reduceMotionQuery.addEventListener("change", startCarouselAutoplay);
    } else if (typeof reduceMotionQuery.addListener === "function") {
      reduceMotionQuery.addListener(startCarouselAutoplay);
    }
  }
}

// --- RESEARCH AREAS ACCORDION LOGIC ---
const defaultAreaImage = "/images/research/Research_Area_Default.png";
const indexResearchAreas = [
  {
    title: "Reproducible and Accountable Systems",
    description:
      "Improving data-intensive distributed and parallel science workflows with reproducible and accountable containers.",
    image: "/images/research/RAS.png",
  },
  {
    title: "Transparent and Explainable AI",
    description:
      "Making data, algorithms, and decision-making processes in science workflows explainable and understandable.",
    image: "/images/research/TEAI.png",
  },
  {
    title: "Big Data Management",
    description:
      "Optimizing scientific data for volume, velocity, and variety via indexing, streaming, and semantic dataspaces.",
    image: "/images/research/BDM.png",
  },
  {
    title: "Scalable Cyberinfrastructure",
    description:
      "Enabling scientific research and innovation at scale by supporting advanced research through distributed, collaborative, and data-intensive capabilities.",
    image: "/images/research/SC.png",
  },
  {
    title: "Community and Policy",
    description: "Engaging with communities for artifact evaluation, guided by policy frameworks.",
    image: "/images/research/CP.png",
  },
];

const accordionContainer = document.querySelector("#index_research_areas .accordion");
const mainDisplayImg = document.getElementById("research-main-img");

if (accordionContainer && mainDisplayImg) {
  const resetAccordion = () => {
    const headers = accordionContainer.querySelectorAll(".accordion-header");
    const bodies = accordionContainer.querySelectorAll(".accordion-body");

    headers.forEach((headerEl) => {
      headerEl.classList.remove("open");
      headerEl.setAttribute("aria-expanded", "false");
      const symbolEl = headerEl.querySelector(".accordion-symbol");
      if (symbolEl) symbolEl.textContent = "+";
    });

    bodies.forEach((bodyEl) => {
      bodyEl.classList.remove("open");
      bodyEl.setAttribute("aria-hidden", "true");
    });
  };

  mainDisplayImg.src = defaultAreaImage;

  indexResearchAreas.forEach((area, index) => {
    const item = document.createElement("div");
    item.classList.add("accordion-item");

    const panelId = `index-area-panel-${index + 1}`;

    const header = document.createElement("button");
    header.type = "button";
    header.classList.add("accordion-header");
    header.setAttribute("aria-expanded", "false");
    header.setAttribute("aria-controls", panelId);

    const label = document.createElement("span");
    label.classList.add("accordion-label");
    label.textContent = area.title;
    label.style.pointerEvents = "none";

    const symbol = document.createElement("span");
    symbol.classList.add("accordion-symbol");
    symbol.textContent = "+";
    symbol.style.pointerEvents = "none";

    header.appendChild(label);
    header.appendChild(symbol);

    const body = document.createElement("div");
    body.id = panelId;
    body.classList.add("accordion-body");
    body.textContent = area.description;
    body.setAttribute("role", "region");
    body.setAttribute("aria-label", area.title);
    body.setAttribute("aria-hidden", "true");

    const toggleArea = () => {
      const isOpen = header.classList.contains("open");
      resetAccordion();

      if (!isOpen) {
        header.classList.add("open");
        body.classList.add("open");
        header.setAttribute("aria-expanded", "true");
        body.setAttribute("aria-hidden", "false");
        symbol.textContent = "-";
        mainDisplayImg.src = area.image;
      } else {
        mainDisplayImg.src = defaultAreaImage;
      }
    };

    header.addEventListener("click", toggleArea);
    header.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggleArea();
      }
    });

    item.appendChild(header);
    item.appendChild(body);
    accordionContainer.appendChild(item);

  });
}
