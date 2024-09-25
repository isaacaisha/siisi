// like-unlike-convers.js

// Get CSRF token from the cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

$(document).ready(function () {
  // Handle click event on like button
  $(".like-button").click(function () {
    var conversationId = $(this).data("conversation-id");
    var button = $(this); // Store reference to the button
    var messageElement = $("#likeMessage-" + conversationId); // Get the message element

    // Toggle liked status
    var liked = button.hasClass("liked") ? 0 : 1;

    // Send AJAX request to update liked status
    $.ajax({
      url: "/update-like/" + conversationId + "/", // Note the trailing slash
      type: "POST",
      contentType: "application/json",
      headers: { "X-CSRFToken": csrftoken }, // Include the CSRF token in headers
      data: JSON.stringify({ liked: liked }), // Send liked status in request body
      success: function (response) {
        // Toggle the 'liked' class on the button
        button.toggleClass("liked");

        // Update button color based on liked status
        if (liked) {
          button.css("color", "pink");
          messageElement.html(
            "Liked!<br>You can access your liked Reviews from the menu."
          );
        } else {
          button.css("color", "lightcyan");
          messageElement.html("Unliked!");
        }

        // Show the message
        messageElement.show();

        // Hide the message after 3 seconds
        setTimeout(function () {
          messageElement.hide();
        }, 3000); // 3000 milliseconds = 3 seconds
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });
});
