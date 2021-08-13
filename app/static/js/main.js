function shuffle(array) {
  var currentIndex = array.length,  randomIndex;
  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }
  return array;
}

function carousel() {
  const animationDuration = '500ms';
  const track = document.querySelector(".carousel__track");
  const slides = Array.from(track.children);
  const nextButton = document.querySelector(".carousel__button--right");
  const prevButton = document.querySelector(".carousel__button--left");
  const dotsNav = document.querySelector(".carousel__nav");
  const dots = Array.from(dotsNav.children);

  var slideWidth = track.getBoundingClientRect().width;

  track.style.transition = 'transform ' + animationDuration + ' ease-out';

  // arrange slides next to one another
  const setSlidePosition = (slide, index) => {
    slide.style.left = slideWidth * index + 'px';
  };
  slides.forEach(setSlidePosition);

  const moveToSlide = (track, currentSlide, targetSlide) => {
    track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
    currentSlide.classList.remove('current-slide');
    targetSlide.classList.add('current-slide');
  }

  const updateDots = (currentDot, targetDot) => {
    currentDot.classList.remove('current-slide');
    targetDot.classList.add('current-slide');
  }

  const hideShowArrows = (prevButton, nextButton, targetIndex) => {
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

  window.addEventListener('resize', e => {
    track.style.transition = 'transform 0ms';

    const currentSlide = track.querySelector('.current-slide');

    slideWidth = track.getBoundingClientRect().width;
    slides.forEach(setSlidePosition);
    track.style.transform = 'translateX(-' + currentSlide.style.left + ')';

    setTimeout(() => { 
      track.style.transition = 'transform ' + animationDuration + ' ease-in';
      console.log(track.style.transition);
    }, 20);
  })

  // when I click left, move to left
  prevButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    const prevSlide = currentSlide.previousElementSibling;
    const currentDot = dotsNav.querySelector('.current-slide');
    const prevDot = currentDot.previousElementSibling;
    const targetIndex = slides.findIndex(slide => slide === prevSlide);

    // move to the next slide
    moveToSlide(track, currentSlide, prevSlide);
    updateDots(currentDot, prevDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  })

  // when I click right, move to right
  nextButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    const nextSlide = currentSlide.nextElementSibling;
    const currentDot = dotsNav.querySelector('.current-slide');
    const nextDot = currentDot.nextElementSibling;
    const targetIndex = slides.findIndex(slide => slide === nextSlide);
    
    // move to the next slide
    moveToSlide(track, currentSlide, nextSlide);
    updateDots(currentDot, nextDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  })

  // when I click a dot, go to that slide
  dotsNav.addEventListener('click', e => {
    // what indicator was clicked?
    const targetDot = e.target.closest('button');
    // stop if not a dotnav button
    if (!targetDot) return;

    const currentSlide = track.querySelector('.current-slide');
    const currentDot = dotsNav.querySelector('.current-slide');
    const targetIndex = dots.findIndex(dot => dot === targetDot);
    const targetSlide = slides[targetIndex];

    moveToSlide(track, currentSlide, targetSlide);
    updateDots(currentDot, targetDot);
    hideShowArrows(prevButton, nextButton, targetIndex);
  })

}

window.onload = () => {
  var colWidthOptions = ["0", "10", "20", "30", "40"];
  colWidthOptions = shuffle(colWidthOptions);

  var index = 0;

  list_items = document.querySelectorAll(".content-list-item");

  for (var i = 0; i < list_items.length; i++) {
    if (index == colWidthOptions.length) {
      colWidthOptions = shuffle(colWidthOptions);
      index = 0;
    }

    if (colWidthOptions[index] != "0") {
      let div = document.createElement("div");
      div.classList.add("col", "col-" + colWidthOptions[index], "col-space");
      let split = list_items[i];
      split.insertBefore(div, split.firstChild);
    }

    index++;
  }

  carousel();
}

