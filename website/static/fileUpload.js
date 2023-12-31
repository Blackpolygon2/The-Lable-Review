const show_make_store = document.getElementById("add_store");
const store_popup = document.getElementById("makeStorePopup");
const store = document.getElementById("StorePopup");

show_make_store.addEventListener("click", () => {
  store_popup.style.display = "flex";
});

store.addEventListener("click", (e) => {
  e.stopPropagation(); // Prevent event from bubbling up to the store_popup element
});

store_popup.addEventListener("click", (e) => {
  if (e.target !== store) {
    if (confirm("Are you sure you want to leave the store creation page?")) {
      store_popup.style.display = "none";
    }
  }
});

Array.prototype.forEach.call(
  document.querySelectorAll(".pic_upload"),
  function(button) {
    const hiddenInput = button.parentElement.querySelector(
      ".inputfile"
    );
    const label = button.parentElement.querySelector(".pic_upload_label");
    const defaultLabelText = "No file(s) selected";

    // Set default text for label
    label.textContent = defaultLabelText;
    label.title = defaultLabelText;

    button.addEventListener("click", function() {
      hiddenInput.click();
    });

    hiddenInput.addEventListener("change", function() {
      const filenameList = Array.prototype.map.call(hiddenInput.files, function(
        file
      ) {
        return file.name;
      });

      label.textContent = filenameList.join(", ") || defaultLabelText;
      label.title = label.textContent;
    });
  }
);
