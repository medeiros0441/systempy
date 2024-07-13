const feedbackItems = [
  { id: 'image-1', name: 'João Silva' },
  { id: 'image-2', name: 'Mariana Costa' },
  { id: 'image-3', name: 'Carlos Oliveira' },
  { id: 'image-4', name: 'Beatriz Santos' },
  { id: 'image-5', name: 'Pedro Almeida' },
  { id: 'image-6', name: 'Larissa Fernandes' },
  { id: 'image-7', name: 'Ricardo Moreira' },
  { id: 'image-8', name: 'Sofia Lima' },
  { id: 'image-9', name: 'Mateus Rocha' },
  { id: 'image-10', name: 'Juliana Cardoso' }
];

function isFemale(name) {
  const femaleNames = ['Ana', 'Mariana', 'Beatriz', 'Larissa', 'Juliana', 'Sofia'];
  return femaleNames.some(femaleName => name.toLowerCase().includes(femaleName.toLowerCase()));
}

function fetchProfileImage(elementId, gender) {
  const genderType = gender ? 'women' : 'men';
  const randomNumber = Math.floor(Math.random() * 99); // Random number between 0 and 99
  const imgUrl = `https://randomuser.me/api/portraits/${genderType}/${randomNumber}.jpg`;
  document.getElementById(elementId).src = imgUrl;
}

document.addEventListener("DOMContentLoaded", function() {
  animacao_carrossel();
});
function animacao_carrossel() {
  document.querySelectorAll('.item--carousel').forEach(item => {
    item.addEventListener('click', function() {
      const elAlreadyActive = document.querySelector('.item--carousel.active');
      const elAlreadyActivePosition = Array.from(document.querySelectorAll('.item--carousel')).indexOf(elAlreadyActive);
      document.querySelectorAll('.item--carousel').forEach(el => el.classList.remove('active'));
      this.classList.add('active');
      this.classList.remove("showme");

      const elLength = document.querySelectorAll('.item--carousel').length;
      const elPosition = Array.from(document.querySelectorAll('.item--carousel')).indexOf(this);
      const elBeforeThis = this.previousElementSibling ? Array.from(document.querySelectorAll('.item--carousel')).indexOf(this.previousElementSibling) : -1;
      const elAfterThis = this.nextElementSibling ? Array.from(document.querySelectorAll('.item--carousel')).indexOf(this.nextElementSibling) : -1;

      if (elBeforeThis >= 0 && elAfterThis !== -1) {
        if (elPosition > elAlreadyActivePosition) {
          if (this.previousElementSibling && this.previousElementSibling.previousElementSibling) {
            this.previousElementSibling.previousElementSibling.classList.add('hideme', 'redux');
          }
        } else if (elPosition < elAlreadyActivePosition) {
          if (this.previousElementSibling) {
            this.previousElementSibling.classList.remove('hideme', 'redux');
            this.previousElementSibling.classList.add('showme');
          }
        }
      }

      updateCarouselActivePosition();
    });
  });

  window.addEventListener('resize', updateCarouselActivePosition);

  document.querySelectorAll('.indicators--carousel span').forEach((indicator, index) => {
    indicator.addEventListener('click', function() {
      document.querySelectorAll('.indicators--carousel span').forEach(el => el.classList.remove('active'));
      this.classList.add('active');

      const pos = index;
      document.querySelectorAll('.inner--carousel .item--carousel').forEach(item => {
        item.classList.remove('active');
        item.style.order = '10';
      });

      const activeItem = document.querySelectorAll('.item--carousel')[pos];
      activeItem.classList.add('active');
      activeItem.style.order = '1';
    });
  });

  document.querySelector('.person-carousel .inner--carousel').addEventListener('touchstart', function(event) {
    const xClick = event.touches[0].pageX;

    const touchMoveHandler = function(event) {
      const xMove = event.touches[0].pageX;
      if (Math.floor(xClick - xMove) > 5) {
        swipeCarousel(true); // Movimento para a esquerda
      } else if (Math.floor(xClick - xMove) < -5) {
        swipeCarousel(false); // Movimento para a direita
      }
    };

    this.addEventListener('touchmove', touchMoveHandler);

    this.addEventListener('touchend', function() {
      this.removeEventListener('touchmove', touchMoveHandler);
    }, { once: true });
  });

  function swipeCarousel(isLeft) {
    const active = document.querySelector('.item--carousel.active');
    if (isLeft && active.previousElementSibling) {
      document.querySelectorAll('.item--carousel').forEach(item => {
        item.classList.remove('active');
        item.style.order = '10';
      });
      active.previousElementSibling.classList.add('active');
      active.previousElementSibling.style.order = '1';
      const activeIndicator = document.querySelector('.indicators--carousel span.active');
      activeIndicator.classList.remove('active');
      if (activeIndicator.previousElementSibling) {
        activeIndicator.previousElementSibling.classList.add("active");
      }
    } else if (!isLeft && active.nextElementSibling) {
      document.querySelectorAll('.item--carousel').forEach(item => {
        item.classList.remove('active');
        item.style.order = '10';
      });
      active.nextElementSibling.classList.add('active');
      active.nextElementSibling.style.order = '1';
      const activeIndicator = document.querySelector('.indicators--carousel span.active');
      activeIndicator.classList.remove('active');
      if (activeIndicator.nextElementSibling) {
        activeIndicator.nextElementSibling.classList.add("active");
      }
    }
  }

  function updateCarouselActivePosition() {
    const items = document.querySelectorAll(".inner--carousel .item--carousel");
    items.forEach(item => item.classList.remove('active'));
    if (window.innerWidth < 768) {
      items[0].classList.add('active');
    } else {
      if (items[1]) items[1].classList.add('active');
    }
  }
}
