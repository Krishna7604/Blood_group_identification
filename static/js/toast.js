class Toast {
  static container = null;

  static init() {
    if (!this.container) {
      this.container = document.createElement("div");
      this.container.className = "toast-container";
      document.body.appendChild(this.container);
    }
  }

  static show(message, type = "info", duration = 5000) {
    this.init();

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    const icon = this.getIcon(type);

    toast.innerHTML = `
            <i class="fas ${icon}"></i>
            <div class="toast-message">${message}</div>
            <div class="toast-close"><i class="fas fa-times"></i></div>
        `;

    this.container.appendChild(toast);

    const close = toast.querySelector(".toast-close");
    close.addEventListener("click", () => this.dismiss(toast));

    if (duration > 0) {
      setTimeout(() => this.dismiss(toast), duration);
    }
  }

  static dismiss(toast) {
    toast.style.animation = "slideOut 0.3s ease-out forwards";
    setTimeout(() => toast.remove(), 300);
  }

  static getIcon(type) {
    switch (type) {
      case "success":
        return "fa-check-circle";
      case "error":
        return "fa-exclamation-circle";
      case "warning":
        return "fa-exclamation-triangle";
      default:
        return "fa-info-circle";
    }
  }
}
