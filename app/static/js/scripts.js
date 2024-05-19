function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var cover = document.querySelector('.cover');
    if (sidebar.style.left === '-250px') {
        sidebar.style.left = '0';
        cover.style.display = 'block';
    } else {
        sidebar.style.left = '-250px';
        cover.style.display = 'none';
    }
}

const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const slideContainer = document.querySelector('.slides');
const intervalTime = 5000; // Время переключения слайдов
let slideInterval;

// Функция для переключения слайдов
function nextSlide() {
    // Получаем текущий активный слайд
    const currentSlide = document.querySelector('.slide.active');
    // Перемещаем текущий слайд в конец списка слайдов
    slideContainer.appendChild(currentSlide);

    // Получаем новый текущий слайд, который стал первым после перемещения
    const newCurrentSlide = document.querySelector('.slide:first-child');
    // Добавляем класс 'active' новому текущему слайду
    newCurrentSlide.classList.add('active');
}

// Функция для запуска автоматического переключения слайдов
function startSlideShow() {
    slideInterval = setInterval(nextSlide, intervalTime);
}

// Запускаем автоматическое переключение слайдов при загрузке страницы
startSlideShow();
