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
