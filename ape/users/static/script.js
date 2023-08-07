const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
    bar.addEventListener('click', () => {
     nav.classList.add('active');   
    })
}

if (close) {
    close.addEventListener('click', () => {
     nav.classList.remove('active');   
    })
}

// Get all the links in the navbar
const navbarLinks = document.querySelectorAll('#navbar li a');

// Add an event listener to each link
navbarLinks.forEach(link => {
  link.addEventListener('click', function(event) {
    // Allow the default link behavior
    // This will navigate to the href specified in the link
    // and load the new page
    // After that, we can update the active class
    return true;

    // Remove the "active" class from all links
    navbarLinks.forEach(link => {
      link.classList.remove('active');
    });

    // Add the "active" class to the clicked link
    this.classList.add('active');
  });
});





// Sign up page

document.addEventListener("DOMContentLoaded", function() {
  let signupBtn = document.getElementById("signupBtn");
  let signinBtn = document.getElementById("signinBtn");
  let logoutBtn = document.getElementById("logoutBtn");

  signinBtn.onclick = function() {
    // some code
    nameField.style.maxHeight = "0";
    title.innerHTML = "Sign in";
    signupBtn.classList.add("disable");
    signinBtn.classList.remove("disable");
    
  };

  signupBtn.onclick = function() {
    // some code
    nameField.style.maxHeight = "60px";
    title.innerHTML = "Sign up";
    signupBtn.classList.remove("disable");
    signinBtn.classList.add("disable");
  };

  logoutBtn.onclick = function() {
    // some code to handle logout
    showPopup("You have been logged out.");
    };

    function showPopup(message) {
      let popup = document.getElementById("popup");
      let popupMessage = document.getElementById("popup-message");
  
      popupMessage.innerText = message;
      popup.style.display = "block";
      
      setTimeout(function() {
        popup.style.display = "none";
      }, 300000);
      }
      
      });
