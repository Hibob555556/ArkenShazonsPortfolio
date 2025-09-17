// Sidebar toggle
const nav = document.getElementById("navbar");
const toggleBtn = document.getElementById("menu-toggle");

// Auto-collapse on small screens (<914px)
function handleSidebar() {
  if (window.innerWidth < 914) {
    nav.classList.add("hide");
  } else {
    nav.classList.remove("hide");
  }
}

// Run on load and resize
window.addEventListener("load", handleSidebar);
window.addEventListener("resize", handleSidebar);

// Hamburger toggle
toggleBtn.addEventListener("click", () => {
  nav.classList.toggle("hide");
});

// ---------------- Screen Switching ----------------
const decToBinScreen = document.getElementById("decToBinScreen");
const binToDecScreen = document.getElementById("binToDecScreen");
const decToBinLink = document.getElementById("decToBinLink");
const binToDecLink = document.getElementById("binToDecLink");

decToBinLink.addEventListener("click", () => {
  decToBinScreen.style.display = "block";
  binToDecScreen.style.display = "none";

  // Close sidebar on small screens after selection
  if (window.innerWidth < 914) {
    nav.classList.add("hide");
  }
});

binToDecLink.addEventListener("click", () => {
  decToBinScreen.style.display = "none";
  binToDecScreen.style.display = "block";

  // Close sidebar on small screens after selection
  if (window.innerWidth < 914) {
    nav.classList.add("hide");
  }
});
