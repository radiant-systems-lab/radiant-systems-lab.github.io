// // About Page History Carousel - Image Slides
// let currentSlide = 0;
// const totalSlides = 3;
// const images = document.getElementById("carousel-images");
// const dots = document.getElementById("carousel-dots").children;

// function updateCarousel() {
//   images.style.transform = `translateX(-${currentSlide * 100}%)`;
//   for (let i = 0; i < dots.length; i++) {
//     dots[i].classList.remove("active");
//   }
//   dots[currentSlide].classList.add("active");
// }

// function nextSlide() {
//   currentSlide = (currentSlide + 1) % totalSlides;
//   updateCarousel();
// }

// function prevSlide() {
//   currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
//   updateCarousel();
// }

// function goToSlide(index) {
//   currentSlide = index;
//   updateCarousel();
// }

// setInterval(() => {
//   nextSlide();
// }, 3000);

// updateCarousel();