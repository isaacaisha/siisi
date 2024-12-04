// Selecting elements from the DOM
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatHistory = document.getElementById("chat-history");

// Initially hide chat history by adding the 'hidden' class
chatHistory.classList.add("hidden");

// Event listener to show chat history on input
chatInput.addEventListener("input", () => {
  if (chatHistory.classList.contains("hidden")) {
    chatHistory.classList.remove("hidden");
    chatHistory.classList.add("visible");
  }
});

// Event listener for form submission
chatForm.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission
  const message = chatInput.value.trim(); // Get and trim input value

  // Check if the input is empty
  if (!message) {
    // Notify the user using Django's messaging framework
    fetch("/index/response", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      body: new URLSearchParams({ message: "" }), // Send an empty message
    })
      .then((response) => response.text()) // Expect HTML with the messages block
      .then((html) => {
        // Parse the response to update the messages section
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html; // Add the server response to a temp container

        // Extract the updated messages block
        const updatedMessages = tempDiv.querySelector("div.alert");
        const existingMessages = document.querySelector("div.alert");

        if (existingMessages) {
          existingMessages.parentElement.replaceChild(
            updatedMessages,
            existingMessages
          );
        } else if (updatedMessages) {
          chatForm.insertAdjacentElement("beforebegin", updatedMessages);
        }
      })
      .catch((error) => console.error("Error:", error));
    return; // Stop further execution
  }

  // Add the user's message to the chat history
  const userMessage = createMessageElement(message, "user");
  chatHistory.appendChild(userMessage);

  // Clear the input field
  chatInput.value = "";

  // Add an "AI is typing..." indicator
  const typingIndicator = createMessageElement("AI is typing...", "ai-typing");
  chatHistory.appendChild(typingIndicator);

  // Scroll to the bottom of the chat history
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Send the message to the server
  fetch("/index/response", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      csrfmiddlewaretoken: document.querySelector("[name=csrfmiddlewaretoken]")
        .value,
      message: message,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      return response.json(); // Parse JSON response
    })
    .then((data) => {
      if (!data.response) {
        throw new Error("Invalid response format from server.");
      }

      const response = data.response;
      const audioUrl = data.audio_url;

      // Remove the typing indicator
      chatHistory.removeChild(typingIndicator);

      // Add the AI's response to the chat history
      const aiMessage = createMessageElement(response, "ai", audioUrl);
      chatHistory.appendChild(aiMessage);

      // Automatically play the audio response
      playAudio(audioUrl);

      // Scroll to the bottom of the chat history
      chatHistory.scrollTop = chatHistory.scrollHeight;
    })
    .catch((error) => {
      console.error("Error:", error);

      // Remove the typing indicator
      chatHistory.removeChild(typingIndicator);

      // Add an error message to the chat history
      const errorMessage = createMessageElement(
        "Oops! Something went wrong. Please try again later.",
        "error"
      );
      chatHistory.appendChild(errorMessage);

      // Scroll to the bottom of the chat history
      chatHistory.scrollTop = chatHistory.scrollHeight;
    });
});

// Helper function to create chat message elements
function createMessageElement(content, sender, audioUrl = null) {
  const messageWrapper = document.createElement("div");
  messageWrapper.classList.add("chat-message", sender);

  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);

  const hasLinks = /(https?:\/\/[^\s]+)/.test(content);
  if (hasLinks) {
    const parsedContent = content.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    messageElement.innerHTML = parsedContent;
  } else {
    messageElement.textContent = content;
  }

  messageWrapper.appendChild(messageElement);

  if (audioUrl) {
    const replayButton = document.createElement("button");
    replayButton.textContent = "Replay";
    replayButton.classList.add("replay-btn");
    replayButton.addEventListener("click", () => {
      playAudio(audioUrl);
    });
    messageWrapper.appendChild(replayButton);
  }

  return messageWrapper;
}

// Helper function to play audio
function playAudio(audioUrl) {
  const audio = new Audio(audioUrl);
  audio.play().catch((error) => {
    console.error("Audio playback failed:", error);
  });
}
