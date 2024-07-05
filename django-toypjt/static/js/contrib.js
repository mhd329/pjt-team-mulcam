const body_animation = function () {
    let items, winH;

    const initModule = function () {
        items = document.getElementsByClassName("invisible");
        winH = window.innerHeight;
        _addEventHandlers();
    }

    const _addEventHandlers = function () {
        window.addEventListener("scroll", _checkPosition);
        window.addEventListener("resize", initModule);
    };

    const _checkPosition = function () {
        for (let i = 0; i < items.length; i++) {
            let posFromTop = items[i].getBoundingClientRect().top;
            if (winH - posFromTop > 750) {
                items[i].className = items[i].className.replace("invisible", "animate__animated animate__zoomIn animate__dulation-3s");
            }
        }
    }

    return {
        init: initModule
    }
}

body_animation().init();