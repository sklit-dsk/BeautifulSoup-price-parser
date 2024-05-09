var elem = document.getElementById('productImage')
if (elem != null) {
    elem.addEventListener('error', function () {
        this.src = 'parser/images/not_found.png';
    });
}