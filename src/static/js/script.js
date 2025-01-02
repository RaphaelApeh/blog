const preloader = document.querySelector(".preloader");

// window.addEventListener('load', () => {
//     preloader.remove();
// })
if (preloader.dataset.is_authenticated === "True"){
    window.addEventListener('load', () => {
            preloader.remove();
        })
}