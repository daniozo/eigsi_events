const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
// const pauseBtn = document.getElementById('pauseBtn');
let currentIndex = 0;
let intervalId;
let isPaused = false;

slides.forEach((slide, index) => {
   slide.style.left = index * 100 + '%';
});

function moveToSlide(index) {
   track.style.transform = 'translateX(-' + (index * 100) + '%)';
   currentIndex = index;
}

function nextSlide() {
   if (currentIndex === slides.length - 1) {
      moveToSlide(0);
   } else {
      moveToSlide(currentIndex + 1);
   }
}

function prevSlide() {
   if (currentIndex === 0) {
      moveToSlide(slides.length - 1);
   } else {
      moveToSlide(currentIndex - 1);
   }
}

// function togglePause() {
//    if (isPaused) {
//       isPaused = false;
//       pauseBtn.textContent = 'Pause';
//       startAutoSlide();
//    } else {
//       isPaused = true;
//       pauseBtn.textContent = 'Play';
//       clearInterval(intervalId);
//    }
// }

function startAutoSlide() {
   intervalId = setInterval(nextSlide, 3000);
}

prevBtn.addEventListener('click', () => {
   prevSlide();
   if (!isPaused) {
      clearInterval(intervalId);
      startAutoSlide();
   }
});

nextBtn.addEventListener('click', () => {
   nextSlide();
   if (!isPaused) {
      clearInterval(intervalId);
      startAutoSlide();
   }
});

// pauseBtn.addEventListener('click', togglePause);

startAutoSlide();