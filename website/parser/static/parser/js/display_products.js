document.addEventListener("DOMContentLoaded", function() {
    var productsWindow = document.getElementById("products_window");
    var headerHeight = document.querySelector("header").offsetHeight; // Получаем высоту header

    // Проматываем экран на 100vh вниз, учитывая высоту header
    window.scrollTo({
        top: productsWindow.getBoundingClientRect().top + window.scrollY - headerHeight,
        behavior: "smooth"
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var searchForm = document.getElementById("search-form");
    var searchInput = document.getElementById("main-search-input");

    searchForm.addEventListener("submit", function(event) {
        if (searchInput.value.length > 0) {
            document.querySelector("#main-search-button").style.backgroundImage = "url(static/parser/images/giphy.gif)";
            }
        });
});

document.addEventListener("DOMContentLoaded", function() {
    // Обработчик для закрытия модального окна при щелчке за его пределами
    window.onclick = function(event) {
        if (event.target == document.getElementById("modal")) {
            document.getElementById("modal").style.display = "none";
        }
    }
});