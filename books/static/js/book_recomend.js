document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector("#recommendShelfBtn");
  const shelfField = document.querySelector("#id_addr");
  const feedback = document.querySelector("#recommendFeedback");
  const feedbackAddr = document.querySelector("#recommendShelfAddr");

  if (!button) return;

  button.addEventListener("click", function () {
    const name = document.querySelector("#id_name")?.value;
    const author = document.querySelector("#id_auther")?.value;
    const tagSelect = document.querySelector("#id_catagory");
    const selectedTags = Array.from(tagSelect?.selectedOptions || []).map(opt => opt.text);

    fetch(`/books/api/recommend-shelf/?name=${encodeURIComponent(name)}&author=${encodeURIComponent(author)}&` +
          selectedTags.map(tag => `tags[]=${encodeURIComponent(tag)}`).join("&"))
      .then(res => res.json())
      .then(data => {
        const addr = data.recommended_addr;

        // ✅ Update shelf field
        if (shelfField) {
          shelfField.value = addr;
        }

        // ✅ Show inline feedback
        if (feedback && feedbackAddr) {
          feedbackAddr.textContent = addr;
          feedback.style.display = "block";
        }
      })
      .catch(err => {
        console.error("❌ Shelf recommendation failed:", err);
      });
  });
});