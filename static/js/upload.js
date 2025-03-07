document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".upload-form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        window.location.href = data.redirect;
      } else {
        Toast.show(data.message, "error");
      }
    } catch (error) {
      Toast.show("An unexpected error occurred. Please try again.", "error");
    }
  });
});
