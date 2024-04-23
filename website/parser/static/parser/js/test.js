console.log("JavaScript file is loaded and running!");

document.addEventListener("DOMContentLoaded", function() {
    const testElement = document.querySelector(".shop-name");
    if (testElement) {
        testElement.textContent = "Test Shop";
    }
});