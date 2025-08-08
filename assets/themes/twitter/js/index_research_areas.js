// index page Carousel - Image Slides
let currentSlide = 0;
const totalSlides = 3;
const images = document.getElementById("carousel-images");
const dots = document.getElementById("carousel-dots").children;

function updateCarousel() {
  images.style.transform = `translateX(-${currentSlide * 100}%)`;
  for (let i = 0; i < dots.length; i++) {
    dots[i].classList.remove("active");
  }
  dots[currentSlide].classList.add("active");
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  updateCarousel();
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  updateCarousel();
}

function goToSlide(index) {
  currentSlide = index;
  updateCarousel();
}

setInterval(() => {
  nextSlide();
}, 3000);

updateCarousel();


// index page Research Areas - click and show
const index_researchAreas = [
  {
    title: 'Reproducible and Accountable Systems',
    description: 'Improving data-intensive distributed and parallel science workflows with reproducible and accountable containers.',
  },
  {
    title: 'Transparent and Explainable AI',
    description: 'Making data, algorithms, and decision-making processes in science workflows explainable and understandable.',
  },
  {
    title: 'Big Data Management',
    description: 'Optimizing scientific data for volume, velocity, and variety via indexing, streaming, and semantic dataspaces.',
  },
  {
    title: 'Scalable Cyberinfrastructure',
    description: 'Enabling scientific research and innovation at scale by supporting advanced research through distributed, collaborative, and data-intensive capabilities.',
  },
  {
    title: 'Community and Policy',
    description: 'Engaging with communities for artifact evaluation, guided by policy frameworks.',
  },
];

const accordionContainer = document.querySelector('#index_research_areas .accordion');

index_researchAreas.forEach((area, index) => {
  const item = document.createElement('div');
  item.classList.add('accordion-item');

  const header = document.createElement('div');
  header.classList.add('accordion-header');
  header.textContent = area.title;

  const symbol = document.createElement('span');
  symbol.textContent = '+';
  header.appendChild(symbol);

  const body = document.createElement('div');
  body.classList.add('accordion-body');
  body.textContent = area.description;

  header.addEventListener('click', () => {
    const isOpen = header.classList.contains('open');
    document.querySelectorAll('.accordion-header').forEach(h => {
      h.classList.remove('open');
      h.querySelector('span').textContent = '+';
    });
    document.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));

    if (!isOpen) {
      header.classList.add('open');
      body.classList.add('open');
      symbol.textContent = '−';
    }
  });

  item.appendChild(header);
  item.appendChild(body);
  accordionContainer.appendChild(item);
});
