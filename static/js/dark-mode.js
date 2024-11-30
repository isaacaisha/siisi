// Function to toggle the theme
function toggleTheme() {
  const isDarkMode = document.body.classList.toggle("dark-mode");

  // Save the current theme in localStorage
  localStorage.setItem("theme", isDarkMode ? "dark" : "light");

  // Update the toggle button state
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.checked = isDarkMode;
  }

  // Dynamically update reCAPTCHA theme
  toggleCaptchaTheme(isDarkMode);
}

// On page load, apply the saved theme
window.addEventListener("load", function () {
  const savedTheme = localStorage.getItem("theme");
  const isDarkMode = savedTheme === "dark";

  // Apply the saved theme
  document.body.classList.toggle("dark-mode", isDarkMode);

  // Update the toggle button state
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.checked = isDarkMode;
  }

  // Add smooth transitions for a better user experience
  document.body.style.transition = "background-color 0.3s, color 0.3s";

  // Initialize reCAPTCHA with the correct theme
  toggleCaptchaTheme(isDarkMode);
});

// Function to dynamically render reCAPTCHA with the correct theme and size
function toggleCaptchaTheme(isDarkMode) {
  const captchaContainer = document.getElementById("recaptcha-container");

  // Check if the container exists
  if (!captchaContainer) {
    console.warn("reCAPTCHA container not found");
    return;
  }

  // Remove the existing reCAPTCHA widget
  while (captchaContainer.firstChild) {
    captchaContainer.removeChild(captchaContainer.firstChild);
  }

  // Determine the theme and size
  const theme = isDarkMode ? "dark" : "light";

  // Re-render reCAPTCHA with the updated theme
  grecaptcha.render("recaptcha-container", {
    sitekey: "6Ld_gXoqAAAAAAW5xhn_zisNn47tL0yqR391bGL6", // Replace with your actual site key
    theme: theme,
    size: "compact", // Compact size for smaller layouts
  });
}

// Attach event listener for theme toggle button
const themeToggle = document.getElementById("theme-toggle");
if (themeToggle) {
  themeToggle.addEventListener("change", toggleTheme);
}

// Function to toggle password visibility
function togglePasswordVisibility(toggleElementId, passwordFieldId) {
  const toggleElement = document.getElementById(toggleElementId);
  const passwordField = document.getElementById(passwordFieldId);

  if (toggleElement && passwordField) {
    toggleElement.addEventListener("click", function () {
      const isPassword = passwordField.getAttribute("type") === "password";
      passwordField.setAttribute("type", isPassword ? "text" : "password");

      // Toggle icon classes for better UI
      this.classList.toggle("fa-eye");
      this.classList.toggle("fa-eye-slash");
    });
  } else {
    console.warn(
      `Toggle element or password field not found (IDs: ${toggleElementId}, ${passwordFieldId})`
    );
  }
}

// Add event listeners for password visibility toggles (if applicable)
togglePasswordVisibility("togglePassword", "password");

// Show the Password Fields during Registration & Login
function togglePassword(fieldId) {
  const passwordField = document.getElementById(fieldId);
  if (passwordField) {
    passwordField.type =
      passwordField.type === "password" ? "text" : "password";
  }
}

// Optional: Ensure compatibility with missing toggle buttons
const togglePasswordElement = document.getElementById("togglePassword");
if (togglePasswordElement) {
  togglePasswordElement.addEventListener("click", function () {
    const passwordField = document.getElementById("password");
    if (passwordField) {
      passwordField.type =
        passwordField.type === "password" ? "text" : "password";
    }
  });
}
