const glow = document.createElement("div");

glow.className = "cursor-glow";

document.body.appendChild(glow);

document.addEventListener("mousemove", (e) => {
  glow.style.left = e.clientX + "px";

  glow.style.top = e.clientY + "px";
});

function copyURL() {
  const input = document.getElementById("shortURL");

  navigator.clipboard.writeText(input.value);

  const btn = document.querySelector(".result-url button");

  btn.innerHTML = "✓ Copied";

  setTimeout(() => {
    btn.innerHTML = '<i class="bi bi-copy"></i> Copy';
  }, 2000);
}

function copyTopLink(link) {
  navigator.clipboard.writeText(link);

  showToast("success", "Copied!", "Short URL copied to clipboard.");
}

// ================= DELETE MODAL =================

const modal = document.getElementById("deleteModal");

const confirmBtn = document.getElementById("confirmDeleteBtn");

function openDeleteModal(url) {
  confirmBtn.href = url;

  modal.classList.add("active");
}

function closeDeleteModal() {
  modal.classList.remove("active");
}

modal.addEventListener("click", function (e) {
  if (e.target === modal) {
    closeDeleteModal();
  }
});

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeDeleteModal();
  }
});

// ================= TOAST =================

function showToast(type, title, message) {
  const toast = document.getElementById("toast");

  const icon = document.getElementById("toastIcon");

  const iconBox = document.querySelector(".toast-icon");

  document.getElementById("toastTitle").innerText = title;

  document.getElementById("toastMessage").innerText = message;

  if (type === "success") {
    icon.className = "bi bi-check-circle-fill";

    iconBox.style.background = "#22C55E";
  } else if (type === "error") {
    icon.className = "bi bi-x-circle-fill";

    iconBox.style.background = "#EF4444";
  } else {
    icon.className = "bi bi-info-circle-fill";

    iconBox.style.background = "#3B82F6";
  }

  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}
