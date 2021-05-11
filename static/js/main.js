let currentLocation = location.href;
let menuItem = document.querySelectorAll('a.nav-link');
let menuLength = menuItem.length;
for (let i = 0; i < menuLength; i++) {
  if(menuItem[i].href === currentLocation){
    menuItem[i].classList.add("active")
  }
};