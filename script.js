var swiper = new Swiper(".swiper", {
  // Optional parameters
  direction: 'horizontal',
  loop: true,
  centeredSlides: true,
  spaceBetween: 30,

  preventClicks: false,
  preventClicksPropagation: false,

  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  breakpoints: {
    0: {
      slidesPerView: 1
    },

    768: {
      slidesPerView: 2
    },


    1400: {
      slidesPerView: 3
    },

  }

});


const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

ScrollReveal().reveal(".headTitle", {
  ...scrollRevealOption,
  origin: "top",
});

ScrollReveal().reveal(".missionContent .missionTitle ", {
  ...scrollRevealOption,
  origin: "top",
});

ScrollReveal().reveal(".missionContent .missionP", {
  ...scrollRevealOption,
  origin: "bottom",
  delay: 300,
});

ScrollReveal().reveal(".visionContent .visionTitle ", {
  ...scrollRevealOption,
  origin: "bottom",
});

ScrollReveal().reveal(".visionContent .visionP", {
  ...scrollRevealOption,
  origin: "bottom",
  delay: 300,
});

ScrollReveal().reveal(".aboutContent1 .passionateExperts ", {
  ...scrollRevealOption,
  origin: "left",
});

ScrollReveal().reveal(".aboutContent1 .passionExpertImgContainer", {
  ...scrollRevealOption,
  origin: "right",
  delay: 300,
});

ScrollReveal().reveal(".aboutContent2 .analyticalApproach ", {
  ...scrollRevealOption,
  origin: "right",
});

ScrollReveal().reveal(".aboutContent2 .analyticalApproachImgContainer ", {
  ...scrollRevealOption,
  origin: "left",
  delay: 300,
});

ScrollReveal().reveal(".aboutContent3 .industrySuccess  ", {
  ...scrollRevealOption,
  origin: "left",
});

ScrollReveal().reveal(".aboutContent3 .industrySuccessImgContainer ", {
  ...scrollRevealOption,
  origin: "right",
  delay: 300,
});



