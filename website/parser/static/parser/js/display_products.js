let main;

document.addEventListener("DOMContentLoaded", function() {
    scrollToTop = document.querySelector('#scroll-to-top')
    main = document.querySelector('main');

    window.addEventListener('scroll', toggleScrollToTop);
    scrollToTop.addEventListener('click', scrollToTopFunction);
});

// scrolling
document.addEventListener("DOMContentLoaded", function () {
    let productsWindow = document.getElementById("products_window");
    let headerHeight = document.querySelector("header").offsetHeight; // Получаем высоту header

    let product = document.getElementsByClassName("product");

    if (product.length > 0) {
        window.scrollTo({
            top: productsWindow.getBoundingClientRect().top + window.scrollY - headerHeight,
            behavior: "smooth"
        });
    }
});

// animation while search process
document.addEventListener("DOMContentLoaded", function () {
    let searchForm = document.getElementById("search-form");
    let searchInput = document.getElementById("id_q");

    searchForm.addEventListener("submit", function (event) {
        if (searchInput.value.length > 0) {
            document.querySelector("#main-search-button").style.backgroundImage = "url(static/parser/images/giphy.gif)";
        }
    });
});

// handler for modal window closing
document.addEventListener("DOMContentLoaded", function () {
    window.onclick = function (event) {
        if (event.target == document.getElementById("modal") || event.target == document.getElementById("close-modal")) {
            document.getElementById("modal").style.display = "none";
        }
    }
});

// Scroll up

function toggleScrollToTop() {
    if (window.scrollY + 5 >= main.offsetHeight) {
        scrollToTop.style.display = 'block';
    } else {
        scrollToTop.style.display = 'none';
    }
}

function scrollToTopFunction() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}