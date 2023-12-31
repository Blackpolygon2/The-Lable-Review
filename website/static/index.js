// Select all alerts
const alerts = document.querySelectorAll('.alert');

// Close alert after 5 seconds
alerts.forEach(alert => {
  setTimeout(() => {
    alert.classList.remove('show');
    alert.classList.add('out');
  }, 5000);
});

// Click to remove alert
alerts.forEach(alert => {
  const close = alert.querySelector('.close');
  close.addEventListener('click', () => {
    alert.classList.remove('show');
    alert.classList.add('out'); 
  }) 
})

function add_to_favorites(store) {
  fetch("/add_to_favorites", {
    method: "POST",
    body: JSON.stringify({ storeid: store }),
  }).then((_res) => {
    window.location.href = "/store/"+store;
  });
}
let searchinput = document.getElementById("searchinput");
searchinput.addEventListener("input", async () => {
  let response = await fetch("/search?q=" + searchinput.value);
  let stores = await response.text();
  document.getElementById("search_results").innerHTML = stores;
})
function toggle_search(){
  elm = document.getElementById("searchview");
  if (elm.style.display === "none") {
    elm.style.display = "block";
  } else {
    elm.style.display = "none";
  }
}
function enlargeImage(img){
  let enlargedImage = document.getElementById("enlarged_image");
  enlargedImage.src = img;
  image_continer= document.getElementById("enlarged_image_container");
  image_continer.style.display = "block";
  image_continer.addEventListener("click", ()=>{
    image_continer.style.display = "none";
  })
}
// Add the event listener outside the adminsearch function
document.getElementById("admin_search").addEventListener("input", async () => {
  let adminsearchValue = document.getElementById("admin_search").value;
  let activeButtonType = getActiveButtonType();

  if (activeButtonType) {
    let response = await fetch(`/adminsearch?q=${adminsearchValue}|${activeButtonType}`);
    let result = await response.text();
    document.getElementById("admin_search_results").innerHTML = result;
  }
});

function getActiveButtonType() {
  let buttons = document.querySelectorAll(".admin_button");
  for (let button of buttons) {
    if (button.style.backgroundColor === "yellow") {
      return button.id.replace("admin_search_", "");
    }
  }
  return null;
}

function adminsearch(object) {
  let display = document.getElementById("admin_search_results");
  display.innerHTML = "";

  let type = object;

  let buttons = document.querySelectorAll(".admin_button");
  buttons.forEach(button => (button.style.backgroundColor = ""));

  let button = document.getElementById("admin_search_" + type);
  button.style.backgroundColor = "yellow";
}
async function delete_item_review(reviewid) {
  if (confirm("Are you sure you want to delete this review?")) {
    let response = await fetch("/delete_item_review", {
    method: "POST",
    body: JSON.stringify({ reviewid: reviewid }),
  });
  window.location.href = "/suscess";
  }
  
}
async function delete_item_store(storeid) {
  if (confirm("Are you sure you want to delete this store?")) {
    let response = await fetch("/delete_store", {
    method: "POST",
    body: JSON.stringify({ storeid: storeid }),
  });
  window.location.href = "/suscess";
  }
  
}
function logout() {
  window.location.href = "/logout";
}
document.getElementById('reviewimages').addEventListener('change', function() {
  // Get the selected files
  const files = this.files;
  
  // Check if the number of selected files exceeds the limit (3 in this case)
  if (files.length > 3) {
    alert('You can only upload a maximum of 3 files.');
    
    // Clear the file input to allow the user to select again
    this.value = '';
  }
});

function toggleMobileNav() {
  const navContent = document.getElementById('navContent');
  const mobileNavIcon = document.getElementById('mobile_nav_icon');

  if (navContent.classList.contains('mobile_nav_open')) {
    navContent.classList.remove('mobile_nav_open');
    mobileNavIcon.classList.remove('mobile_icon_nav_open');
  } else {
    navContent.classList.add('mobile_nav_open');
    mobileNavIcon.classList.add('mobile_icon_nav_open');
  }
}
function store_filter_query(url, store, query){
  console.log(url+"?store="+store+"?q="+query);
  window.location.href = url+store+"?q="+query;
}
