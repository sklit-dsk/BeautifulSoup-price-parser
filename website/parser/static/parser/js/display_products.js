let main;
let minPrice;
let maxPrice;

document.addEventListener("DOMContentLoaded", function () {
    let products = document.querySelectorAll(".products-container a");

    // Находим минимальное и максимальное значения при загрузке страницы
    Array.from(products).forEach(product => {
        let priceText = product.querySelector(".product-price").textContent;
        let price = parseFloat(priceText.replace(" €", ""));
        if (minPrice === undefined || price < minPrice) {
            minPrice = price;
        }
        if (maxPrice === undefined || price > maxPrice) {
            maxPrice = price;
        }
    });
})

document.addEventListener("DOMContentLoaded", function () {
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
            document.querySelector("#search-form > div > button").style.backgroundImage = "url(static/parser/images/giphy.gif)";
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

function sortElements(ascending = true) {
    let productLinks = document.querySelectorAll(".products-container a");
    let sortedProductLinks = Array.from(productLinks).sort((a, b) => {
        let priceA = parseFloat(a.querySelector(".product-price").textContent.replace(" €", ""));
        let priceB = parseFloat(b.querySelector(".product-price").textContent.replace(" €", ""));
        return ascending ? priceA - priceB : priceB - priceA;
    });

    // Очищаем контейнер от существующих элементов
    let productsContainer = document.querySelector(".products-container");
    productsContainer.innerHTML = '';

    // Вставляем отсортированные элементы обратно в контейнер
    sortedProductLinks.forEach(productLink => {
        productsContainer.appendChild(productLink);
    });
}


// From ... To ... element
document.addEventListener("DOMContentLoaded", function () {
    let minPriceInput = document.getElementById("minPrice");
    let maxPriceInput = document.getElementById("maxPrice");

    // Устанавливаем значения в поля "от" и "до"
    minPriceInput.value = minPrice;
    maxPriceInput.value = maxPrice;

    // Обработчик события для кнопки "Go"
    document.querySelector(".price-range button").addEventListener("click", function () {
        let enteredMinPrice = parseFloat(minPriceInput.value);
        let enteredMaxPrice = parseFloat(maxPriceInput.value);

        // Проверяем, входит ли введенный диапазон цен в диапазон всех цен
        if (enteredMinPrice >= minPrice && enteredMaxPrice <= maxPrice && enteredMinPrice <= enteredMaxPrice) {
            // Продолжаем сортировку продуктов
            filterProducts(enteredMinPrice, enteredMaxPrice);
        } else {
            // Введенные значения не соответствуют диапазону всех цен, корректируем их
            if (enteredMinPrice < minPrice || enteredMinPrice > maxPrice) {
                minPriceInput.value = minPrice;
            }
            if (enteredMaxPrice > maxPrice || enteredMaxPrice < minPrice) {
                maxPriceInput.value = maxPrice;
            }
            // Продолжаем сортировку продуктов
            filterProducts(minPrice, maxPrice);
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let sortButtons = document.querySelectorAll(".sort-items button");
    let minPriceInput = document.getElementById("minPrice");
    let maxPriceInput = document.getElementById("maxPrice");

    // Добавляем обработчик события для кнопки сброса
    document.querySelector(".reset-btn").addEventListener("click", function() {
        // Сбрасываем значения полей ввода на пустые
        minPriceInput.value = minPrice;
        maxPriceInput.value = maxPrice;

        // Сбрасываем выделение кнопок сортировки
        sortButtons.forEach(button => {
            button.classList.remove("active");
        });

        // Вызываем функцию для сортировки по умолчанию
        filterProducts(minPrice, maxPrice);
        sortElements(true);
    });
});

function filterProducts(minPrice, maxPrice) {
        let products = document.querySelectorAll(".products-container a");
        products.forEach(product => {
            let priceText = product.querySelector(".product-price").textContent;
            let price = parseFloat(priceText.replace(" €", ""));
            if (price >= minPrice && price <= maxPrice) {
                product.style.display = "block"; // Показываем продукт
            } else {
                product.style.display = "none"; // Скрываем продукт
            }
        });
    }