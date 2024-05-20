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

document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;
    const totalSlides = slides.length;

    function showNextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % totalSlides;
        slides[currentSlide].classList.add('active');
    }

    setInterval(showNextSlide, 3000); // Change image every 3 seconds
});