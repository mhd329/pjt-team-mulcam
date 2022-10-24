const timer = setTimeout(function () {
    window.location = review_url
}, 4000);

let sec = 3;
let indicator = document.getElementById("indicator");
const spinner = document.querySelector("#spinner-div")
const x = setInterval(function () {
    indicator.textContent = sec + "초 후에 게시판으로 돌아갑니다.";
    sec--;
    if (sec < 0) {
        clearInterval(x);
        indicator.textContent = "잠시만 더 기다려주세요...";
        spinner.classList.add("spinner-border", "text-primary")
    }
}, 1000)