class Popup {
  constructor() {
    this.popup = null;
    this.init();
  }

  init() {
    // Create popup element
    this.popup = document.createElement("div");
    this.popup.className = "popup";
    this.popup.innerHTML = `
            <div class="popup-content">
                <div class="popup-header">
                    <span class="close-popup">&times;</span>
                </div>
                <div class="popup-body">
                    <i class="popup-icon"></i>
                    <p class="popup-message"></p>
                </div>
            </div>
        `;
    document.body.appendChild(this.popup);

    // Add close button event
    const closeBtn = this.popup.querySelector(".close-popup");
    closeBtn.onclick = () => this.hide();

    // Close on outside click
    window.onclick = (event) => {
      if (event.target === this.popup) {
        this.hide();
      }
    };
  }

  show(message, type = "error") {
    const popupContent = this.popup.querySelector(".popup-content");
    const popupMessage = this.popup.querySelector(".popup-message");
    const popupIcon = this.popup.querySelector(".popup-icon");

    // Set message
    popupMessage.textContent = message;

    // Set icon and style based on type
    if (type === "error") {
      popupIcon.className = "popup-icon fas fa-exclamation-circle";
      popupContent.className = "popup-content error";
    } else if (type === "success") {
      popupIcon.className = "popup-icon fas fa-check-circle";
      popupContent.className = "popup-content success";
    }

    this.popup.style.display = "flex";

    // Auto hide after 3 seconds
    setTimeout(() => this.hide(), 3000);
  }

  hide() {
    this.popup.style.display = "none";
  }
}

// Initialize popup
const popup = new Popup();
