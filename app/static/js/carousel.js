/* 
 *  ============================
 *  ADD CAROUSEL FUNCTIONALITY
 *  ============================
*/
var slideWidth;
// Function to add listeners for click events to a carousel
function carouselise(carousel, index) {
  var animationDuration = '500ms';
  var track = carousel.querySelector(".carousel__track");
  var slides = Array.from(track.children);
  var nextButton = carousel.querySelector(".carousel__button--right");
  var prevButton = carousel.querySelector(".carousel__button--left");
  var dotsNav = carousel.querySelector(".carousel__nav");
  var dots = Array.from(dotsNav.children);

  var slideWidth = track.getBoundingClientRect().width;

  track.style.transition = 'transform ' + animationDuration + ' ease-out';

  // arrange slides next to one another
  var setSlidePosition = (slide, index) => {
    slide.style.left = slideWidth * index + 'px';
  };

  slides.forEach(setSlidePosition);

  var moveToSlide = (track, currentSlide, targetSlide) => {
    track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
    currentSlide.classList.remove('current-slide');
    targetSlide.classList.add('current-slide');
  }

  var updateDots = (currentDot, targetDot) => {
    currentDot.classList.remove('current-slide');
    targetDot.classList.add('current-slide');
  }

  var hideShowArrows = (prevButton, nextButton, targetIndex) => {
    if (targetIndex === 0) {
      prevButton.classList.add('is-hidden');
      nextButton.classList.remove('is-hidden');
    } else if (targetIndex === slides.length - 1) {
      prevButton.classList.remove('is-hidden');
      nextButton.classList.add('is-hidden');
    } else {
      prevButton.classList.remove('is-hidden');
      nextButton.classList.remove('is-hidden');
    }
  }

  // when I click left, move to left
  prevButton.addEventListener('click', e => {
    var carousel = e.target.closest('.carousel');
    var track = carousel.querySelector(".carousel__track");
    var slides = Array.from(track.children);
    var dotsNav = carousel.querySelector(".carousel__nav");

    var currentSlide = track.querySelector('.current-slide');
    var prevSlide = currentSlide.previousElementSibling;
    var currentDot = dotsNav.querySelector('.current-slide');
    var prevDot = currentDot.previousElementSibling;
    var targetIndex = slides.findIndex(slide => slide === prevSlide);

    // move to the next slide
    moveToSlide(track, currentSlide, prevSlide);
    updateDots(currentDot, prevDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  })

  // when I click right, move to right
  nextButton.addEventListener('click', e => {
    var carousel = e.target.closest('.carousel');
    var track = carousel.querySelector(".carousel__track");
    var slides = Array.from(track.children);
    var dotsNav = carousel.querySelector(".carousel__nav");

    var currentSlide = track.querySelector('.current-slide');
    var nextSlide = currentSlide.nextElementSibling;
    var currentDot = dotsNav.querySelector('.current-slide');
    var nextDot = currentDot.nextElementSibling;
    var targetIndex = slides.findIndex(slide => slide === nextSlide);
    
    // move to the next slide
    moveToSlide(track, currentSlide, nextSlide);
    updateDots(currentDot, nextDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  })

  // when I click a dot, go to that slide
  dotsNav.addEventListener('click', e => {
    var carousel = e.target.closest('.carousel');
    var track = carousel.querySelector(".carousel__track");
    var slides = Array.from(track.children);
    var dotsNav = carousel.querySelector(".carousel__nav");

    // what indicator was clicked?
    var targetDot = e.target.closest('button');
    // stop if not a dotnav button
    if (!targetDot) return;

    var currentSlide = track.querySelector('.current-slide');
    var currentDot = dotsNav.querySelector('.current-slide');
    var targetIndex = dots.findIndex(dot => dot === targetDot);
    var targetSlide = slides[targetIndex];

    moveToSlide(track, currentSlide, targetSlide);
    updateDots(currentDot, targetDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  });
}

// CREATE CAROUSEL EVENTS
window.onload = () => {
  var carousels = document.querySelectorAll('.carousel');
  
  carousels.forEach(carouselise);
}

/* 
 *  ============================
 *  ADD WINDOW RESIZE SMOOTHING
 *  ============================
*/
// Var
var rtime;
var timeout = false;
var delta = 200;

// Function
function resizeend() {
  if (new Date() - rtime < delta) {
      setTimeout(resizeend, delta);
  }
  else {
    timeout = false;

    var carousels = document.querySelectorAll('.carousel');

    carousels.forEach(function(carousel) {
      var track = carousel.querySelector(".carousel__track");
      var slides = Array.from(track.children);
      var currentSlide = track.querySelector('.current-slide');
      slideWidth = track.getBoundingClientRect().width;

      slides.forEach(setSlidePosition);
    });
  }
}

// Listener
window.addEventListener('resize', e => {
  rtime = new Date();
  if (timeout === false) {
      timeout = true;
      setTimeout(resizeend, delta);
  };
});