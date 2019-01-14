function menuIconClick() {
    var x = document.getElementById("main-nav");
    if (x.className === "menus") {
        x.className += " show";
    } else {
        x.className = "menus";
    }
}

var specifiedElement = document.getElementById('menu-icon');
document.addEventListener('click', function (event) {
    var isClickInside = specifiedElement.contains(event.target);
    var x = document.getElementById("main-nav");
    if (!isClickInside) {
        if (x.className === "menus") {
            //x.className += " show";
        } else {
            x.className = "menus";
        }
    }
});