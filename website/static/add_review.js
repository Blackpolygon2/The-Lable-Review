const show_make_store = document.querySelector(".the_store_page_reviews_add_review");
const store_popup = document.querySelector(".the_store_page_reviews_add_review_form_container");
const store = document.querySelector(".the_store_page_reviews_add_review_form");

show_make_store.addEventListener("click", () => {
  store_popup.style.display = "flex";
});

store.addEventListener("click", (e) => {
  e.stopPropagation(); // Prevent event from bubbling up to the store_popup element
});

store_popup.addEventListener("click", (e) => {
  if (e.target !== store) {
    if (confirm("Are you sure you want to cancel this review?")) {
      store_popup.style.display = "none";
    }
  }
});