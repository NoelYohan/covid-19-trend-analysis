const sideMenu = document.querySelector('aside');
const menuBtn = document.querySelector('#menu_bar');
console.log(menuBtn);
const closeBtn = document.querySelector('#close_btn');


const themeToggler = document.querySelector('.theme-toggler');

if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        if (sideMenu) {
            sideMenu.style.display = "block";
        }
    });
} else {
    console.error("Menu button not found!");
}

