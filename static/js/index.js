const timer = setTimeout(function () {
    window.location = intro;
}, 18000);

let sec = 15;

let s = document.getElementById("s");
let timer_1 = document.getElementById("timer-1");
let greeting_1 = document.getElementById("indicator-1");
let greeting_2 = document.getElementById("indicator-2");
let greeting_3 = document.getElementById("indicator-3");
let greeting_4 = document.getElementById("indicator-4");
let greeting_5 = document.getElementById("indicator-5");

const x = setInterval(function () {
    if (sec >= 0 && sec < 11) {
        s.textContent = "초";
        s.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
        timer_1.textContent = "\u00a0" + sec + "\u00a0";
        timer_1.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
        greeting_1.textContent = "인트로 진입까지";
        greeting_1.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
    };
    if (sec > 8) {
        greeting_2.textContent = "잠시만 기다려주세요...";
        greeting_2.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
    } else if (sec > 5) {
        greeting_2.textContent = "";
        greeting_3.textContent = "방문해주셔서 감사합니다!";
        greeting_3.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
    } else if (sec > 2) {
        greeting_3.textContent = "";
        greeting_4.textContent = "감상 후 글 남겨주세요!";
        greeting_4.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
    } else if (sec >= 0) {
        greeting_4.textContent = "";
        greeting_5.textContent = "감사합니다...";
        greeting_5.classList.add("animate__animated", "animate__fadeInUp", "animate__duration-1s", "text-white");
    } else if (sec < 0) {
        s.textContent = "";
        timer_1.textContent = "";
        greeting_1.textContent = "불러오는 중...";
        greeting_5.textContent = "";
        const spinner = document.querySelector("#spinner-div");
        spinner.classList.add("spinner-border", "text-danger");
    } if (sec < 4) {
        timer_1.classList.remove("text-white");
        timer_1.classList.add("text-danger");
    };
    sec--;
}, 1000);