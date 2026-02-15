const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    centerSlides: true,
    autoplay: {
        delay: 1000,
        disableOnInteraction: false,
      },

  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
      dynamicBullets: true,
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },


    breakpoints: {
      0: {
        slidesPerView: 2
      },
      500: {
        slidesPerView: 3
      },
      800: {
        slidesPerView: 4
      },
      1400: {
        slidesPerView: 5
      },
    }
  
  });

  

const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

ScrollReveal().reveal(".headTitle h1", {
  ...scrollRevealOption,
  origin: "top",
});

ScrollReveal().reveal(" .headContentP .paragraph", {
  ...scrollRevealOption,
  delay: 500,
  origin: "bottom",
});

ScrollReveal().reveal(".serviceContainer .servicesWording .serviceTitle ", {
  ...scrollRevealOption,
  origin: "top",
  delay: 1000,
});

ScrollReveal().reveal(".serviceContainer .servicesWording .servicesP", {
  ...scrollRevealOption,
});

ScrollReveal().reveal(".serviceContainer .serviceBtnContainer .servicesBtn", {
  ...scrollRevealOption,
  origin: "left",
});

ScrollReveal().reveal(".topServices1", {
  ...scrollRevealOption,
  origin: "right",
});


ScrollReveal().reveal(".workWithUsContainer .workWithTitle", {
  ...scrollRevealOption,
  origin: "top",
});

ScrollReveal().reveal(".workWithUsContainer .workwithP .trustContent", {
  ...scrollRevealOption,
  origin: "left",
  delay: 100
});

ScrollReveal().reveal(".workWithUsContainer .workwithP .loyaltyContent", {
  ...scrollRevealOption,
  delay: 200,
  origin: "right",
});

ScrollReveal().reveal(".workWithUsContainer .workwithP .confidentContent", {
  ...scrollRevealOption,
  delay: 300,
  origin: "right",
});


