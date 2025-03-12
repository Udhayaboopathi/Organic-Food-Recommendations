document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("problemInput")
    .addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        getRecommendations();
      }
    });
});

function getRecommendations() {
  const problemInput = document.getElementById("problemInput").value.trim();
  const resultContainer = document.getElementById("resultContainer");

  if (!problemInput) {
    alert("Please enter a health problem.");
    return;
  }

  // Show loading animation
  resultContainer.innerHTML = `<div class="loading"><div class="loader"></div></div>`;

  fetch(`/recommend?problem=${encodeURIComponent(problemInput)}`)
    .then((response) => response.json())
    .then((data) => {
      resultContainer.innerHTML = ""; // Clear previous results

      if (data.error) {
        resultContainer.innerHTML = `<p class="error">${data.error}</p>`;
        return;
      }

      if (!Array.isArray(data.recommendations)) {
        console.error("Unexpected API response:", data);
        resultContainer.innerHTML = `<p class="error">Unexpected response. Please try again.</p>`;
        return;
      }

      data.recommendations.forEach((item) => {
        const foodCard = document.createElement("div");
        foodCard.classList.add("food-card");

        // Remove "**" from food names
        const cleanFoodName = item.food.replace(/\*\*/g, "");

        foodCard.innerHTML = `
            <h3>${cleanFoodName}</h3>
            <p><strong>Benefits:</strong> ${item.benefits}</p>
            <p><strong>Recipe:</strong></p>
            <ul>${item.recipe.map((step) => `<li>${step}</li>`).join("")}</ul>
          `;

        resultContainer.appendChild(foodCard);
      });
    })
    .catch((error) => {
      console.error("Error fetching recommendations:", error);
      resultContainer.innerHTML = `<p class="error">Failed to fetch recommendations. Please try again.</p>`;
    });
}
